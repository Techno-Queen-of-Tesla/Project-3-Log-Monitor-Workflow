from datetime import datetime
import yagmail

# defined file paths
log_file = "access.log"
last_run_time = "last_run_time.txt"
monitor_log = "monitoring.log"

# function to load the last run time from file
def load_last_run_time():
    try:
        with open(last_run_time, "r") as last_run_file:
            timestamp_str = last_run_file.read().strip()
            # in case the file is empty, return None
            if not timestamp_str:   
                return None
            return datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
    except FileNotFoundError:
        return None
    except ValueError:
        # if the timestamp format isn't valid, return None
        return None

def save_last_run_time(timestamp):
    # save the last run time to a file
    with open(last_run_time, "w") as last_run_file:
        last_run_file.write(timestamp.strftime("%b %d %H:%M:%S"))

def log_activity(message):
    # log the alert or activity with a timestamp in monitoring.log
    with open(monitor_log, "a") as log_file:
        log_file.write(f"{datetime.now().strftime("%b %d %H:%M:%S")} - {message}\n")

def web_traffic(last_run_time=None):
    # monitor web traffic and detect unusually high activity
    new_last_run_time = datetime.now()
    relevant_lines = []

    # if it's the first run, ignore all past logs by setting last_run_time to the current time (now)
    if last_run_time is None:
       last_run_time = new_last_run_time

    with open(log_file, "r") as f:
        for line in f:
            try:
                # get timestamp from the log entry (adjusted to log format)
                timestamp_str = line.split("[")[1].split(" ")[0]  # extract timestamp
                log_timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
                log_timestamp = log_timestamp.replace(year=new_last_run_time.year)

                # check if the log entry is new since the previous scan
                if last_run_time is None or log_timestamp > last_run_time:
                    relevant_lines.append(line)
            except (ValueError, IndexError):
                # skip any lines that don't match the format
                continue

    # count the new log input lines since the last scan
    requests = len(relevant_lines)

    # email settings
    EMAIL_ADDRESS = "me@lighthouselabs.com" # my email address
    EMAIL_PASSWORD = "mypassword"  # password for my email account
    ALERT_EMAIL = "manager@lighthouselabs.com" # manager's email address

    def send_email_alert(subject, message):
        try:
            yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
            yag.send(
                to=ALERT_EMAIL,
                subject=subject,
                contents=message
            )

        # checks if the threshold has been exceeded, and outputs an alert to an email, if so
            if requests > 300:
                send_email_alert(f"ALERT: High traffic detected! {requests} new requests since last scan.")
        except Exception as e:
                send_email_alert(f"Failed to send email: {e}")

    # last_run_time.txt file is updated with the current time
    save_last_run_time(new_last_run_time)

if __name__ == "__main__":
    last_run = load_last_run_time()
    web_traffic(last_run)
