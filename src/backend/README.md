Backend (FastAPI + SQLite)

How to run:

1. Create/activate your virtual environment.
2. Install dependencies from the project root or backend folder.
3. Start the API server.

On Windows PowerShell:

```powershell
cd "c:\Users\shiva\OneDrive\Desktop\College\New folder\src\backend"
python -m pip install -r ..\..\requirements.txt
python run_server.py
```

The API will be available at http://localhost:8000.

What it does:
- Creates a local SQLite database at src/backend/logistics.db
- On startup, reads CSVs from data/raw and seeds tables (drivers, vehicles, trips, expenses)
- Exposes endpoints that the frontend expects, e.g. /dashboard/stats, /drivers, /trips, /expenses
