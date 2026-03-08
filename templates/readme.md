.

📁 Mini Drive – Secure Cloud File Storage Web App

Mini Drive is a Flask-based cloud file storage web application that allows users to securely upload, download, and manage files with private or public access control.
It provides a modern dashboard experience with drag-and-drop uploads, progress indicators, and authentication.

🚀 Features

✅ User Authentication (Register / Login / Logout)
✅ Secure File Upload & Download
✅ Public / Private File Access Control
✅ Drag & Drop File Upload
✅ Real-time Upload Progress Bar
✅ Button Loading Spinner
✅ Modern Responsive Dashboard UI
✅ File Management System

🖼️ Application Screens

Login Page with Background Image

Register Page with Cloud Storage Theme

Dashboard with Upload Area

File List with Download Options

🛠️ Tech Stack

Backend

Python

Flask

SQLite

Flask-Login

Frontend

HTML5

CSS3

JavaScript

Other Tools

Git

GitHub

📂 Project Structure
MiniDrive/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
└── uploads/
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/minidrive.git
cd minidrive
2️⃣ Create virtual environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the application
python app.py
5️⃣ Open in browser
http://127.0.0.1:5000
📊 Key Functionalities
🔐 Authentication

Users can register and securely log in to their account.

📤 File Upload

Users can upload files via drag-and-drop or manual selection.

📥 File Download

Uploaded files can be downloaded anytime from the dashboard.

📊 Upload Progress

A real-time progress bar displays upload status.

🔒 Access Control

Files can be marked Public or Private.

🎯 Future Improvements

File preview (images / PDFs)

File delete option

Multiple file upload

Shareable public links

Cloud storage integration (AWS S3 / Google Cloud)

👨‍💻 Author

Your Name

GitHub:
https://github.com/yourusername

⭐ If you like this project, give it a star on GitHub!