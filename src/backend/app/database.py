from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Initialize supabase client only if credentials are provided
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("Warning: Supabase credentials not found. Please create a .env file with SUPABASE_URL and SUPABASE_ANON_KEY")

def get_db():
    if supabase is None:
        raise Exception("Database not configured. Please set up Supabase credentials in .env file")
    return supabase

def get_supabase_client():
    """Dependency function for FastAPI routes"""
    return get_db()
