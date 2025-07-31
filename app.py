from flask import Flask, render_template, request
import requests
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def get_projects():
    api_url = 'https://api.github.com/users/JeevanC31/repos'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        cards_list = response.json()
    except Exception as e:
        print("Error fetching GitHub repos:", e)
        cards_list = []
    return cards_list

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', message="Bad Request"), 400

@app.errorhandler(404)
def err_404(e):
    return render_template('error.html', message='404 Page Not Found'), 404

@app.route('/')
def main_page():
    return render_template('index.html', title='Jeevan C - Homepage')

@app.route('/home')
def home():
    return render_template('base.html', title='Base')


# Email configuration using environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 'yes']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_info_included = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        reason = request.form.get('reason', '').strip()

        contact_info_included = False
        if 10 <= len(phone) <= 13:
            contact_info_included = True

            # Send email
            msg = Message("New Contact Form Submission",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nReason: {reason}"
            mail.send(msg)

    return render_template('contact.html', contact_status=contact_info_included)


@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

