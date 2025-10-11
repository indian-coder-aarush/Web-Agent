import os
import dotenv
import google.generativeai as genai

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# Your conversation as dicts
messages = [
    {"role": "system", "content": "You are a code editor AI agent that makes frontends for apps."
                                  "You will reply in the following format only."
                                  "{"
                                  "tool_used : <the tool you will use>,"
                                  "file_address: <optional for run_command, but neccessary if you want to specify file address you want to use.>"
                                  "content: <the code or command>,"
                                  "reason: <why did you do that step>,"
                                  "memory_add: <what to add to the memory that can help you accesses it later>"
                                  "}"
                                  "The tools that are available to you are "
                                  "write_file: lets you rewrite the whole file or write something in it if it is blank"
                                  "read_file: get the contents of a file"
                                  "run_command: run a terminal command"
                                  "Terminate: once the app is created you can terminate yourself"
                                  "ask_user: ask something to the user"
                                  "Remember that you dont have to put anything extra like explainations, md files. "
                                  "give only the format i mentioned to u"},
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

response = model.generate_content(dicts_to_prompt(messages))
