from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Установите ваш API ключ от OpenAI
openai.api_key = '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 '

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Или другая модель чата
        messages=[{"role": "user", "content": user_input}]
    )
    message = response['choices'][0]['message']['content'] if response['choices'] else "No response."
    return jsonify(message=message)

if __name__ == '__main__':
    app.run(debug=False)