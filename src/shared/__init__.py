from dotenv import load_dotenv

res = load_dotenv()
if not res:
    print("========= COULD NOT LOAD .env =========")
