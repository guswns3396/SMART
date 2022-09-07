from flask import Flask, request, Response, json, abort

from Study import Study

# maps study id to Study object
STUDIES = {}

app = Flask(__name__)

@app.route('/join/<study_id>')
def join_study(study_id):
    """
    Allows survey responder to join a study
    Randomizes responder
    :param study_id: id of study
    :return:
    """
    if study_id not in STUDIES:
        abort(Response('Room with given ID already exists', status=400))
    # TODO randomize

@app.route('/configure', methods=['POST'])
def configure():
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


if __name__ == '__main__':
    app.run(debug=True)
