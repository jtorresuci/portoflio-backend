import os
from flask import Flask, request, jsonify
import smtplib
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/submit": {"origins": "http://localhost:3000"}})

@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        response = app.response_class(
            status=200,
            mimetype='application/json',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )
        return response

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Send email
    from_email = 'jtorresuci@gmail.com'
    to_email = 'jtorresuci@gmail.com'
    subject = 'New Contact Form Submission'
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
    message = f'Subject: {subject}\n\n{body}'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, os.environ['GMAIL_PASSWORD'])
        server.sendmail(from_email, to_email, message)
        server.quit()
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
