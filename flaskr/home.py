from io import StringIO
import requests
import pandas as pd
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from flaskr.models import db, MutableStudy, Studies, Subjects, Participations,\
    Levels, Questions, LevelQuestions, StudyLevels

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
    if not Studies.query.filter_by(id=study_id).first_or_404():
        flash('Invalid study ID')
        return redirect(url_for('home.join_menu'))

    # read in users and passwords using REDCap API
    study_row = Studies.query.filter_by(id=study_id).first_or_404()
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
    participation = Participations.query.filter_by(study_id=study_id, subject_id=username).first_or_404()
    # add if no participation
    if not participation:
        db.session.add(
            Participations(
                study_id=study_id,
                subject_id=username,
                configuration=[]
            )
        )
        participation = Participations.query.filter_by(study_id=study_id, subject_id=username).first_or_404()
        # add participant
        participation.study.study.enroll()
        # commit changes
        db.session.commit()
    config = participation.configuration
    study = participation.study.study

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

    # verify data
    MutableStudy.verify_params(parameters)
    # parse parameters to create levels & questions
    levels = MutableStudy.make_levels(parameters)
    # make tree
    root = MutableStudy.make_tree(levels)
    # instantiate study
    study = MutableStudy(root=root, numlvls=len(levels), p=float(parameters['p']))

    # insert study
    db.session.add(
        Studies(
            id=study.id,
            study=study,
            numlvls=study.numlvls,
            p=study.p,
            token=parameters['token'],
            username_field=parameters['username_field'],
            password_field=parameters['password_field']
        )
    )
    # insert levels to db
    for i, level in enumerate(levels):
        db.session.add(
            Levels(
                level_num=i,
                scna=level.scna,
                scnb=level.scnb
            )
        )
        currlvl = Levels.query.order_by(Levels.id.desc()).first_or_404()
        # fill association table
        db.session.add(
            StudyLevels(
                level_id=currlvl.id,
                study_id=study.id
            )
        )
        # insert questions to db
        for j, question in enumerate(level.qset):
            db.session.add(
                Questions(
                    question_num=j,
                    question=question.q,
                    range=question.a
                )
            )
            currq = Questions.query.order_by(Questions.id.desc()).first_or_404()
            # fill association table
            db.session.add(
                LevelQuestions(
                    level_id=currlvl.id,
                    question_id=currq.id
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
