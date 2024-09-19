import os
from email_alert import send_email_alert
import time

phytotron_login = {"A": "F: 192.168.100.80 Admin00 /USER:Admin",
                   "C": "I: 192.168.100.82 Admin00 /USER:Admin"}
phytotron_drive = {"A": "F", "C": "I"}

def get_log(current_working_directory, output_path="", phytotrons=["A"]):
    try:
        # Remove existing xlsx
        for directory in ("Active", "History"):
            for root, dirs, files in os.walk(os.path.join(current_working_directory, directory)):
                for file in files:
                    os.remove(os.path.join(root, file))

        for phytotron in phytotrons:
            cmd = f"cd C:\\Program Files\\Ferro Software\\FtpUse && ftpuse {phytotron_login[phytotron]} && timeout 30 && exit"
            os.system(f'start cmd /c "{cmd}"')
            
            time.sleep(5)
            cmd = f"copy {phytotron_drive[phytotron]}:\\Samples\\PHYTO_{phytotron}_COURBE\\Active {output_path}"
            os.system(cmd)
    except:
          send_email_alert("Couldn't reach local phytotron server")

if __name__ == "__main__":
       get_log(current_working_directory=".")
