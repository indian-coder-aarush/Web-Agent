import os
import dotenv
import google.generativeai as genai
import ast
import Tools

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# Your conversation as dicts
messages = [
    {"role": "system", "content": "You are a code editor AI agent that makes frontends for apps."
                                  "You will reply in the following format only."
                                  "{"
                                  "'tool_used' : '<the tool you will use>',"
                                  "'file_address': '<optional for run_command, but neccessary if you want to specify file address you want to use.>'"
                                  "'content': '<the code or command>',"
                                  "'reason': '<why did you do that step>',"
                                  "'memory_add': '<what to add to the memory that can help you accesses it later>'"
                                  "}"
                                  "The tools that are available to you are "
                                  "write_file: lets you rewrite the whole file or write something in it if it is blank"
                                  "read_file: get the contents of a file"
                                  "run_command: run a terminal command"
                                  "Terminate: once the app is created you can terminate yourself."
                                  "Remember that you dont have to put anything extra like explainations, md files. "
                                  "give only the format i mentioned to u amd mo things like ```json also"},
    {"role": "user", "content": "Make a todo app using HTML, CSS, and JavaScript in C:/Users/rohit/OneDrive/Documents/GitHub/Web-Agent"}
]

# Convert dicts into a single prompt
def dicts_to_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        prompt += f"{role}: {msg['content']}\n"
    return prompt

terminate = False

model_response = model.generate_content(dicts_to_prompt(messages))

while not terminate:
    response_text = model_response.text if hasattr(model_response, "text") else \
    model_response.candidates[0].content.parts[0].text
    response = ast.literal_eval(response_text)
    print(response["tool_used"])
    if response["tool_used"] == "terminate":
        terminate = True
    elif response["tool_used"] == "read_file":
        file_content = Tools.read_file(response["file_address"])
        messages.append({"role": response["file_address"], "content": file_content})
    elif response["tool_used"] == "run_command":
        command = response["content"]
        output = Tools.safe_run_command(command)
        messages.append({"role": response["file_address"], "content": output})
        print(response["content"])
    elif response["tool_used"] == "write_file":
        Tools.write_file(response["file_address"],response["content"])
        print(response["content"])
    model_response = model.generate_content(dicts_to_prompt(messages))

