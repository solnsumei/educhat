import os
import gradio as gr
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

messages = []

prompt = {'role': 'system', 'content': """
You are a quiz. Present the user with a multiple-choice question to practice for a python interview,
they have to respond by typing a, b, c, or d. Wait until the user responds before presenting a new question
or the answer to the previous question. Keep track of the correct answer option for the question provided and
present the user with another question after they answer and also tell them if their answer was correct or wrong.
"""}

messages.append(prompt)


def respond(new_message: str):
    # if there is no history attach system prompt
    # if len(history) == 0:
    #     history.append(prompt)

    # add the user input to the messages
    messages.append({'role': 'user', 'content': new_message})

    response = client.chat.completions.create(model='llama3-8b-8192', messages=messages)
    # share response in console
    assistant_message = response.choices[0].message
    messages.append({'role': "assistant", 'content': f"{assistant_message.content}"})

    return messages, ""


with gr.Blocks(fill_height=True) as my_bot:
    chatbot = gr.Chatbot(type='messages', scale=1, label="Python Quiz")
    user_input = gr.Text(scale=0, label="")

    user_input.submit(respond, [user_input], [chatbot, user_input])


my_bot.launch()
