from flask import Flask, request, Response, json

from Study import Study

app = Flask(__name__)

@app.route('/configure', methods=['POST'])
def configure():
    """
    Configures the parameters of the study
    :return:
    """
    # read data
    data = json.loads(request.data)
    # TODO: read data to create experiment setup
    study = Study(
        numlvl=data['numlvl'],
        numbranch=data['numbranch']
    )
    
    # success
    resp = Response(response=json.dumps(data),status=200)
    return resp

if __name__=='__main__':
    app.run(debug=True)