from flask import Flask, render_template, request
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY") 
openai.organization = os.getenv("OPENAI_ORGANIZATION") 

conversation=[{"role": "system", "content": "You are a helpful assistant."}]

app = Flask(__name__)

#define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def completion_response():
    user_input = request.args.get('msg')   
    conversation.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation,
        temperature=1,
        max_tokens=250,
        top_p=0.9
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    return str(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    app.run()