import os
import smtplib
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

def get_email(app_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(app_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    email_tag = soup.find("a", href=lambda href: href and "mailto:" in href)
    if email_tag:
        return email_tag["href"].replace("mailto:", "")
    return None

def send_email(to_email, subject, body, sender, auth):
    try:
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, auth)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

@app.route("/send-email", methods=["POST"])
def fetch_and_send_email():
    data = request.json
    url = data.get("url")
    subject = data.get("subject")
    body = data.get("body")
    sender = data.get("sender")
    auth = data.get("auth")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    developer_email = get_email(url)
    if not developer_email:
        return jsonify({"error": "Developer email not found"}), 404
    
    if send_email(developer_email, subject, body, sender, auth):
        return jsonify({"message": "Email sent successfully", "to": developer_email})
    else:
        return jsonify({"error": "Failed to send email"}), 500

@app.route("/send-email-test", methods=["POST"])    
def send_email_test():
    data = request.json
    email = data.get("email")
    subject = data.get("subject")
    body = data.get("body")
    sender = data.get("sender")
    auth = data.get("auth")
    
    if not email:
        return jsonify({"error": "No Email provided"}), 400
    
    if send_email(email, subject, body, sender, auth):
        return jsonify({"message": "Email sent successfully", "to": email})
    else:
        return jsonify({"error": "Failed to send email"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # print(send_email("bozo4cecil@gmail.com", "Test", "This is a test email"))
