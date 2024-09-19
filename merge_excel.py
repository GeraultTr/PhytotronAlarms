import os
import pandas as pd

def merge_exported_excels(current_working_directory, input_file=True, workpath = "Active", phytotrons=["A"]):
    for phytotron in phytotrons:
        daily_list = []
        if input_file:
            history_file = pd.read_excel(os.path.join(current_working_directory, f"Phyto_{phytotron}_courbes.xlsx")).set_index(["Date", "Time"], drop=False)
            history_file.index = history_file.index.rename(["days", "seconds"])
            history_file = history_file[[col for col in history_file.columns if "Unnamed" not in col]]
            new_file = pd.read_excel(os.path.join(workpath, f"PHYTO_{phytotron}_COURBE.xlsx")).set_index(["Date", "Time"], drop=False)
            new_file.index = new_file.index.rename(["days", "seconds"])
            new_file = new_file[[col for col in new_file.columns if "Unnamed" not in col]]
            new_file = new_file[new_file["Date"] > 0.]

        else:
            for file in os.listdir(workpath):
                if file.endswith(".xlsx"):
                    daily_list += [pd.read_excel(os.path.join(workpath, file))[:-2]]

        merged_dataframe = history_file.merge(new_file, how="outer")
        
        merged_dataframe.to_excel(f"Phyto_{phytotron}_courbes.xlsx")
