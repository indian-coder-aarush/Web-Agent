import flask
import flask_cors
import flask_socketio
import Brain

app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")

@app.route("/api/receive-prompt", methods=["POST"])
def receive_prompt():
    data = flask.request.get_json()
    prompt = data.get("prompt",'')
    Brain.execute(prompt)
    return ''

@app.route("/api/give-response")
def give_response():
    return flask.jsonify({"hello":"world"})

def send_to_frontend(event,message):
    socketio.emit(event,message)

if __name__ == "__main__":
    app.run(debug=True, port = 1234)