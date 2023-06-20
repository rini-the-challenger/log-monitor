import string
import pathlib
from yml_admin import YmlAdmin
import regex


import pandas as pd

"""
Responsible for doing the search
"""

pattern = ["info", "error", "warning"]
err_df = pd.DataFrame(columns=['Filename', 'Type', 'Line No.', 'Issue Details'])


def process_log():
    yml = YmlAdmin()
    yml.read_yaml()
    root = yml.settings['APP']['ROOT-DIR']
    root_path = pathlib.Path(root)

    for item in root_path.rglob("*"):
        # print(f"{item} - {'dir' if item.is_dir() else 'file'}")
        if item.is_file():
            # Read log file and classify each entry
            with open(item, 'r', encoding="ISO-8859-1") as file:
                line_cnt = 0
                for line in file:
                    line_cnt = line_cnt + 1
                    if str(pattern[0]) in line:
                        temp_lst = [str(item), "ERROR", str(line_cnt), line]
                        print(temp_lst)
                    elif str(pattern[1]) in line:
                        temp_lst = [str(item), "WARNING", str(line_cnt), line]
                        print(temp_lst)

                        err_df.loc[len(err_df)] = temp_lst

                    # r1 = regex.search (r"error", line)
                    # print(r1)
                    # findall(r"^\w+",xx)
    # display all the  rows
    pd.set_option('display.max_rows', None)

    # display all the  columns
    pd.set_option('display.max_columns', None)

    # set width  - 100
    pd.set_option('display.width', 100)

    # set column header -  left
    pd.set_option('display.colheader_justify', 'left')

    # set precision - 5
    pd.set_option('display.precision', 10)
    print(err_df)
    return err_df
