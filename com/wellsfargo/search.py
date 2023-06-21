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
    log_scan_types = yml.settings['APP']['SCAN-XTN']

    root_path = pathlib.Path(root)

    # Using join regex for pattern
    regex_pattern = '(% s)' % '|'.join(pattern)

    print(regex_pattern)
    for item in root_path.rglob("*"):
        if item.is_file():
            if pathlib.Path(item).suffix in log_scan_types:

                # Read log file and classify each entry
                with open(item, 'r', encoding="ISO-8859-1") as file:
                    line_cnt = 0
                    for line in file:
                        line_cnt = line_cnt + 1
                        match = regex.search(regex_pattern, line, regex.IGNORECASE)
                        if match:
                            err_lst = [str(item), match.group(), str(line_cnt), line]
                            print(err_lst)

                            err_df.loc[len(err_df)] = err_lst

    display_logs(err_df)
    return err_df


def display_logs(df):
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
    print(df)
