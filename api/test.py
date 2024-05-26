from supabase import create_client, Client
from dotenv import load_dotenv
from os import environ

load_dotenv()

supabase_url = environ.get("SUPABASE_URL")
supabase_secret = environ.get("SUPABASE_SECRET")

supabaseClient: Client = create_client(supabase_url, supabase_secret)

status = supabaseClient.table('users').insert([{"email": "email@gmail.co", "password": "password"}]).execute()

print(status)