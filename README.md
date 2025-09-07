# 🚀 Route Genie Service

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green?logo=fastapi)
![OR-Tools](https://img.shields.io/badge/OR--Tools-9.7.0-orange)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

---

## 🌟 Introduction
**Route Genie Service** is a FastAPI-based backend service to calculate **optimized vehicle routes** using **OR-Tools** and **OpenRouteService (ORS)**. It supports shortest path calculation based on:

- Distance 🚗
- Duration ⏱️
- Blended metrics ⚖️

The service is designed for **high accuracy**, **efficient computation**, and **scalable to multiple locations**.

---

## ✨ Features
- Compute the shortest route based on distance, duration, or a blended metric
- Supports returning to the starting location
- Integration with external routing services (e.g., ORS)
- Multiple path calculation strategies:
  - OR-Tools (optimal)
  - Nearest Neighbour (heuristic)
  - TSP (exact for small sets)
- Returns detailed route information:
  - Step distances and durations
  - Ordered path of locations
  - Total distance and duration
- no limit on the number of locations (with performance considerations)
---

## 🏗️ Architecture Diagram
```json

```

## 🛠️ APIs

### 1️⃣ Optimize Route
**POST** `/routes/optimize`  

**Request Example:**
```json
{
  "mode": "car",
  "start": {
    "latitude": 12.9779,
    "longitude": 77.5713,
    "id": "Majestic, Bengaluru"
  },
  "routes": [
    {"latitude": 12.9740, "longitude": 77.6056, "id": "MG Road"},
    {"latitude": 13.0358, "longitude": 77.5970, "id": "Herbal"}
  ]
}
```
**Response Example:**
```json
{
  "route_groups": [
    {
      "shortest_distance": {},
      "shortest_duration": {},
      "shortest_blended": {}
    }
  ],
  "mode": "car",
  "start_location": {}
}
```
### 2️⃣ Health Check
**GET** `/health`  
**Response Example:**
```json
{"status": "ok"}
```

## 🚀 Steps to Run Locally

### 1️⃣ Clone the repository
```bash
    git clone <repository_url>
    cd <project_directory>
```
### 2️⃣ Set up a virtual environment
```bash
    python -m venv .venv
    # Activate the virtual environment
    # macOS/Linux
    source .venv/bin/activate 
    # Windows 
    .venv\Scripts\activate
```
### 3️⃣ Install dependencies
```bash
    pip install --upgrade pip
    pip install -r requirements.txt
```
### 4️⃣ Set up environment variables
Create a `.env` file in the root directory and add required variables:
```env
    ORS_API_KEY=your_openrouteservice_api_key
    LOG_LEVEL=logging_level(e.g., INFO, DEBUG)
```
### 5️⃣ Run the FastAPI server
```bash
    uvicorn app.main:app --reload
```
### 6️⃣ Access the API
- localhost url: `http://localhost:8000/`
- swagger docs: `http://localhost:8000/docs`
- redoc docs: `http://localhost:8000/redoc`

## 📝 Notes
- 🌍 Create an account on [openRouteService](https://openrouteservice.org)
- 🔑 Generate your free API Key
---
## 📜 License
This project is licensed under the [MIT License](./LICENSE)