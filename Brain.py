from openai import OpenAI
import flask
import os
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key)

