import flask
import flask_cors
import Brain
import time

app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config['SECRET_KEY'] = 'secret!'

@app.route("/api/receive-prompt", methods=["POST"])
def receive_prompt():
    data = flask.request.get_json()
    prompt = data.get("prompt",'')
    Brain.execute(prompt)
    return '', 200

@app.route("/api/give-response")
def give_response():
    return flask.jsonify({"hello":"world"})

@app.route("/api/send")
def live():
    def send():
        index = 0
        while True:
            if index < len(Brain.AI_messages):
                message = Brain.AI_messages[-1]
                yield "data: "+message+"\n\n"
                index += 1
            time.sleep(1)
    return flask.Response(send(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, port=1235)