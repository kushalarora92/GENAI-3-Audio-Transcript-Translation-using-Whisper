import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        language = request.form['language']
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            audio_file = open("static/recording.m4a", "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": f"You are a helpful assistant that translates text from English to ${language}."},
                          {"role": "user", "content": transcript.text}],
                temperature=0,
                max_tokens=256,
            )
            
            return response.choices[0].message.content
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)