from os import environ

from dotenv import load_dotenv


def getenv(key):
    load_dotenv("/root/.venom-backup/venom_backup-main/.env")

    if result := environ.get(key):
        try:
            return eval(result)
        except:
            return result
    return None
