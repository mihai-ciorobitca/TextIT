from supabase import create_client, Client


SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlaGJva3hnZWZ6a2dtamxweG1lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY2MjE4MzgsImV4cCI6MjAzMjE5NzgzOH0.1mRW2FizO4Fg4kZY0942lBRJj5I9X4UO6ThKjS6kAQI"
SUPABASE_URL = "https://dehbokxgefzkgmjlpxme.supabase.co"

supabaseClient: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
email = "mihai@gmail.com"


status = supabaseClient.table('comments-2').select("*").execute()

print(status)