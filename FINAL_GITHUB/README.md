# Carba Lens - Carbon Emissions Tracking System

A full-stack web application for tracking and visualizing carbon emissions data from materials and transportation sources.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Verifying the Setup](#verifying-the-setup)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** and **npm** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads)

Verify your installations:
```bash
python --version
node --version
npm --version
git --version
```

## 📁 Project Structure

```
FINAL_GITHUB/
├── backend/              # Flask API server
│   ├── api_server.py    # Main Flask application
│   ├── ranking_system.py # Emissions ranking logic
│   ├── requirements.txt  # Python dependencies
│   └── *.json           # Data files
├── frontend/            # React + Vite web app
│   ├── src/            # React components
│   ├── package.json    # Node dependencies
│   └── vite.config.js  # Vite configuration
└── scope3-scraper/     # Azure Function for data scraping
```

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/Punit-154/HACKCELERATE-Project-Stardust-Crusaders.git
cd HACKCELERATE-Project-Stardust-Crusaders/FINAL_GITHUB
```

### Step 2: Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify backend files exist:**
   - Check that `api_server.py` and `ranking_system.py` are present
   - Ensure JSON data files (`materials_emissions.json`, `transport_emissions.json`) exist

### Step 3: Frontend Setup

1. **Open a new terminal and navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

   > ⏱️ This may take 2-5 minutes depending on your internet connection

3. **Verify installation:**
   ```bash
   npm list --depth=0
   ```

## ▶️ Running the Application

### Start the Backend Server

1. **In the backend terminal (with virtual environment activated):**
   ```bash
   python api_server.py
   ```

2. **Expected output:**
   ```
   ==================================================
   Simple Ranking Server Started
   Dashboard available at: http://localhost:5000
   NOTE: Auto-updates disabled. Data is loaded from existing CSVs/JSON.
   ==================================================
   
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   ```

3. **Backend is now running on:** `http://localhost:5000`

### Start the Frontend Development Server

1. **In the frontend terminal:**
   ```bash
   npm run dev
   ```

2. **Expected output:**
   ```
   VITE v7.x.x  ready in xxx ms

   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

3. **Frontend is now running on:** `http://localhost:5173`

## ✅ Verifying the Setup

### Quick Verification Steps

#### 1. Test Backend API
Open your browser or use curl to test:

```bash
# Test materials ranking endpoint
curl http://localhost:5000/api/rankings/materials

# Test transport ranking endpoint
curl http://localhost:5000/api/rankings/transport

# Test combined rankings endpoint
curl http://localhost:5000/api/rankings/all
```

**Expected response:**
```json
{
  "status": "success",
  "materials": [...],
  "transport": [...],
  "last_update": "2026-01-31T..."
}
```

#### 2. Test Frontend Application

1. **Open browser:** Navigate to `http://localhost:5173`

2. **Check for these elements:**
   - ✅ "Carba Lens" title (in calligraphic font)
   - ✅ Wavy navigation bar at the top
   - ✅ Dashboard with emissions rankings
   - ✅ Bar charts visualizing data
   - ✅ Materials and Transport sections

3. **Verify data loading:**
   - Rankings should display real data from the backend
   - Charts should render properly
   - No console errors in browser DevTools (F12)

#### 3. Check Network Communication

1. **Open browser DevTools (F12)**
2. **Go to Network tab**
3. **Refresh the page**
4. **Look for successful API calls:**
   - Request to `http://localhost:5000/api/rankings/all`
   - Status: 200 OK
   - Response contains materials and transport data

### Verification Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend dev server running on port 5173
- [ ] API endpoints return valid JSON responses
- [ ] Frontend displays "Carba Lens" branding
- [ ] Emissions data visible in dashboard
- [ ] Bar charts render correctly
- [ ] No errors in browser console
- [ ] No errors in backend terminal

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/rankings/materials` | GET | Get materials emissions ranking |
| `/api/rankings/transport` | GET | Get transport emissions ranking |
| `/api/rankings/all` | GET | Get all rankings (materials + transport) |
| `/api/rankings/refresh` | POST | Manually refresh rankings from CSV files |

### Example API Response

```json
{
  "status": "success",
  "materials": [
    {"rank": 1, "material": "Steel", "emissions": 1234.56},
    {"rank": 2, "material": "Concrete", "emissions": 987.65}
  ],
  "transport": [
    {"rank": 1, "mode": "Air Freight", "emissions": 5678.90},
    {"rank": 2, "mode": "Truck", "emissions": 2345.67}
  ],
  "last_update": "2026-01-31T07:28:00.000000"
}
```

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

**Problem:** Port 5000 already in use
```bash
# Solution: Kill the process using port 5000 or change port in api_server.py
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

**Problem:** No data showing in API responses
```bash
# Solution: Verify JSON data files exist in backend directory
ls backend/*.json

# Or manually refresh rankings
curl -X POST http://localhost:5000/api/rankings/refresh
```

### Frontend Issues

**Problem:** `npm install` fails
```bash
# Solution: Clear npm cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem:** Frontend can't connect to backend (CORS errors)
- Ensure backend is running on port 5000
- Check that `flask-cors` is installed in backend
- Verify frontend is making requests to `http://localhost:5000`

**Problem:** Port 5173 already in use
```bash
# Solution: Kill the process or use a different port
npm run dev -- --port 3000
```

### Data Issues

**Problem:** "No rankings available"
```bash
# Check that CSV/JSON data files exist
cd backend
ls *.json *.csv

# Manually trigger data refresh
curl -X POST http://localhost:5000/api/rankings/refresh
```

## 📊 Features

- **Real-time Emissions Tracking:** Monitor carbon emissions from materials and transportation
- **Visual Dashboard:** Interactive bar charts and rankings
- **RESTful API:** Clean API endpoints for data access
- **Modern UI:** Built with React, Tailwind CSS, and Framer Motion
- **Responsive Design:** Works on desktop and mobile devices

## 🛠️ Technology Stack

**Backend:**
- Flask (Python web framework)
- Flask-CORS (Cross-origin resource sharing)

**Frontend:**
- React 19
- Vite (Build tool)
- Tailwind CSS v4 (Styling)
- Recharts (Data visualization)
- Framer Motion (Animations)

## 📝 License

This project was created for HACKCELERATE by Team Stardust Crusaders.

---

**Need help?** Check the troubleshooting section or open an issue on GitHub.
