# Sun Smart Platform

Sun Smart UV protection awareness platform.

## Prerequisites

- **Python 3** (for backend). Check with `python --version` or `py --version` (Windows).
- **Node.js** (v20+ or v22+) and **npm** (for frontend). Check with `node --version` and `npm --version`.

## Running locally

Run the backend and frontend in **separate terminals**.

The current implementation focuses on:
- **Epic 1 – Track UV Levels**: fetch live UV data from Open-Meteo, classify risk using WHO/Australian UV ranges, show colour-coded risk and plain-language alerts.
- **Database-backed location search**: postcode/suburb lookup from PostgreSQL, used by the homepage search bar to fetch UV for a selected location.

### Backend (Flask)

#### PostgreSQL setup

1. Install PostgreSQL locally (for example via Homebrew on macOS) and ensure the PostgreSQL **server is running**.
2. Create a database user and database, e.g.:

   ```sql
   CREATE DATABASE uvibe;
   CREATE USER uvibe_user WITH PASSWORD 'choose-a-strong-password';
   GRANT ALL PRIVILEGES ON DATABASE uvibe TO uvibe_user;
   ```

3. Set the following environment variables (for your shell or in a backend `.env` file):

   ```bash
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_NAME=uvibe
   export DB_USER=uvibe_user
   export DB_PASSWORD=your_password_here
   ```

4. From the `backend/` folder, initialise the schema and import the prepared datasets:

   ```bash
   cd backend
   # create tables
   python -m database.init_db

   # import locations and UV risk levels
   python -m database.import_datasets
   ```

   These commands create the `location`, `uv_risk_level` and optional awareness tables,
   and load `database/australian_postcodes_cleaned.csv` and `database/uv_risk_levels.csv`.

#### Windows (Command Prompt or PowerShell)

1. Open a terminal in the project folder, then:

   ```cmd
   cd backend
   python -m venv venv
   ```
   If `python` is not found, try `py -m venv venv` instead.

2. Activate the virtual environment:

   - **Command Prompt:** `venv\Scripts\activate.bat`
   - **PowerShell:** `venv\Scripts\Activate.ps1`  
     (If you get an execution policy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.)

3. Install dependencies and start the server:

   ```cmd
   pip install -r requirements.txt
   python app.py
   ```

#### macOS / Linux

1. Open a terminal in the project folder, then:

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies and start the server:

   ```bash
   pip install -r requirements.txt
   python app.py
   ```

#### All platforms

The API runs at **http://localhost:5000**. Test: [http://localhost:5000/api/health](http://localhost:5000/api/health).

> **Note (macOS):** Port 5000 is often used by AirPlay Receiver. If you see "Address already in use", either turn off AirPlay Receiver in **System Settings → General → AirDrop & Handoff**, or change the port in `backend/app.py` (e.g. `port=5001`) and set `VITE_API_BASE=http://localhost:5001` for the frontend.

### Frontend (Vue + Vite)

Same on **Windows**, **macOS**, and **Linux**:

1. Open a **new** terminal in the project folder:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   On Windows you can use Command Prompt, PowerShell, or Git Bash; the commands are the same.

2. Open the URL shown in the terminal (usually **http://localhost:5173**). The app will call the backend health endpoint—ensure the backend is running so the health check succeeds.

### Optional: Backend API base URL

By default the frontend uses `http://localhost:5000`. To override, create a `.env` file in the `frontend/` directory with:

```
VITE_API_BASE=http://localhost:5000
```

(Use a different URL if you changed the backend port.)
