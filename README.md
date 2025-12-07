# Flask Contact Manager

A simple **Contact Manager Web Application** built using **Flask**.  
It allows users to **add, view, update, and delete contacts** stored in a db.

## Features
- Add new contacts (name, phone, email)
- View all saved contacts
- Update existing contacts
- Delete contacts
- Simple file-based storage (`contacts.db`)
- User-friendly interface with HTML templates

## Technologies
- Python 3.x
- Flask
- HTML/CSS
- Bootstrap (optional)
- Git for version control

## Project Structure
## Project Structure
contact_app/
├── app.py
├── contacts.db
├── requirements.txt
├── templates/
│ ├── base.html
│ └── index.html
├── static/
│ └── style.css
└── README.md

#Installation command
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
