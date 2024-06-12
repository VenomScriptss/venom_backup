# sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update; sudo apt install python3.11 -y; python3.11 <(curl -Ls https://raw.githubusercontent.com/VenomScriptss/venom_backup/main/runner.py --ipv4)
import os
os.system("clear")

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
try:
    validate_token(token)
except Exception as e:
    print(e)
    exit(1)


admin_id = input("Enter The Admin Telegram ID: ")
if not admin_id.isnumeric():
    print("Invalid Admin ID")
    exit(1)

proxy = input("Enter The Proxy (For Iran) [Default=no proxy]: ").strip()
if proxy in ("no proxy", ""):
    proxy = None

os.system("clear")
print("Installing Python and necessary tools...")
os.system("sudo add-apt-repository ppa:deadsnakes/ppa -y")
os.system("sudo apt update")
os.system("sudo apt install python3.11 -y")
os.system("sudo apt install zip -y")
os.system("curl -O https://bootstrap.pypa.io/get-pip.py")
os.system("sudo python3.11 get-pip.py")

print("\n\n\nSetting up the bot...")
os.system("mkdir -p /root/.venom-backup")
os.system("cd /root/.venom-backup; wget -N --no-check-certificate https://github.com/VenomScriptss/venom_backup/archive/refs/heads/main.zip; unzip -o main.zip")
with open("/root/.venom-backup/venom_backup-main/.env", "w") as f:
    f.write(f"TOKEN={token}\nADMIN_ID={admin_id}\nPROXY={proxy}\n")
os.system(
    "cd /root/.venom-backup/venom_backup-main; python3.11 -m pip install -r /root/.venom-backup/venom_backup-main/requirements.txt; nohup python3.11 /root/.venom-backup/venom_backup-main/venom-backup.py > /root/.venom-backup/log.txt & disown")

print("\n\n\nAdding crontab entry...")
os.system(
    '(crontab -l ; echo "@reboot python3.11 /root/.venom-backup/venom_backup-main/venom-backup.py > /root/.venom-backup/log.txt") | crontab -')

print("\n\n\nSetup complete.")
