from dotenv import dotenv_values

env = dotenv_values(".env")

# TELEGRAM BOT
TOKEN: str = env["TOKEN"]

