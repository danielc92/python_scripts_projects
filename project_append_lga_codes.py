import datetime as dt
import pandas as pd
import numpy as np

def get_lga_name_column_as_series(data, dirty_lga_col_name=""):
    try:
        series = data[dirty_lga_col_name]
        return series
    except:
        print("error: could not create series using the column name specified.")


def import_csv_or_excel(filepath="",
                        sheet_name="Sheet1",
                        data_delimeter=",",
                        lga_col_name=""):

    if ".csv" in filepath:
        data = pd.read_csv(filepath, low_memory=False, error_bad_lines=False, delimiter=data_delimeter)

    elif ".xlsx" in filepath:
        # excel_data = pd.ExcelFile(filepath)
        # data = pd.concat([excel_data.parse(sheet_name)], axis=1)
        data = pd.read_excel(filepath, sheet_name = sheet_name)

    else:
        print("File neither .csv or .xlsx")

    data = data.dropna(how="all", axis=1)

    return data


def clean_lga_name_list(series):
    dirty_lga_list = series.tolist()
    '''
        steps
        1. uppercase
        2. strip
        3. replace anything which is not A-Z with spaces
        4. replace all double spaces with single spaces
    '''
    # Change all case to uppercase
    for n in range(len(dirty_lga_list)):
        dirty_lga_list[n] = dirty_lga_list[n].upper()

    # Any chars included in this string will not be replaced by spaces
    acceptable_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for index in range(len(dirty_lga_list)):
        string = dirty_lga_list[index]
        for index2 in range(len(string)):
            if string[index2] in acceptable_chars:
                pass
            else:
                string = string.replace(string[index2], " ")
        dirty_lga_list[index] = string

    # Replace all double spaces with single spaces
    for index in range(len(dirty_lga_list)):
        while "  " in dirty_lga_list[index]:
            dirty_lga_list[index] = dirty_lga_list[index].replace("  ", " ")

    # Strip all of the trailing and leading white space
    for index in range(len(dirty_lga_list)):
        dirty_lga_list[index] = dirty_lga_list[index].strip()

    cleaned_lga_list = dirty_lga_list

    return cleaned_lga_list


