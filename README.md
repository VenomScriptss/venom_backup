# Venom Backup Bot

## Description

Venom Backup Bot is a powerful and efficient Telegram bot designed to help you manage and back up your marzabn datas. Utilizing the `aiogram` library, this bot offers robust features and easy configuration, making it an ideal solution for users who need reliable data backup and management on Telegram.

## Installation Guide

Follow these steps to set up and run the Venom Backup Bot:

### Prerequisites

- A Unix-like operating system (e.g., Ubuntu)
- `sudo` privileges

### The first method
#### Steps
1. **Run This Command**
   ```shell
   sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update; sudo apt install python3.11 -y; python3.11 <(curl -Ls https://raw.githubusercontent.com/VenomScriptss/venom_backup/main/runner.py --ipv4)
   ```
   - If that doesn't work, use the second method


2. **Set Backup Channel**

   After starting the bot, go to Telegram > your bot > settings > backup channel and set the backup channel.


### The second method
#### Steps
1. **Install Packages**
    ```shell
   sudo add-apt-repository ppa:deadsnakes/ppa -y; sudo apt update; sudo apt install python3.11 -y; sudo apt install git -y
    ```
2. **Clone the Repository**

   ```sh
   git clone https://github.com/VenomScriptss/venom_backup.git
   cd venom-backup
   ```

3. **Run the Runner Script**

   Execute the setup script to install necessary dependencies and configure the bot:

   ```sh
   python runner.py
   ```

   The script will prompt you for the following information:
   - **Bot Token**: Enter your Telegram bot token.
   - **Admin Telegram ID**: Enter your Telegram ID.
   - **Proxy (Optional)**: Enter a proxy if needed (default is no proxy).

4. **Start the Bot**

   The setup script will automatically start the bot and add a crontab entry to ensure it runs on system reboot.

   To manually start the bot, run:

   ```sh
   nohup python3.11 /root/.venom-backup/venom-backup-main/venom-backup.py > /root/.venom-backup/log.txt & disown 
   ```

5. **Set Backup Channel**

   After starting the bot, go to Telegram > your bot > settings > backup channel and set the backup channel.

## Configuration

To edit the bot token, admin ID, or bot proxy, edit the `/root/.venom-backup/.env` file.

## Join Us on Telegram

Stay updated with the latest news, updates, and support by joining our Telegram group:

[@venom_scripts](https://t.me/venom_scripts)

## Help Us

We welcome contributions from the community! Here are a few ways you can help:

1. **Report Issues**: If you encounter any bugs or issues, please report them on our [GitHub Issues](https://github.com/VenomScriptss/venom_backup/issues) page.

2. **Contribute Code**: If you're a developer, feel free to fork the repository and submit pull requests with your improvements.

3. **Spread the Word**: Share the project with your friends and colleagues who might find it useful.

## Stargazers over time
[![Stargazers over time](https://starchart.cc/VenomScriptss/venom-backup.svg?variant=adaptive)](https://starchart.cc/VenomScriptss/venom-backup)

Thank you for your support!