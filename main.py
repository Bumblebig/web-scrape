from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

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

@app.route("/get-email", methods=["POST"])
def fetch_email():
    data = request.json  # Get JSON payload
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    email = get_email(url)
    return jsonify({"email": email})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
