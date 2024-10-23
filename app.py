from flask import Flask, render_template, request, session
from chatbot import get_bot_response
import os

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = get_bot_response(user_input)
        return render_template('index.html', response=response)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
