import os
import dotenv
import google.generativeai as genai
import ast
import Tools
from flask_app import send_to_frontend

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
                                  "'memory': '<what to add to the memory that can help you accesses it later>'"
                                  "}"
                                  "The tools that are available to you are "
                                  "write_file: lets you rewrite the whole file or write something in it if it is blank"
                                  "read_file: get the contents of a file"
                                  "run_command: run a terminal command"
                                  "Terminate: once the app is created you can terminate yourself."
                                  "Remember that you dont have to put anything extra like explainations, md files. "
                                  "Always return valid JSON:"
                                    "- Use double quotes for keys and string values"
                                    "- Escape newlines and quotes inside content"
                                    "- Example:"
                                    "{"
                                        '"tool_used": "write_file",'
                                        '"file_address": "script.js",'
                                        '"content": "document.addEventListener(\"DOMContentLoaded\", () => { ... });"'
                                    "}"
                                    "- NEVER write files repeatedly once they exist and are complete. "
                                  "You can see the completed files in the memory\n"
                                    "- If you are unsure or have no next step, TERMINATE."
                                    "- If the user asks to edit anything, first READ the file then edit it."
                                  "give only the format i mentioned to u amd mo things like ```json also. in content while writing code "
                                  "remember to terminate after your project is done and after writing every line of code "
                                  "go to a newline"
                            },
]

# Convert dicts into a single prompt
def dicts_to_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        prompt += f"{role}: {msg['content']}\n"
    return prompt

def execute(prompt):
    terminate = False
    messages.append({"role":"user", "content": prompt})
    model_response = model.generate_content(dicts_to_prompt(messages))
    while not terminate:
        response_text = model_response.text if hasattr(model_response, "text") else \
        model_response.candidates[0].content.parts[0].text
        response = ast.literal_eval(response_text)
        messages.append(response)
        print(messages)
        if response["tool_used"] == "Terminate":
            terminate = True
        elif response["tool_used"] == "read_file":
            file_content = Tools.read_file(response["file_address"])
            messages.append({"role": response["file_address"], "content": file_content})
        elif response["tool_used"] == "run_command":
            command = response["content"]
            output = Tools.safe_run_command(command)
            messages.append({"role": "terminal", "content": output})
        elif response["tool_used"] == "write_file":
            Tools.write_file(response["file_address"], response["content"])
            messages.append({
                "role": "system",
                "content": f"File '{response['file_address']}' has been successfully written. Do not rewrite it again unless there is a major error. Check if other files are needed or terminate."
            })
        model_response = model.generate_content(dicts_to_prompt(messages))