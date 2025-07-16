from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_default_secret_key")

# ✅ Project Data
projects = [
    {
        "id": 1,
        "title": "Amazon Sales Dashboard",
        "description": "Developed an interactive Tableau dashboard for analysing Amazon sales data...",
        "image": "dashboard.png",
        "technologies": ["Tableau Prep", "Tableau Desktop", "Data Visualization", "Data Manipulation"],
        "categories": ["data"],
        "github_url": "https://github.com/Akanchakumarisah/Amazon-Sales-Analysis",
        "live_url": "https://github.com/Akanchakumarisah/Amazon-Sales-Analysis/blob/main/Screenshot%202024-11-17%20143614.png"
    },
    {
        "id": 2,
        "title": "Mall Customer Segmentation",
        "description": "Segmented mall customers based on spending patterns and demographics...",
        "image": "Customer-Segmentation.png",
        "technologies": ["Python", "NumPy", "Matplotlib", "Seaborn", "Power BI", "Machine Learning"],
        "categories": ["data"],
        "github_url": "https://github.com/Akanchakumarisah/Mall-Customer-Segmentation-Project",
        "live_url": "https://github.com/Akanchakumarisah/Mall-Customer-Segmentation-Project/blob/main/Dashboard/Mall-Customer%20Dashboard.pbix"
    },
    {
        "id": 3,
        "title": "Bike Sales Dashboard",
        "description": "Developed an interactive Power BI dashboard to analyse bike sales data...",
        "image": "Bike Sales Dashboard.png",
        "technologies": ["Power BI", "Data Analysis", "Data Visualization"],
        "categories": ["data"],
        "github_url": "https://github.com/Akanchakumarisah/Bike-Sales-Dashboard",
        "live_url": "https://github.com/Akanchakumarisah/Bike-Sales-Dashboard/blob/main/Bike%20Sales%20Dashboard.png"
    },
    {
        "id": 4,
        "title": "Portfolio Website",
        "description": "Developed a responsive personal portfolio website to showcase my projects...",
        "image": "portfolio.png",
        "technologies": ["HTML5", "CSS3", "JavaScript"],
        "categories": ["web"],
        "github_url": "https://github.com/Akanchakumarisah/PortfolioWebsiteAkancha",
        "live_url": "https://akanchakumarisah.github.io/PortfolioWebsiteAkancha/"
    }
]

# ✅ Skills Data
skills = {
    'languages': [
        {'name': 'Python', 'icon': 'fa-brands fa-python'},
        {'name': 'JavaScript', 'icon': 'fa-brands fa-js'},
        {'name': 'Java', 'icon': 'fa-brands fa-java'},
        {'name': 'C++', 'icon': 'fa-solid fa-file-code'}
    ],
    'web_tech': [
        {'name': 'HTML', 'icon': 'fa-brands fa-html5'},
        {'name': 'CSS', 'icon': 'fa-brands fa-css3-alt'},
        {'name': 'Tailwind CSS', 'icon': 'fa-solid fa-paintbrush'},
        {'name': 'Flask', 'icon': 'fa-solid fa-flask'},
        {'name': 'React', 'icon': 'fa-brands fa-react'}
    ],
    'databases': [
        {'name': 'MySQL', 'icon': 'fa-solid fa-database'},
        {'name': 'SQL', 'icon': 'fa-solid fa-database'},
        {'name': 'Hadoop', 'icon': 'fa-solid fa-database'},
        {'name': 'Hbase', 'icon': 'fa-solid fa-database'},
        {'name': 'Hive', 'icon': 'fa-solid fa-database'}
    ],
    'tools': [
        {'name': 'Git', 'icon': 'fa-brands fa-git-alt'},
        {'name': 'VS Code', 'icon': 'fa-solid fa-code'},
        {'name': 'Tableau', 'icon': 'fa-solid fa-chart-bar'},
        {'name': 'Excel', 'icon': 'fa-solid fa-file-excel'},
        {'name': 'Google Colab', 'icon': 'fa-brands fa-google'}
    ]
}

# ✅ Education Data
education = [
    {
        'degree': 'Bachelor of Computer Science And Engineering',
        'institution': 'Lovely Professional University',
        'year': '2022-2026',
        'gpa': '7.17'
    },
    {
        'degree': 'Higher Secondary Education',
        'institution': 'Om National Academy',
        'year': '2019-2021',
        'gpa': '88.8%'
    }
]

# ✅ Google Sheets Setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

sheet = None
credentials_json = os.getenv("GOOGLE_CREDENTIALS")

if credentials_json:
    try:
        creds_dict = json.loads(credentials_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("sheet").sheet1  # replace with your actual Google Sheet name
    except Exception as e:
        print(f"❌ Google Sheets setup failed: {e}")
else:
    print("❌ GOOGLE_CREDENTIALS environment variable not found.")

# ✅ Flask Routes
@app.route('/')
def home():
    return render_template('index.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html', skills=skills, education=education)

@app.route('/projects')
def projects_page():
    return render_template('projects.html', projects=projects)

@app.route('/experience')
def experience():
    experiences = []  # Add your experience data if needed
    return render_template('experience.html', experiences=experiences)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        os.makedirs('data', exist_ok=True)
        try:
            with open('data/contact_submissions.txt', 'a', encoding='utf-8') as f:
                f.write(f"{data}\n")
        except Exception as e:
            print(f"❌ Error saving locally: {e}")

        if sheet:
            try:
                row = [data['name'], data['email'], data['subject'], data['message'], data['timestamp']]
                sheet.append_row(row)
                flash('Thank you! Message saved to Google Sheets.', 'success')
            except Exception as e:
                print(f"❌ Google Sheets write error: {e}")
                flash('Saved locally. Sheets failed.', 'warning')
        else:
            flash('Message saved locally only. Google Sheets not connected.', 'warning')

        return redirect(url_for('contact'))

    return render_template('contact.html')

# ✅ Run app (only for local dev; use gunicorn for prod)
if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
