import flask
import flask_cors
import Brain
import time
import os
import shutil
import db

backend = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(backend, ".."))
workspace = os.path.join(root, "workspace")
build = os.path.join(root, "frontend", "build")

os.makedirs(workspace,exist_ok = True)

token = None

app = flask.Flask(__name__,static_folder=build, static_url_path="/")
flask_cors.CORS(app)
app.config['SECRET_KEY'] = 'secret!'

def rebuild_workspace(user_token):
    if os.path.exists(workspace):
        shutil.rmtree(workspace)
    os.makedirs(workspace, exist_ok=True)
    db_user = db.get_or_make_user(user_token)
    for file in db_user:
        file_path = os.path.join(workspace, file['filepath'])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file['content'])

@app.route("/")
def index():
    return flask.send_from_directory(app.static_folder, "index.html")

@app.route("/api/receive-prompt", methods=["POST"])
def receive_prompt():
    data = flask.request.get_json()
    prompt = data.get("prompt",'')
    token = data.get("token")
    db.get_or_make_user(token)
    if prompt == 'clear!!!000':
        Brain.messages = Brain.messages[0:1]
        Brain.AI_messages = []
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
            os.mkdir(workspace)
    Brain.execute(prompt, token = token)
    return '', 200

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
    token = flask.request.args.get("token")
    rebuild_workspace(token)
    return flask.send_from_directory(workspace, "index.html")

@app.route("/preview/<path:path>")
def preview_files(path):
    token = flask.request.args.get("token")
    rebuild_workspace(token)
    return flask.send_from_directory(workspace, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))