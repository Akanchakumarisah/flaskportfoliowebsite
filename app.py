from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Configure Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet (replace with your sheet name)
try:
    sheet = client.open("sheet").sheet1
except Exception as e:
    print(f"Error connecting to Google Sheet: {str(e)}")
    sheet = None

# Projects data
projects = [
    {
        "id": 1,
        "title": "Amazon Sales Dashboard",
        "description": "Developed an interactive Tableau dashboard for analysing Amazon sales data, enabling businesses to track revenue, order trends, and customer behaviour while providing real-time insights into sales performance, top-selling products, and seasonal trends.",
        "image": "dashboard.png",
        "technologies": ["Tableau Prep", "Tableau Desktop", "Data Visualization", "Data Manipulation"],
        "categories": ["data"],
        "github_url": "https://github.com/Akanchakumarisah/Amazon-Sales-Analysis",
        "live_url":"https://github.com/Akanchakumarisah/Amazon-Sales-Analysis/blob/main/Screenshot%202024-11-17%20143614.png"
    },
    {
        "id": 2,
        "title": "Mall Customer Segmentation",
        "description": "Segmented mall customers based on spending patterns and demographics to enable targeted marketing strategies. Performed clustering analysis to identify distinct customer groups.",
        "image": "Customer-Segmentation.png",
        "technologies": ["Python", "NumPy", "Matplotlib", "Seaborn", "Power BI", "Machine Learning"],
        "categories": ["data"],
        "github_url": "https://github.com/Akanchakumarisah/Mall-Customer-Segmentation-Project",
        "live_url": "https://github.com/Akanchakumarisah/Mall-Customer-Segmentation-Project/blob/main/Dashboard/Mall-Customer%20Dashboard.pbix"
    },
    {
        "id": 3,
        "title": "Bike Sales Dashboard",
        "description": "Developed an interactive Power BI dashboard to analyse bike sales data and provide actionable insights including revenue, customer demographics, and purchasing trends.",
        "image": "Bike Sales Dashboard.png",
        "technologies": ["Power BI", "Data Analysis", "Data Visualization"],
        "categories": ["data"],
        "github_url": "https://github.com/Akanchakumarisah/Bike-Sales-Dashboard",
        "live_url":"https://github.com/Akanchakumarisah/Bike-Sales-Dashboard/blob/main/Bike%20Sales%20Dashboard.png"
    },
    {
    "id": 4,
    "title": "Portfolio Website",
    "description": "Developed a responsive personal portfolio website to showcase my projects and skills. Built with modern web technologies to demonstrate front-end development capabilities.",
    "image": "portfolio.png",
    "technologies": ["HTML5", "CSS3", "JavaScript"],
    "categories": ["web"],
    "github_url":"https://github.com/Akanchakumarisah/PortfolioWebsiteAkancha",
    "live_url": "https://akanchakumarisah.github.io/PortfolioWebsiteAkancha/"
}
]

# Skills and education data
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
    # If you have experience data, add it here
    experiences = []  # Placeholder - add your experience data
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
        
        print(f"New contact form submission: {data}")
        
        # Save to local file
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/contact_submissions.txt', 'a', encoding='utf-8') as f:
                f.write(f"{data}\n")
        except IOError as e:
            print(f"Error writing contact submission to file: {str(e)}")
        
        # Save to Google Sheets
        if sheet:
            try:
                row = [data['name'], data['email'], data['subject'], data['message'], data['timestamp']]
                sheet.append_row(row)
                flash('Thank you for your message! It has been saved successfully.', 'success')
            except Exception as e:
                print(f"Error writing to Google Sheet: {str(e)}")
                flash('Your message was saved locally but failed to save to Google Sheets.', 'warning')
        else:
            flash('Your message was saved locally but Google Sheets connection is not available.', 'warning')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)