import datetime
import subprocess

def main():
    now = datetime.now() # gets the current time
    now_formatted = now.strftime('%m/%d/%Y %H:%M:%S') # formats the time into MM/DD/YYY HH:MM:SS format
    with open("send_email.txt", "w") as email_message:
        email_message.writelines(f"access.log and auth.log last scanned at {now_formatted}") # writes the log entry to an external .txt file

# FAILED PASSWORD MONITORING - running a shell command with "subprocess" module, and sending the output to failed_passwords.txt
tail_process = subprocess.Popen(['tail', '-n', '100', '/workspaces/Project-2-Log-Monitor-Workflow/auth.log'], stdout=subprocess.PIPE, text=True)
grep_process = subprocess.Popen(["grep", "fail"], stdin=tail_process.stdout, stdout=subprocess.PIPE, text=True)
with open("failed_passwords.txt", "w") as grep_output:
    output, error = grep_process.communicate()
    grep_output.writelines(output)

# UNUSUAL SERVER TRAFFIC - run the traffic_script.py file to check the web server access log
exec(open("traffic_script.py").read())

if __name__ == "__main__":
    main()