from flask import Flask, render_template, request, send_file
from core.encryptor import encrypt_file, decrypt_file
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        password = request.form['password']
        action = request.form['action']  # 'encrypt' or 'decrypt'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            if action == 'encrypt':
                out_file = encrypt_file(filepath, password)
            else:
                out_file = decrypt_file(filepath, password)
        except Exception as e:
            return f"Error: {str(e)}"
        
        return send_file(out_file, as_attachment=True)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)