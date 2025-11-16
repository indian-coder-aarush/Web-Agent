import flask
import flask_cors
import Brain
import time
import os
import shutil

backend = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(backend, ".."))
workspace = os.path.join(root, "workspace")
build = os.path.join(root, "frontend", "build")

os.makedirs(workspace,exist_ok = True)

app = flask.Flask(__name__,static_folder=build, static_url_path="/")
flask_cors.CORS(app)
app.config['SECRET_KEY'] = 'secret!'

@app.route("/")
def index():
    return flask.send_from_directory(app.static_folder, "index.html")

@app.route("/api/receive-prompt", methods=["POST"])
def receive_prompt():
    data = flask.request.get_json()
    prompt = data.get("prompt",'')
    if prompt == 'clear!!!000':
        Brain.messages = Brain.messages[0:1]
        Brain.AI_messages = []
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
            os.mkdir(workspace)
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

@app.route("/preview/")
def preview_index():
    return flask.send_from_directory(workspace, "index.html")

@app.route("/preview/<path:path>")
def preview_files(path):
    return flask.send_from_directory(workspace, path)

if __name__ == "__main__":
    app.run(debug=True, port=1235)