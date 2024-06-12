# sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update; sudo apt install python3.11 -y; python3.11 <(curl -Ls https://raw.githubusercontent.com/VenomScriptss/venom_backup/main/runner.py --ipv4)
import os


def validate_token(token: str) -> bool:
    """
    Validate Telegram token

    :param token:
    :return:
    """
    if not isinstance(token, str):
        raise ValueError(
            f"Token is invalid! It must be 'str' type instead of {type(token)} type."
        )

    if any(x.isspace() for x in token):
        message = "Token is invalid! It can't contains spaces."
        raise ValueError(message)

    left, sep, right = token.partition(":")
    if (not sep) or (not left.isdigit()) or (not right):
        raise ValueError("Token is invalid!")


token = input("Enter The Bot Token: ")
if not validate_token(token):
    print("Invalid Token")
    exit(1)

admin_id = input("Enter The Admin Telegram ID: ")
if not admin_id.isnumeric():
    print("Invalid Admin ID")
    exit(1)

proxy = input("Enter The Proxy (For Iran) [Default=no proxy]: ").strip()
if proxy in ("no proxy", ""):
    proxy = None

with open(".env", "w") as f:
    f.write(f"TOKEN={token}\nADMIN_ID={admin_id}\nPROXY={proxy}\n")

print("Installing Python and necessary tools...")
os.system("sudo add-apt-repository ppa:deadsnakes/ppa -y")
os.system("sudo apt update")
os.system("sudo apt install python3.11 -y")
os.system("sudo apt install zip -y")
os.system("curl -O https://bootstrap.pypa.io/get-pip.py")
os.system("sudo python3.11 get-pip.py")

print("Setting up the bot...")
os.system("mkdir -p /root/.venom-backup")
os.system(
    "cd /root/.venom-backup; wget -N --no-check-certificate https://github.com/VenomScriptss/venom_backup/archive/refs/heads/main.zip; unzip -o main.zip; cd venom-backup-main; python3.11 -m pip install -r requirements.txt; nohup python3.11 /root/.venom-backup/venom-backup-main/venom-backup.py > /root/.venom-backup/log.txt & disown")

print("Adding crontab entry...")
os.system(
    '(crontab -l ; echo "@reboot python3.11 /root/.venom-backup/venom-backup-main/venom-backup.py > /root/.venom-backup/log.txt") | crontab -')

print("Setup complete.")