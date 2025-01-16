import datetime
from crontab import CronTab

def main():
    now = datetime.datetime.now()
    print(f"Cron job executed at {now}")

if __name__ == "__main__":
    main()