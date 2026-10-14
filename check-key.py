from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("TYPESAFE_API_KEY")

if key:
    print("Key found successfully!")
    print("First 12 characters:", key[:12])
    print("Total length:", len(key))
else:
    print("ERROR: Key NOT found.")
