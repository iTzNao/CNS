import subprocess
import json

def get_config():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config

def main():
    config = get_config()
    if config["bot_run"] == True:
        print("🔄️ Running bot")
        subprocess.Popen(["python", "bot/bot.py"])
    
if __name__ == "__main__":
    main()
