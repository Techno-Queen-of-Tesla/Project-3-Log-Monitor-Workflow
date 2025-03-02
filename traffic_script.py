from datetime import datetime
import pytz
import yagmail
import re

    # defined file paths
log_file = "/workspaces/Project-2-Log-Monitor-Workflow/var/log/auth.log"
last_run_time_file = "/workspaces/Project-2-Log-Monitor-Workflow/tmp/last_run_time.txt"
monitor_log = "/workspaces/Project-2-Log-Monitor-Workflow/var/log/monitoring.log"
eastern = pytz.timezone("America/New_York")

    # email settings
EMAIL_ADDRESS = "me@lighthouselabs.com" # my email address
EMAIL_PASSWORD = "mypassword"  # password for my email account
ALERT_EMAIL = "manager@lighthouselabs.com" # manager's email address

    # function to load the last run time from file
def load_last_run_time():
    try:
        with open(last_run_time_file, "r") as last_run_file:
            timestamp_str = last_run_file.read().strip()

    # in case the file is empty, return None
            if not timestamp_str:   
                return None
            return datetime.strptime(timestamp_str, "%b %d %H:%M:%S").replace(tzinfo=eastern)
    except FileNotFoundError:
        return None
    except ValueError:
    # if the timestamp format isn't valid, return None
        return None

def save_last_run_time(timestamp):
    # save the last run time to a file
    with open(last_run_time_file, "w") as last_run_file:
        last_run_file.write(timestamp.strftime("%b %d %H:%M:%S"))

def log_activity(message):
    now = datetime.now(eastern)

    # log the alert or activity with a timestamp in monitoring.log
    with open(monitor_log, "a") as monitor_file:
        log_file.write(f"{now.strftime('%b %d %H:%M:%S')} - {message}\n")

def send_email_alert(subject, message):
    try:
        yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
        yag.send(
            to=ALERT_EMAIL,
            subject=subject,
            contents=message
        )
    except Exception as e:
        log_activity(f"Failed to send email: {e}")

def web_traffic(last_run_time=None):

    # monitor web traffic and detect unusually high activity
    new_last_run_time = datetime.now(eastern)
    relevant_lines = []

    # if it's the first run, ignore all past logs by setting last_run_time to the current time (now)
    if last_run_time is None:
       last_run_time = new_last_run_time

    with open(log_file, "r") as f:
        for line in f:
            pattern = r'[A-Z]{3} +[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
            match = re.search(pattern, line)

            if match:
                timestamp_str = match.group(0)

    # get timestamp from the log entry (adjusted to log format)
                try:
                    log_timestamp = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
                    log_timestamp = eastern.localize(log_timestamp.replace(year=new_last_run_time.year))

    # check if the log entry is new since the previous scan
                    if last_run_time is None or log_timestamp > last_run_time:
                        relevant_lines.append(line)
                except (ValueError, IndexError):
            
    # skip any lines that don't match the format
                    continue

    # count the new log input lines since the last scan
    requests = len(relevant_lines)

    # checks if the threshold has been exceeded, and outputs an alert to an email, if so
    if requests > 300:
        send_email_alert(f"ALERT: High traffic detected! {requests} new requests since last scan.")

    # last_run_time.txt file is updated with the current time
    save_last_run_time(new_last_run_time)

if __name__ == "__main__":
    last_run = load_last_run_time()
    web_traffic(last_run)
