from io import StringIO
import requests
import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.models import db, Studies, MutableStudy, Answers, Subjects, Participations

bp = Blueprint('server', __name__)

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


@bp.route('/')
def home():
    # show options to either
    # join study or configure study
    session.clear()
    return render_template('index.html')


@bp.route('/join_menu')
def join_menu():
    # show options for joining study
    return render_template('join_menu.html')


@bp.route('/config_menu')
def config_menu():
    # show options for configuring study
    return render_template('config_menu.html')


@bp.route('/study_id')
def show_study_id():
    study_id = session['study_id']
    return render_template('show_id.html', study_id=study_id)


@bp.route('/vignette')
def show_vignette():
    # get study & participation
    study_id = session['study_id']
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    subject_id = session['subject_id']
    participation = Participations.query.filter_by(study=study_id, subject=subject_id).first()
    config = participation.configuration

    print('current participant config: ', config)

    # get vignette parameters
    vignette_params = study.get_vignette_params(config)
    return render_template('vignette.html', txt=vignette_params['txt'], qset=vignette_params['qset'])


@bp.route('/done')
def done():
    return render_template('done.html')


@bp.route('/randomize')
def randomize():
    # get data
    subject_id = session['subject_id']
    study_id = session['study_id']
    # get study
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    # get participation
    participation = Participations.query.filter_by(study=study_id, subject=subject_id).first()
    config = participation.configuration

    print('current participant config: ', config)

    # make sure user answered questions before randomization
    # (at a y node)
    if len(config) % 2 == 1:
        return redirect(url_for('server.show_vignette'))
    # randomize if next vignette exists
    if len(config) < len(study.lvls) * 2:
        x = study.randomize(config)
        config.append(x)
        # update study & participation
        study_tbl.study = study
        print(type(participation))
        print(type(participation.configuration))
        participation.configuration = config
        db.session.commit()

        print('current participant config after randomization: ', config)
        study.print()

        # redirect to next vignette
        return redirect(url_for('server.show_vignette'))
    # otherwise finish survey
    else:
        print('current participant config after completion: ', config)
        study.print()
        session.clear()
        return redirect(url_for('server.done'))


@bp.route('/join', methods=('GET', 'POST'))
def join_study():
    if request.method == 'GET':
        return redirect(url_for('server.join_menu'))
    # get form args
    args = request.form
    # get study id
    study_id = args['study_id']
    username = args['username']
    password = args['password']
    # find study
    study_tbl = Studies.query.filter_by(id=study_id).first()
    # get redcap attributes
    token = study_tbl.token
    username_field = study_tbl.username_field
    password_field = study_tbl.password_field
    # get list of users
    data = {
        'token': token,
        'content': 'record',
        'action': 'export',
        'format': 'csv',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': username_field,
        'fields[1]': password_field,
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    # make request
    r = requests.post('https://redcap.stanford.edu/api/', data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        print("Error: " + str(e))
        raise e
    # verify user and password
    df = pd.read_csv(StringIO(r.text))
    # no match
    if not ((df[username_field] == username) & (df[password_field] == password)).any():
        flash('Invalid username and password')
        return redirect(url_for('server.join_menu'))
    # add to table if not exist
    if not Subjects.query.get(username):
        db.session.add(
            Subjects(id=username)
        )
    # get study
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
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

    print('current participant config: ', config)

    # print
    study.print()
    # store study id & username
    session['study_id'] = study_id
    session['subject_id'] = username
    # show vignette
    return redirect(url_for('server.randomize'))


@bp.route('/configure', methods=['GET', 'POST'])
def configure_study():
    if request.method == 'GET':
        return redirect(url_for('server.config_menu'))
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
        # store study id in session data
        session['study_id'] = study.id
        return redirect(url_for('server.show_study_id'))


@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('server.show_vignette'))
    # get study & participation
    study_id = session['study_id']
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    subject_id = session['subject_id']
    participation = Participations.query.filter_by(study=study_id, subject=subject_id).first()
    config = participation.configuration
    # get answers
    answers = request.form
    print(answers)
    # store answers
    pass
    config = study.get_answers(answers, config)
    # update study & participation
    participation.configuration = config
    study_tbl.study = study
    db.session.commit()
    # randomize
    return redirect(url_for('server.randomize'))
