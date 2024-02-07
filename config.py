from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_BOT=os.getenv("TOKEN_BOT")
HOST_DB=os.getenv("HOST_DB")
PORT_DB=int(os.getenv("PORT_DB"))
PASS_DB=os.getenv("PASS_DB")
USER_DB=os.getenv("USER_DB")
NAME_DB=os.getenv("NAME_DB")