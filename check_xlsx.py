import pandas as pd 
from datetime import datetime, timedelta
from email_alert import send_email_alert
from datetime import datetime


def check_data(phytotrons=["A"], back_in_time_minutes = 60, error_threshold: dict = {}, CO2_threshold=4750):
    for phytotron in phytotrons:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        message = f"At time : {time}\n"
        errors = False
        log = pd.read_excel(f"Phyto_{phytotron}_courbes.xlsx")
        log = log[log["Date"] > 0.]

        reference_date = datetime.strptime("18/06/24", '%d/%m/%y')
        reference_date_int = 45461

        log["Real_Date"] = [reference_date + timedelta(days=(log["Date"] + log["Time"]).to_list()[k] - reference_date_int) for k in range(len(log["Date"]))]
        
        log = log[(datetime.now() - log["Real_Date"]).dt.days == 0.]
        log = log[(datetime.now() - log["Real_Date"]).dt.seconds / 3600 <= back_in_time_minutes / 60]

        if 0. in log["MARCHE ARRET Value"].to_list():
            message += f"[ERROR] PHYTOTRON {phytotron} STOPPED\n"
            message += "\n"
            errors = True

        diff_humidity = abs(log["HR Consigne Value"] - log["HR Mesure Value"])/log["HR Consigne Value"]

        humidity_threshold = error_threshold["humidity"]
        if diff_humidity.mean() > humidity_threshold / 100:
            message += f"[ERROR] HUMIDITY WENT AWAY FROM THE {humidity_threshold}% CONSTRAINT : {round(log['HR Mesure Value'].mean(), 2)} instead of {round(log['HR Consigne Value'].mean(), 2)}\n"
            message += "\n"
            errors = True

        diff_temperature = abs(log["T° Consigne Value"] - log["T° Mesure Value"])/log["T° Consigne Value"]

        temperature_threshold = error_threshold["temperature"]
        if diff_temperature.mean() > temperature_threshold:
            message += f"[ERROR] Temperature WENT AWAY FROM THE {temperature_threshold}% CONSTRAINT : {round(log['T° Mesure Value'].mean(), 2)} instead of {round(log['T° Consigne Value'].mean(), 2)}\n"
            message += "\n"
            errors = True

        check_CO2 = log['CO2 Mesure Value'] > CO2_threshold

        if True in check_CO2.to_list():
            message += f"[ERROR] CO2 peaks above {CO2_threshold} ppm limit value, maxima at {log['CO2 Mesure Value'].max()} ppm\n"
            message += "\n"
            errors = True

        general_footer = """\n__________________\n
            EN CAS D'ALARME INATTENDUE, contacter localement :\n
            - Auriane Voyard : 06 04 41 99 92\n
            - Tristan Gérault : 06 95 76 47 98\n
            - Xavier Cornilleau : 06 37 98 17 97\n
            - Alain Fortineau : 06 78 34 57 39\n
            - Frédéric Rees : 06 63 97 46 60\n
            (Si vous en êtes à l'origine, faites un retour de mail)\n\n
            SI LE PROBLEME PERSISTE, contacter : \n
            https://www.froids-et-mesures.com/ Tél. : +33 (0)2 41 35 06 06 Beaucouzé 49070 - France\n
            Numéros d'urgence : Georges Menard 06 71 76 89 10  jusqu'au 12 aout 2024\n
            Daniel Foinel  06 80 95 19 11  à partir du 12 aout 2024\n
            contact@froids-et-mesures.fr\n
            POUR L'ACCES HORS DES HORAIRES D'OUVERTURE DU SITE, PC Sécurité AgroParisTech : 01 89 10 01 12\n"""
        
        message += general_footer
        
        if errors:
            send_email_alert(body=message, subject=f"Phytotron {phytotron} report")
            print(message)
        else:
            print(f"At time {time}, Every check passed on phytotron {phytotron}")
