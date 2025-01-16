import datetime
import crontab

def main():
    now = datetime.datetime.now() # gets the current time
    now_formatted = now.strftime('%m/%d/%Y %H:%M:%S') # formats the time into MM/DD/YYY HH:MM:SS format
    with open("send_email.txt", "w") as email_message:
        email_message.writelines(f"access.log and auth.log last scanned at {now_formatted}") # writes the log entry to an external .txt file

if __name__ == "__main__":
    main()