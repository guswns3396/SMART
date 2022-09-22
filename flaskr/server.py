from flask import Flask, request, session, redirect, url_for, render_template

from Study import Study

# maps study id to Study object
STUDIES = {}

app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static'
)

app.secret_key = 'c8bfa41b5909bd96de540549a6ea6a390d3beea2ad115452f4c771fa8b43dc8d'


@app.errorhandler(KeyError)
def keyError(e):
    error = str(e) + " key not found"
    return render_template('error.html', error=error), 400


@app.route('/')
def home():
    # show options to either
    # join study or configure study
    session.clear()
    return render_template('index.html')


@app.route('/join_menu')
def join_menu():
    # show options for joining study
    return render_template('join_menu.html')


@app.route('/config_menu')
def config_menu():
    # show options for configuring study
    return render_template('config_menu.html')


@app.route('/study_id')
def show_study_id():
    study_id = session['study_id']
    return render_template('show_id.html', study_id=study_id)


@app.route('/vignette')
def show_vignette():
    # get study & config
    study_id = session['study_id']
    study = STUDIES[study_id]
    config = session['config']
    vignette_params = study.get_vignette_params(config)
    return render_template('vignette.html', txt=vignette_params['txt'], qset=vignette_params['qset'])


@app.route('/done')
def done():
    return render_template('done.html')


@app.route('/randomize')
def randomize():
    # get data
    config = session['config']
    study_id = session['study_id']
    study = STUDIES[study_id]
    # make sure user answered questions before randomization
    # (at a y node)
    if len(config) % 2 == 1:
        return redirect(url_for('show_vignette'))
    # randomize if next vignette exists
    if len(config) < len(study.lvls) * 2:
        x = study.randomize(config)
        config.append(x)
        # update config
        session['config'] = config

        print(config)
        study.print()

        # redirect to next vignette
        return redirect(url_for('show_vignette'))
    else:
        print(config)
        study.print()
        session.clear()
        return redirect(url_for('done'))


@app.route('/join')
def join_study():
    # get query parameter for study id
    args = request.args.to_dict()
    # if study_id not defined redirect to join menu
    if 'study_id' not in args:
        return redirect(url_for('join_menu'))
    # else get study id
    study_id = args['study_id']
    # get study
    study = STUDIES[study_id]
    # add participant
    study.enroll()
    # set initial config
    config = []
    # store study id & participant configuration
    session['config'] = config
    session['study_id'] = study_id
    # show vignette
    return redirect(url_for('randomize'))


@app.route('/configure', methods=['GET', 'POST'])
def configure_study():
    if request.method == 'GET':
        return redirect(url_for('config_menu'))
    # read data
    parameters = request.form
    # create study
    study = Study(
        parameters
    )
    STUDIES[study.id] = study
    # store study id in session data
    session['study_id'] = study.id
    return redirect(url_for('show_study_id'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('show_vignette'))
    # get study & config
    study_id = session['study_id']
    study = STUDIES[study_id]
    config = session['config']
    # get answers
    answers = request.form
    print(answers)
    config = study.get_answers(answers, config)
    # update config
    session['config'] = config
    # randomize
    return redirect(url_for('randomize'))


if __name__ == '__main__':
    app.run(debug=True)
