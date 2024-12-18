from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

messages = []
prompt = {'role': 'system', 'content': """
You are a quiz. Present the user with a multiple-choice question to practice for a python interview,
they have to respond by typing a, b, c, or d. Wait until the user responds before presenting a new question.
"""}
messages.append(prompt)

while True:
    # send the api call
    response = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)

    # share response in console
    print(response.choices[0].message.content)

    # expanding the conversation
    messages.append(response.choices[0].message)

    messages.append(prompt)

    # Capture user input
    user_input = input('Enter a prompt: ')

    # quit loop
    if user_input == 'end' or user_input == 'quit' or user_input == 'q':
        break

    # prompt preparation
    messages.append({'role': 'user', 'content': user_input})