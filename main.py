# Personal packages
from get_log import get_log
from check_xlsx import check_data
from merge_excel import merge_exported_excels
from usmp_converter import usmp_converter
import email_alert

# Public librairies
import time
import os


if __name__ == "__main__":
    # Folder path
    current_working_directory = os.getcwd()

    # Which to check and who to contact, how often
    phytotrons_to_check = ["C"]
    email_alert.recipients = ["tristan.gerault@inrae.fr", "xavier.cornilleau@inrae.fr", "alain.fortineau@inrae.fr", "frederic.rees@inrae.fr", "auriane.voyard@inrae.fr"]
    check_period_in_minutes = 10
    accepted_error_in_percent = dict(
        humidity=20,
        temperature=5
    )

    while True:
        # Steps
        # 1. We open a FTP connection for each rhizotron, mount it to a drive letter, and copy / paste the .uspm file to the local "Active" directory
        get_log(current_working_directory=current_working_directory, output_path=os.path.join(current_working_directory, "Active"), phytotrons=phytotrons_to_check)
        usmp_converter()
        merge_exported_excels(current_working_directory=current_working_directory, workpath=os.path.join(current_working_directory, "Active"), phytotrons=phytotrons_to_check)
        check_data(back_in_time_minutes = check_period_in_minutes, error_threshold = accepted_error_in_percent, CO2_threshold=1500, phytotrons=phytotrons_to_check)
        time.sleep(check_period_in_minutes * 60)
