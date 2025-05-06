# Incident Management System

A Flask-based web application for logging, tracking, and resolving infrastructure and application incidents with role-based access. The system provides a user-friendly interface, REST APIs, email notifications, and is containerized using Docker for easy deployment.

## Features
- **Role-Based Access**:
  - **Users**: Create and view their own incidents.
  - **Admins/Technicians**: Update incident status (Open, In Progress, Resolved).
- **REST APIs**: Create, retrieve, and update incidents securely with JWT authentication.
- **Email Notifications**: Sends email alerts to admins when new incidents are created.
- **SQLite Database**: Lightweight storage for users and incidents.
- **Professional UI**: Colorful, formal interface using Bootstrap and Roboto font.
- **Dockerized**: Packaged as a Docker image for consistent deployment.
- **Version Control**: Source code hosted on GitHub with Git for tracking changes.

## Project Structure
```
incident-management/
├── templates/
│   ├── index.html        # Login and registration page
│   └── dashboard.html    # Incident management dashboard
├── docs/
│   ├── login.png        # Login page screenshot
│   └── dashboard.png    # Dashboard screenshot
├── app.py               # Main Flask application
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## Prerequisites
- Python 3.9+
- Docker
- Git
- Gmail account (for email notifications)

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/incident-management.git
   cd incident-management
   ```
   Replace `yourusername` with your GitHub username.

2. **Configure Email Notifications**:
   - Open `app.py` and update the following:
     ```python
     app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
     app.config['MAIL_PASSWORD'] = 'your-app-password'
     ```
   - Generate a Gmail App Password:
     - Enable 2-Factor Authentication in your Google Account.
     - Go to Google Account > Security > App Passwords.
     - Create an App Password for "Mail" and copy the 16-character code.
   - Update the admin email in the `/incidents` POST route:
     ```python
     recipients=['admin@example.com']
     ```
     Replace with the admin’s email address.

3. **Install Dependencies (Optional for Local Testing)**:
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Build the Docker Image**:
   ```bash
   docker build -t incident-management .
   ```

5. **Run the Docker Container**:
   ```bash
   docker run -p 5000:5000 incident-management
   ```

6. **Access the Application**:
   - Open a browser and navigate to `http://localhost:5000`.

## Usage
- **Login Page**: Register a new account or log in with existing credentials.
- **Dashboard**:
  - **Users**: Create new incidents with a title, description, and priority (Low, Medium, High).
  - **Admins/Technicians**: Update incident status via a dropdown in the incident table.
- **Email Notifications**: Admins receive an email when a new incident is created.

### Sample Credentials
- **Admin**: Username: `admin`, Password: `admin123`
- **Technician**: Username: `tech`, Password: `tech123`
- **User**: Username: `user`, Password: `user123`

## Demo
- **Screenshots**:
  - Login Page: [docs/login.png](docs/login.png)
  - Dashboard: [docs/dashboard.png](docs/dashboard.png)

## Sample Issues
- **Incident 1**:
  - Title: Server Down
  - Description: Main server offline
  - Priority: High
  - Status: Resolved
- **Incident 2**:
  - Title: App Crash
  - Description: Mobile app crashing on login
  - Priority: Medium
  - Status: In Progress

## Development
- **Run Locally** (without Docker):
  ```bash
  python app.py
  ```
- **Database**: SQLite (`incidents.db`) is created automatically on first run.
- **Security**:
  - Replace `SECRET_KEY` in `app.py` with a secure random string in production.
  - Use environment variables for sensitive data (e.g., email credentials).
- **Enhancements**:
  - Add incident comments or file attachments.
  - Implement pagination for large incident lists.
  - Add user management for admins.

## Troubleshooting
- **Email Issues**: Verify Gmail App Password and SMTP settings in `app.py`.
- **Database Issues**: Delete `incidents.db` and rerun `app.py` to reinitialize.
- **Docker Issues**: Ensure port 5000 is free and Docker is running.
- **Dependency Errors**: Ensure `requirements.txt` matches the provided versions.

## License
This project is licensed under the MIT License.
