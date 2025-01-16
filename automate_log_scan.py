import datetime
from crontab import CronTab

def main():
    now = datetime.datetime.now()
    with open(r"send_email.txt", "w"):
        print(f"Cron job executed at {now}")

if __name__ == "__main__":
    main()