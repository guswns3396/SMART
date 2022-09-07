from flask import Flask, request, Response, json, abort

from Study import Study

# maps study id to Study object
STUDIES = {}

app = Flask(__name__)

# TODO: how to keep frontend and backend separate?

@app.route('/')
def home():
    """

    :return:
    """
    # show options to either
    # join study or configure study
    pass


@app.route('/join_menu')
def join_menu():
    """

    :return:
    """
    # show options for joining study
    pass


@app.route('/config_menu')
def config_menu():
    """

    :return:
    """
    # show options for configuring study
    pass


@app.route('/join/<study_id>')
def join_study(study_id):
    """
    Allows survey responder to join a study
    Randomizes responder
    :param study_id: id of study
    :return:
    """
    # abort if invalid study id
    if study_id not in STUDIES:
        abort(Response('Room with given ID does not exist', status=400))
    # find study
    study = STUDIES[study_id]
    # TODO: give participant first vignette


@app.route('/configure', methods=['POST'])
def configure_study():
    """
    Configures the parameters of the study
    :return:
    """
    # read data
    parameters = json.loads(request.data)
    # TODO: verify parameters syntax correct
    # level 0 only has 1 text
    # binary

    study = Study(
        parameters
    )
    STUDIES[study.id] = study
    # success, return study id
    resp = Response(response=json.dumps(study.id), status=200)
    return resp


@app.route('/vignette')
def show_vignette(params):
    """

    :param params:
    :return:
    """
    # use the parameters to show vignette
    # and question sets & choices
    # then have submission redirect to submit
    # TODO: find a way to get parameters without GET in URL
    pass


@app.route('/submit', methods=['POST'])
def submit():
    """

    :return:
    """
    # store the participant's answers
    # randomize if next vignette exists
    # get vignette params following randomization
    # redirect to vignette
    pass


if __name__ == '__main__':
    app.run(debug=True)
