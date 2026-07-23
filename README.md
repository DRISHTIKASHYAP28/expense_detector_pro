# 💰 Expense Detector Pro

A Production-Ready Expense Management Web Application built with Flask, SQLAlchemy, Bootstrap, and Chart.js.
Secure • Responsive • Layered Architecture • Analytics Dashboard

---

## 🚀 Live Demo

🌐 https://expense-detector-pro.onrender.com

---

# 📖 Overview

Expense Detector Pro is a full-stack web application that helps users securely manage their daily expenses, monitor spending habits, and visualize financial insights through an interactive dashboard.

The project follows a **Layered Architecture (Routes → Services → Repository → Database)** to keep the code modular, maintainable, and scalable.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login & Logout
- Password Hashing
- Session Management

---

## 💵 Expense Management

- Add Expenses
- Edit Expenses
- Delete Expenses
- Expense History
- Category-wise Expense Tracking

---

## 📊 Analytics Dashboard

- Expense Summary
- Interactive Charts
- Monthly Overview
- Category-wise Analysis

---

## 🛡 Security

- Environment Variables
- Secure Authentication
- Error Handling
- Logging

---

## 📁 Project Structure

```
expense_detector_pro
│
├── models/
├── repositories/
├── routes/
├── services/
├── static/
├── templates/
├── tests/
├── utils/
│
├── app.py
├── config.py
├── logging_config.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

# 🏗 Architecture

```
                User
                  │
                  ▼
            Flask Routes
                  │
                  ▼
           Service Layer
                  │
                  ▼
        Repository Layer
                  │
                  ▼
            SQLAlchemy ORM
                  │
                  ▼
        SQLite / PostgreSQL
```

The application follows a layered architecture to separate presentation, business logic, and data access. This improves readability, testing, and maintainability.

---

# 🛠 Tech Stack

## Backend

- Python
- Flask
- SQLAlchemy

## Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript
- Chart.js

## Database

- SQLite
- PostgreSQL (Production Ready)

## Deployment

- Render

## Version Control

- Git
- GitHub

---

# 📸 Screenshots

> Add screenshots inside the `screenshots` folder.

### Login Page

<img width="1920" height="1032" alt="Screenshot 2026-07-23 175627" src="https://github.com/user-attachments/assets/1afcbee7-196f-4fdf-bb98-5297afb663be" />


---

### Dashboard

<img width="1920" height="1032" alt="Screenshot 2026-07-23 183210" src="https://github.com/user-attachments/assets/295d2a52-b3e5-4086-a51d-2c6a17747020" />


---

### Add Expense

<img width="1920" height="1032" alt="Screenshot 2026-07-23 183405" src="https://github.com/user-attachments/assets/0fb3f1fe-0aaf-4c99-b0a9-0bae76f0f8e8" />

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/DRISHTIKASHYAP28/expense_detector_pro.git
```

## Navigate into Project

```bash
cd expense_detector_pro
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///database/expense.db
LOG_LEVEL=DEBUG
```

## Run Application

```bash
python app.py
```

---

# 📚 Key Learnings

During this project, I gained hands-on experience with:

- Layered Software Architecture
- Repository Pattern
- Service Layer Design
- Flask Authentication
- SQLAlchemy ORM
- Session Management
- Logging
- Error Handling
- Environment Variable Management
- Deploying Flask Applications on Render

---

# 🚀 Future Enhancements

- Google OAuth Login
- Password Reset
- Email Verification
- Docker Support
- REST API
- Swagger Documentation
- PostgreSQL Production Database
- Export Reports (PDF & CSV)
- Monthly Budget Planning
- AI-Based Expense Insights

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

If you'd like to contribute:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 👩‍💻 Author

**Drishti Kashyap**

- GitHub: https://github.com/DRISHTIKASHYAP28

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub!

It motivates me to build more open-source projects.

---

# 📄 License

This project is licensed under the MIT License.
