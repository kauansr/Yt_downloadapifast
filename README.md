# 🎬 YouTube Downloader – Web App (FastAPI + ReactJS)

This project is a simple **YouTube Downloader website**, featuring a **ReactJS frontend** and a **FastAPI backend**.  
It allows users to input one or more YouTube URLs and download:

- 🎥 Video files (highest available resolution)
- 🎧 Audio files (converted to `.mp3`)

All downloaded files are **temporarily stored on the server** and automatically deleted.

---

## 🌐 About the Project

The frontend is built with **ReactJS**, providing a user-friendly interface to submit YouTube links. The backend is a REST API built with **FastAPI** that processes the downloads and serves the media files.

---

## 🚀 Features

- User-friendly ReactJS frontend for easy URL input
- Supports multiple YouTube URLs per request
- Downloads both videos and audio tracks
- Converts audio streams to `.mp3`
- Temporary file storage with automatic deletion

---

## 🛠️ Tech Stack

- **ReactJS** – frontend UI framework
- **FastAPI** – backend API framework
- **pytubefix** – YouTube video/audio downloader library
- **uvicorn** – ASGI server for FastAPI
- **pytest** – testing framework

---

## 📦 Installation Windows

### 1. Clone the repository

```bash
git clone https://github.com/kauansr/Yt_downloadapifast
cd Yt_downloadapifast
```

### 2. Create and activate a Python Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install backend dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the backend server
```bash
cd app
uvicorn main:app --reload
```

### 5. Setup frontend
```bash
cd frontend
```

### 6. Install frontend dependencies
```bash
npm install
```

### 7. Start the react development server
```bash
npm start
```