def create_lga_code_series_from_list(my_lga_list):

    lga_dict = {20110: 'ALPINE'
    ,20260: 'ARARAT'
    ,20570: 'BALLARAT'
    ,20660: 'BANYULE'
    ,20740: 'BASS COAST'
    ,20830: 'BAW BAW'
    ,20910: 'BAYSIDE'
    ,21010: 'BENALLA'
    ,21110: 'BOROONDARA'
    ,21180: 'BRIMBANK'
    ,21270: 'BULOKE'
    ,21370: 'CAMPASPE'
    ,21450: 'CARDINIA'
    ,21610: 'CASEY'
    ,21670: 'CENTRAL GOLDFIELDS'
    ,21750: 'COLAC OTWAY'
    ,21830: 'CORANGAMITE'
    ,21890: 'DAREBIN'
    ,22110: 'EAST GIPPSLAND'
    ,22170: 'FRANKSTON'
    ,22250: 'GANNAWARRA'
    ,22310: 'GLEN EIRA'
    ,22410: 'GLENELG'
    ,22490: 'GOLDEN PLAINS'
    ,22620: 'GREATER BENDIGO'
    ,22670: 'GREATER DANDENONG'
    ,22750: 'GREATER GEELONG'
    ,22830: 'GREATER SHEPPARTON'
    ,22910: 'HEPBURN'
    ,22980: 'HINDMARSH'
    ,23110: 'HOBSONS BAY'
    ,23190: 'HORSHAM'
    ,23270: 'HUME'
    ,23350: 'INDIGO'
    ,23430: 'KINGSTON'
    ,23670: 'KNOX'
    ,23810: 'LATROBE'
    ,23940: 'LODDON'
    ,24130: 'MACEDON RANGES'
    ,24210: 'MANNINGHAM'
    ,24250: 'MANSFIELD'
    ,24330: 'MARIBYRNONG'
    ,24410: 'MAROONDAH'
    ,24600: 'MELBOURNE'
    ,24650: 'MELTON'
    ,24780: 'MILDURA'
    ,24850: 'MITCHELL'
    ,24900: 'MOIRA'
    ,24970: 'MONASH'
    ,25060: 'MOONEE VALLEY'
    ,25150: 'MOORABOOL'
    ,25250: 'MORELAND'
    ,25340: 'MORNINGTON PENINSULA'
    ,25430: 'MOUNT ALEXANDER'
    ,25490: 'MOYNE'
    ,25620: 'MURRINDINDI'
    ,25710: 'NILLUMBIK'
    ,25810: 'NORTHERN GRAMPIANS'
    ,25900: 'PORT PHILLIP'
    ,25990: 'PYRENEES'
    ,26080: 'QUEENSCLIFFE'
    ,26170: 'SOUTH GIPPSLAND'
    ,26260: 'SOUTHERN GRAMPIANS'
    ,26350: 'STONNINGTON'
    ,26430: 'STRATHBOGIE'
    ,26490: 'SURF COAST'
    ,26610: 'SWAN HILL'
    ,26670: 'TOWONG'
    ,29399: 'UNINCORPORATED VIC'
    ,26700: 'WANGARATTA'
    ,26730: 'WARRNAMBOOL'
    ,26810: 'WELLINGTON'
    ,26890: 'WEST WIMMERA'
    ,26980: 'WHITEHORSE'
    ,27070: 'WHITTLESEA'
    ,27170: 'WODONGA'
    ,27260: 'WYNDHAM'
    ,27450: 'YARRA RANGES'
    ,27350: 'YARRA'
    ,27630: 'YARRIAMBIACK'
    ,29499: 'NO USUAL ADDRESS'
    ,29799: 'MIGRATORY OFFSHORE SHIPPING'}

    lga_code_list = []

    for index in range(len(my_lga_list)):

        current_lga_name = my_lga_list[index]

        flag = False

        for item in lga_dict.items():
            reference_lga_code = item[0]
            reference_lga_name = item[1]

            if reference_lga_name in current_lga_name:
                lga_code_list.append(reference_lga_code)
                flag = True
            if flag == True:
                break

        if flag == False:
            lga_code_list.append(None)

    lga_code_series = pd.Series(lga_code_list)
    return lga_code_series


def append_new_codes_to_original_data(data,
                                      new_lga_column_series):
    data = pd.concat([data, new_lga_column_series.rename("LGA_CODE_SCRIPT")], axis=1)
    return data

def export_new_data(new_data, export_name="cleaned_lga", type=".csv"):
    if type != ".xlsx" and type != ".csv":
        type = ".csv"

    if type == ".csv":
        new_data.to_csv(export_name + type, index=False)
    elif type == ".xlsx":
        new_data.to_excel(export_name + type, index=False)


'''Import data, specifying sheet name if the file has .xlsx extension'''
data = import_csv_or_excel(sheet_name="Sheet1",
                           filepath=r"C:\Users\admin-vicvphq\danielc_pycharm_project\datasets\dirty_lga.csv")

'''Use get_lga_name_column_as_series() to create series from data given the name of dirty lgas'''
series = get_lga_name_column_as_series(data, dirty_lga_col_name="dirty_lga")

'''Clean the series created above using clean_lga_name_list() function'''
clean_list = clean_lga_name_list(series)

'''Create new lga code series based on clean list above'''
new_lga_code_series = create_lga_code_series_from_list(my_lga_list=clean_list)

'''Append newly found codes to original data set'''
new_data = append_new_codes_to_original_data(data, new_lga_code_series)

'''Export to .csv, specifying name of file (excludes extension)'''
export_new_data(new_data, export_name="daniels_very_clean_LGAs", type=".xlsx")