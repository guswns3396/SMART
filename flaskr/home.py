from io import StringIO
import requests
import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.models import db, Studies, MutableStudy, Subjects, Participations

bp = Blueprint('home', __name__)


# @bp.errorhandler(KeyError)
# def keyError(e):
#     error = str(e) + " key not found"
#     return render_template('error.html', error=error), 400
#
#
# @bp.errorhandler(ValueError)
# def valueError(e):
#     error = str(e)
#     return render_template('error.html', error=error), 400

@bp.route('/join', methods=('GET', 'POST'))
def join_study():
    # redirect if GET method
    if request.method == 'GET':
        return redirect(url_for('home.join_menu'))

    # parse form
    study_id, username, password = request.form['study_id'], request.form['username'], request.form['password']

    # validate study id
    if not Studies.query.filter_by(id=study_id).first():
        flash('Invalid study ID')
        return redirect(url_for('home.join_menu'))

    # read in users and passwords using REDCap API
    study_row = Studies.query.filter_by(id=study_id).first()
    data = {
        'token': study_row.token,
        'content': 'record',
        'action': 'export',
        'format': 'csv',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': study_row.username_field,
        'fields[1]': study_row.password_field,
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    r = requests.post('https://redcap.stanford.edu/api/', data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # it wasn't a 200
        print("Error: " + str(e))
        raise e
    df = pd.read_csv(StringIO(r.text))

    # authenticate with REDCap data
    if not ((df[study_row.username_field] == username) & (df[study_row.password_field] == password)).any():
        flash('Invalid username and password')
        return redirect(url_for('home.join_menu'))
    # add subject if not part of database
    if not Subjects.query.get(username):
        db.session.add(
            Subjects(id=username)
        )
        # commit changes
        db.session.commit()

    # check participation
    study = study_row.study
    # add if no participation
    if not Participations.query.filter_by(study=study_id, subject=username).first():
        db.session.add(
            Participations(
                study=study_id,
                subject=username,
                configuration=[]
            )
        )
        # add participant
        study.enroll()
        # commit changes
        db.session.commit()
    # get participation
    participation = Participations.query.filter_by(study=study_id, subject=username).first()
    config = participation.configuration

    # print
    print('current participant config: ', config)
    study.print()

    # store study id & username
    session['study_id'] = study_id
    session['subject_id'] = username

    # show vignette
    return redirect(url_for('administer.randomize'))


@bp.route('/configure', methods=['GET', 'POST'])
def configure_study():
    # redirect if GET
    if request.method == 'GET':
        return redirect(url_for('home.config_menu'))

    # read data
    parameters = request.form

    # create study
    try:
        study = MutableStudy(
            parameters
        )
    except ValueError as e:
        raise e
    else:
        db.session.add(
            Studies(
                id=study.id,
                study=study,
                token=parameters['token'],
                username_field=parameters['username_field'],
                password_field=parameters['password_field']
            )
        )
        db.session.commit()

        # show study id
        return render_template('show_id.html', study_id=study.id)


@bp.route('/')
def home():
    # show options to either
    # join study or configure study
    return render_template('index.html')


@bp.route('/join_menu')
def join_menu():
    # show options for joining study
    return render_template('join_menu.html')


@bp.route('/config_menu')
def config_menu():
    # show options for configuring study
    return render_template('config_menu.html')