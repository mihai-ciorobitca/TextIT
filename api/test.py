import os
from supabase import create_client
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SECRET")
supabase = create_client(url, key)
messages = supabase.table("messages").select("*").execute()

print(messages)