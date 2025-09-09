# Flaskify  

A Flask-based web application that provides user authentication, profile management, and a learning dashboard with lessons and progress tracking.
Flaskify enables users to be able to learn Flask, through Flask and built with Flask.

## Features  

- 🔑 **User Authentication**  
  - Sign up, log in, and log out securely with hashed passwords  
  - Session management via Flask-Login  

- 👤 **User Profiles**  
  - Update personal information (name, email, bio, aspiring job)  
  - Randomly generated profile picture
  - Make and view other people's community posts

- 📚 **Learning Dashboard**  
  - Accordion-style lesson modules  
  - Interactive checkboxes to track lesson completion  
  - Dynamic progress bar showing percentage of completed lessons  

- ⚡ **Flask Extensions**  
  - Flask-WTF for forms and validation  
  - Flask-Migrate for database migrations  
  - Flask-Login for user session handling  
  - SQLAlchemy ORM with SQLite database  

## Tech Stack  

- **Backend:** Flask (Python)  
- **Database:** SQLite (via SQLAlchemy ORM)  
- **Frontend:** Bootstrap 5, Jinja2 templates  
- **Auth:** Flask-Login with password hashing (Werkzeug)  

## Getting Started  

### Prerequisites  
Make sure you have **Python 3.9+** installed.  

### Installation  

```bash
# Clone the repository
git clone https://github.com/your-username/flaskify.git
cd flaskify

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Run the app
flask run
