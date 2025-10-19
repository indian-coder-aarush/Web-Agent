import ast

import flask

app = flask.Flask(__name__)

@app.route("/api/receive-prompt", methods=["POST"])
def receive_prompt():
    data = flask.request.get_json()
    text = data.get("prompt",'')
    return ''

@app.route("/api/give-response")
def give_response():
    return flask.jsonify({"hello":"world"})

if __name__ == "__main__":
    app.run(debug=True, port = 1234)