from flask import Flask, render_template, request
import tiktoken
import json  

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def tokenizer_response():


    tokenizer_value = request.args.get('tokenizer')  # Get the tokenizer value from the request
    tokenizer = tiktoken.get_encoding(tokenizer_value)  # Use the tokenizer value when getting the tokenizer
    count = 0
    token_list = []
    user_input= request.args.get('msg')   
    encode = tokenizer.encode(user_input)
    decode = tokenizer.decode_tokens_bytes(encode)

    for token in decode:
        try:
            token_list.append(token.decode())
        except UnicodeDecodeError:
            token_list.append("�")  # Replace the token with the Unicode replacement character

    character_count = sum(len(i) for i in token_list)
    length = len(encode)

    # Convert token_list items to strings surrounded by single quotes
    quoted_token_list = ["'{}'".format(token) for token in token_list]

    # Create a dictionary containing the desired values
    response_data = {
        "token_list": quoted_token_list,
        "encode": encode,
        "length": length,
        "character_count": character_count
    }

    # Convert the dictionary to a JSON string using json.dumps()
    return json.dumps(response_data)



if __name__ == "__main__":
    app.run()