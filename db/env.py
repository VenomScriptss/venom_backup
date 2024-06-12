from os import environ

from dotenv import load_dotenv


def getenv(key):
    load_dotenv()

    if result := environ.get(key):
        try:
            return eval(result)
        except:
            return result
    return None
