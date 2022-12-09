import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)
from flaskr.models import db, MutableStudy, Participations, StudyLevels, LevelQuestions, Levels, Questions, Answers

bp = Blueprint('administer', __name__)


@bp.before_app_request
def load_logged_in_user():
    # check whether participation exists for each request
    subject_id = session.get('subject_id')
    study_id = session.get('study_id')
    if subject_id is None or study_id is None:
        g.user = None
    else:
        participation = Participations.query.filter_by(study_id=study_id, subject_id=subject_id).first_or_404()
        g.user = participation


@bp.after_app_request
def after_request(response):
    # keep from caching page in case of back button
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0"
    return response


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # redirect to join menu if participation does not exist
        if g.user is None:
            return redirect(url_for('home.join_menu'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/vignette')
@login_required
def show_vignette():
    # get participation
    study_id = session['study_id']
    subject_id = session['subject_id']
    participation = Participations.query.filter_by(study_id=study_id, subject_id=subject_id).first_or_404()
    config = participation.configuration

    # print
    print('current participant config: ', config)

    # make sure on x node
    if len(config) % 2 == 0:
        return redirect(url_for('administer.randomize'))

    # get vignette parameters
    # vignette_params = study.get_vignette_params(config)
    # return render_template('vignette.html', txt=vignette_params['txt'], qset=vignette_params['qset'])

    # get level
    level_num = MutableStudy.get_level_num(config)
    query = db.session.query(Levels). \
        filter_by(level_num=level_num). \
        join(StudyLevels). \
        filter_by(study_id=study_id)
    level = query.first_or_404()
    print('\nGetting level')
    print(query)
    print(level)
    # get questions
    query = db.session.query(Questions). \
        join(LevelQuestions). \
        filter_by(level_id=level.id)
    qset = query.all()
    print("\nGetting questions")
    print(query)
    print(qset)

    # get vignette parameters
    if config[-1] == 1:
        txt = level.scna
    elif config[-1] == -1:
        txt = level.scnb
    else:
        raise ValueError

    return render_template('vignette.html', txt=txt, qset=qset)


@bp.route('/randomize')
@login_required
def randomize():
    # get study and participation
    subject_id = session['subject_id']
    study_id = session['study_id']
    participation = Participations.query.filter_by(study_id=study_id, subject_id=subject_id).first_or_404()
    study = participation.study.study
    config = participation.configuration

    # print
    print('current participant config: ', config)

    # make sure user answered questions before randomization
    # (at a y node)
    if len(config) % 2 == 1:
        return redirect(url_for('administer.show_vignette'))

    # randomize if next vignette exists
    if len(config) < study.numlvls * 2:
        x = study.randomize(config)
        config.append(x)
        # update study & participation
        participation.configuration = config
        db.session.commit()
        # print
        print('current participant config after randomization: ', config)
        study.print()
        # redirect to next vignette
        return redirect(url_for('administer.show_vignette'))

    # otherwise finish survey
    else:
        # print
        print('current participant config at completion: ', config)
        study.print()
        return redirect(url_for('administer.done'))


@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    # redirect if GET
    if request.method == 'GET':
        return redirect(url_for('administer.show_vignette'))

    # get study & participation
    study_id = session['study_id']
    subject_id = session['subject_id']
    participation = Participations.query.filter_by(study_id=study_id, subject_id=subject_id).first_or_404()
    config = participation.configuration
    study = participation.study.study

    # get answers
    answers = request.form
    print('\nAnswers')
    print(answers)

    # make sure only 1 key value pair
    # make sure answers all str
    for qid in answers.keys():
        assert len(answers.getlist(qid)) == 1
        assert isinstance(answers[qid], str)

    # store answers
    answers = dict(answers)
    for qid in answers:
        db.session.add(
            Answers(
                subject_id=subject_id,
                question_id=qid,
                answer=answers[qid]
            )
        )
    config = study.get_answer(int(answers['0']), config)

    # update study & participation
    participation.configuration = config
    db.session.commit()

    # randomize
    return redirect(url_for('administer.randomize'))


@bp.route('/exit')
@login_required
def exit_survey():
    session.clear()
    return redirect(url_for('home.home'))


@bp.route('/done')
@login_required
def done():
    # check if actually done
    # get study and participation
    subject_id = session['subject_id']
    study_id = session['study_id']
    participation = Participations.query.filter_by(study_id=study_id, subject_id=subject_id).first_or_404()
    config = participation.configuration
    study = participation.study.study
    # redirect if not done
    if len(config) < study.numlvls * 2:
        return redirect(url_for('administer.randomize'))
    # clear session
    session.clear()
    return render_template('done.html')
