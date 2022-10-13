from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.models import db, Studies, MutableStudy

from flaskr.Study import Study

bp = Blueprint('server', __name__)

# TODO: store answers
# TODO: input validation
# TODO: how to keep from leaving survey
# TODO: incorporate subject ID? => keep from retaking survey


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
    # get study & config
    study_id = session['study_id']
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    config = session['config']
    vignette_params = study.get_vignette_params(config)
    # update study
    study_tbl.study = study
    db.session.commit()
    return render_template('vignette.html', txt=vignette_params['txt'], qset=vignette_params['qset'])


@bp.route('/done')
def done():
    return render_template('done.html')


@bp.route('/randomize')
def randomize():
    # get data
    config = session['config']
    study_id = session['study_id']
    # get study
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    # make sure user answered questions before randomization
    # (at a y node)
    if len(config) % 2 == 1:
        return redirect(url_for('server.show_vignette'))
    # randomize if next vignette exists
    if len(config) < len(study.lvls) * 2:
        x = study.randomize(config)
        config.append(x)
        # update study
        study_tbl.study = study
        db.session.commit()
        # update config
        session['config'] = config

        print(config)
        study.print()

        # redirect to next vignette
        return redirect(url_for('server.show_vignette'))
    else:
        print(config)
        study.print()
        session.clear()
        return redirect(url_for('server.done'))


@bp.route('/join')
def join_study():
    # get query parameter for study id
    args = request.args.to_dict()
    # if study_id not defined redirect to join menu
    if 'study_id' not in args:
        return redirect(url_for('server.join_menu'))
    # else get study id
    study_id = args['study_id']
    # get study
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    # add participant
    study.enroll()
    # print
    study.print()
    # set initial config
    config = []
    db.session.commit()
    # store study id & participant configuration
    session['config'] = config
    session['study_id'] = study_id
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
            Studies(id=study.id, study=study)
        )
        db.session.commit()
        # store study id in session data
        session['study_id'] = study.id
        return redirect(url_for('server.show_study_id'))


@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('server.show_vignette'))
    # get study & config
    study_id = session['study_id']
    study_tbl = Studies.query.filter_by(id=study_id).first()
    study = study_tbl.study
    config = session['config']
    # get answers
    answers = request.form
    print(answers)
    config = study.get_answers(answers, config)
    # update config
    session['config'] = config
    # update study
    study_tbl.study = study
    db.session.commit()
    # randomize
    return redirect(url_for('server.randomize'))
