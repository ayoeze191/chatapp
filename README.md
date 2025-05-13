# 💬 Django Realtime Chat App

A real-time chat application built with **Django**, **Django Channels**, **Redis**, and styled using **TailwindCSS**. This project demonstrates how to implement websocket-based messaging in Django for instant communication between users.

---

## 🚀 Features

- 🔐 User Authentication (Register, Login, Logout)
- 💬 Real-Time Messaging with WebSockets
- 🌐 Channel Layers powered by Redis
- 📱 Responsive UI with TailwindCSS
- 🗂️ Chat Rooms / Private Chats (optional)
- 📥 Message persistence using Django ORM

---

## 🛠️ Tech Stack

| Layer       | Technology           |
|-------------|----------------------|
| Backend     | Django, Django Channels |
| Frontend    | TailwindCSS, HTML, JS |
| Real-time   | WebSockets, Redis     |
| Database    | SQLite                |
| Auth        | Django Auth           |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/django-chat-app.git
cd django-chat-app
```
### 2. activate virtual environment 
```python -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```pip install -r requirements.txt```
### 4 Run redis server
```On Linux
sudo service redis-server start
# Or using Docker
docker run -p 6379:6379 redis```
