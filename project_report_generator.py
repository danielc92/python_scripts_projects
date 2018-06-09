import pandas as pd
import datetime as dt
import sys
import os

#converts number to percent, without the % sign
def turn_to_perc(number):
    try:
        float(number)
        number = round((number)*100,4)
        return number
    except ValueError:
        print("Number could not be converted to float. Percent could not be produced.")

#converts a variable to string and prints it under a line break
def p(x):
    print("\n--------------------------------------------------------------------------------------\n\n" + str(x))

#prints a string and replaces all occurences of '%%' with arguments passed in after the string, accepts unlimited arguments. example: sp("%% scored %% on the %% test", name, score_val, test_type)
def sp(text, *args):

    var_count = text.count("%%")

    var_list = []

    for item in args:
        var_list.append(str(item))

    if var_count == len(var_list):
        for n in range(var_count):
            text = text.replace("%%", var_list[n], 1)
        print(text)
    else:
        print("Error: args count does not match replacement count.")

#calcualtes and return mean of a float list
def get_str_list_mean(list):

    # remove nulls
    while "NAN" in list:
        list.remove("NAN")

    floats_list = []
    counter = 0

    for item in list:
        try:
            float(item)
            floats_list.append(float(item))
        except ValueError:
            counter = counter + 1

    if counter > 0:
        return "N/A"

    else:
        list_length = len(floats_list)
        total = 0

        for number in floats_list:
            total = total + number

        try:
            mean = total / list_length
            mean_rounded = round(mean,2)
        except ZeroDivisionError:
            mean_rounded = "N/A"

        return mean_rounded

#calculates and returns median of a float list
def get_str_list_median(list):

    # remove nulls and order list
    while "NAN" in list:
        list.remove("NAN")

    floats_list = []

    counter = 0
    for item in list:
        try:
            float(item)
            floats_list.append(float(item))
        except ValueError:
            counter = counter + 1

    floats_list = sorted(floats_list)
    list_length = len(floats_list)

    if counter > 0:

        return "N/A"

    else:
        if list_length == 0:
            list_median_rounded = "N/A"

        elif list_length % 2 == 0:
            upper_index = int(list_length / 2)
            lower_index = upper_index - 1
            list_median = (floats_list[upper_index] + floats_list[lower_index]) / 2
            list_median_rounded = round(list_median, 2)

        else:
            index = int(list_length / 2 )
            list_median = floats_list[index]
            list_median_rounded = round(list_median,2)
        return list_median_rounded

#main report generator code
def gen_data_report(import_path = "",
                    export_path = "",
                    distinct_threshold_int = 30,
                    export_data = False,
                    export_data_type = ".csv",
                    export_data_name = "MY_DATA",
                    report_export = True,
                    report_data_type = ".csv",
                    excel_sheet_name = "Sheet1",
                    data_delimeter = ","
                    ):

    start_time = dt.datetime.now()

    start_time_path_formatted = start_time.strftime("%d-%M-%Y_%H-%M-%p")

    name_and_timestamp = export_data_name.upper().rstrip().lstrip().replace(" ","_") + "_" + start_time_path_formatted

    #set path for .txt dataset report
    if report_export == True:

        text_export_path = export_path +"TEXT_REPORT_" + name_and_timestamp + ".txt"
        sys.stdout = open(text_export_path, "w")

    author = "DANIEL CORCORAN"

    filepath = import_path

    sheet_name = excel_sheet_name

    threshold = distinct_threshold_int

    #validate export_data_type and report_data_type value
    if export_data_type != ".json" and export_data_type != ".html":
        export_data_type = ".csv"

    if report_data_type != ".json" and report_data_type != ".html":
        report_data_type = ".csv"

    #description detailing outputs of report component of script
    desc = "\n> Exports cleaned dataset as .csv/.html/.json (optional).\n> Exports summary report of cleaned dataset as .txt and .json.\n> Cleans column headers, left/right trim, uppercase, replacing spaces with underscores.\n> Cleans data by transforming to string, left/right trim and uppercase.\n> Displays current date time and time taken to process dataset.\n> Iterates through each column displaying; \n   >Column name\n   >Column number\n   >Null count and percent\n   >Non-null count and percent\n   >Numeric count and percent\n   >Non-numeric count and percent\n   >Duplication count and percent\n   >Count\n   >Distinct count\n   >Distinct count values\n   >Range value\n   >Max value\n   >Min value"

    #new list which will be used to store the dictionary created for each column, which will then be used to create the .json report
    dictionary_list = []

    #choose appropriate import method based on file type (note: assumed csv or excel contains headers)
    if ".csv" in filepath:
        my_data = pd.read_csv(filepath, low_memory = False, error_bad_lines = False, delimiter=data_delimeter)

    elif ".xlsx" in filepath:

        excel_data = pd.ExcelFile(filepath)
        my_data = pd.concat([excel_data.parse(sheet_name)], axis = 1)

    else:
        p("File neither .csv or .xlsx")

    #store dataframe's column headers into a list
    col_list = my_data.columns.get_values().tolist()

    #transform every column name in column list and replace existing dataframe column names with ones from list
    for column in col_list:

        my_data.rename(columns = {column:column.strip().upper().replace(" ","_")}, inplace = True)

    #insert cleaned column names into new list
    col_array_cleaned = my_data.columns.get_values()
    col_list_cleaned = col_array_cleaned.tolist()

    #trim dataframe left and right using regular expressions
    my_data.replace('(^\s+|\s+$)','', regex = True, inplace = True)

    #replace every column in dataframe with a string uppercase version
    my_data = pd.concat([my_data[col].astype(str).str.upper() for col in my_data.columns], axis=1)

    row_total = my_data.shape[0]
    col_total = my_data.shape[1]
    cell_total = row_total * col_total

    #print out high level details of dataset
    p("SCRIPT OUTPUTS: \n" + desc)
    p("DATASET SUMMARY: \n")
    sp("AUTHOR: %%", author)
    sp("DATASET PATH: %%", filepath)

    start_time_formatted = start_time.strftime("%d-%m-%Y %H:%M %p")

    sp("TIMESTAMP: %%", start_time_formatted)
    sp("DATASET ROW COUNT: %%", row_total)
    sp("DATASET COLUMN COUNT: %%", col_total)
    sp("DATASET CELL COUNT: %%", cell_total)
    sp("UNIQUE VALUE THRESHOLD: %%", threshold)


    #start looping through every column in cleaned column list
    for n in range(len(col_list_cleaned)):

        # create two lists, one for distinct values and one for every value from each column
        # also resets lists every iteration
        # create new dictionary to be appended to dictionary_list at the end of each loop

        distinct_values_list = []
        all_values_list = []
        dictionary = {}

        #assign high level summary information to dictionary
        dictionary["SUMM_AUTHOR"] = author
        dictionary["SUMM_DATASET_PATH"] = filepath
        dictionary["SUMM_TIMESTAMP"] = start_time.strftime("%d-%m-%Y %H:%M %p")
        dictionary["SUMM_ROW_COUNT"] = row_total
        dictionary["SUMM_COLUMN_COUNT"] = col_total
        dictionary["SUMM_CELL_COUNT"] = cell_total
        dictionary["SUMM_DIST_VALUE_THRESHOLD"] = threshold

        #add all unique values to one list
        for item in my_data[col_list_cleaned[n]].unique():
            distinct_values_list.append(item)

        #add all values to another list
        for item in my_data[col_list_cleaned[n]]:
            all_values_list.append(item)

        #sort list containing unique values
        distinct_values_list = sorted(distinct_values_list)

        #store length of distinct values list in variable
        distinct_list_length = len(distinct_values_list)

        #reset non null count variable every iteration of main loop
        nonnull_count = 0

        #calculate non null count (since column was transformed to string nulls will appear as "NAN" not as None)
        for y in all_values_list:
            if y != "NAN":
                nonnull_count = nonnull_count + 1

        #calculate percentage of convertable numerics in dataset

        float_convertibles = 0

        for item in all_values_list:
            try:
                float(item)
                float_convertibles = float_convertibles + 1
            except ValueError:
                pass

        non_float_convertibles = row_total - float_convertibles

        float_convertibles_percent = turn_to_perc(float_convertibles/row_total)
        non_float_convertibles_percent = turn_to_perc(non_float_convertibles/row_total)

        #calculate total rows in dataset, will be used to calculate null/non-null counts and percents

        null_count = row_total - nonnull_count

        nonnull_percent = turn_to_perc(nonnull_count/row_total)

        null_percent = turn_to_perc(null_count/row_total)

        max_columns = len(col_list)
        column_number = n + 1

        #calculate duplication
        # len(original_list) - len(unique_list)

        duplication_count = row_total - distinct_list_length
        duplication_count_percent = turn_to_perc(duplication_count/row_total)

        #append details to dictionary
        if threshold == len(distinct_values_list):
            condense = False
        else:
            condense = True

        column_name = col_list_cleaned[n]

        dictionary["COLUMN_NAME"] = column_name
        dictionary["COLUMN_NUMBER"] = column_number
        dictionary["NON_NULL_COUNT"] = nonnull_count
        dictionary["NON_NULL_COUNT_PERC"] = nonnull_percent
        dictionary["NULL_COUNT"] = null_count
        dictionary["NULL_COUNT_PERC"] = null_percent
        dictionary["NUMERIC_COUNT"] = float_convertibles
        dictionary["NUMERIC_COUNT_PERC"] = float_convertibles_percent
        dictionary["NON_NUMERIC_COUNT"] = non_float_convertibles
        dictionary["NON_NUMERIC_COUNT_PERC"] = non_float_convertibles_percent
        dictionary["COUNT"] = row_total
        dictionary["DISTINCT_COUNT"] = distinct_list_length
        dictionary["DUPLI_COUNT"] = duplication_count
        dictionary["DUPLI_COUNT_PERC"] = duplication_count_percent
        dictionary["DISTINCT_VALUES"] = distinct_values_list[:threshold]
        dictionary["DISTINCT_VALUES_CONDENSE"] = condense

        print("\n--------------------------------------------------------------------------------------\n")

        sp("COL NAME: '%%' (%%/%%)", column_name, column_number, max_columns)
        sp("NON-NULL: %% (%% %)",nonnull_count, format(nonnull_percent, ".2f"))
        sp("NULL: %% (%% %)",null_count, format(null_percent, ".2f"))
        sp("NUMERIC: %% (%% %)", float_convertibles, format(float_convertibles_percent, ".2f"))
        sp("NON-NUMERIC: %% (%% %)", non_float_convertibles, format(non_float_convertibles_percent, ".2f"))
        sp("COUNT: %%", row_total)
        sp("DISTINCT COUNT: %%",distinct_list_length)
        sp("DUPLICATION COUNT: %% (%% %)",duplication_count, format(duplication_count_percent, ".2f"))

        #print list of distinct values, usign threshold variable to shorten the list length exceeds threshold, and print out leftover elements

        if distinct_list_length <= threshold:
            sp("DISTINCT VALUES: %%", distinct_values_list)

        else:
            sp("DISTINCT VALUES: %%", distinct_values_list[:threshold])
            sp("* %% items were removed due to the list size exceeding threshold (%%)", (distinct_list_length - threshold), threshold)

        #calculate min and max values of list

        distinct_values_list_copy = distinct_values_list
        float_list = []
        reject_list = []

        while "NAN" in distinct_values_list_copy:
            distinct_values_list_copy.remove("NAN")

        for item in distinct_values_list_copy:
            try:
                float(item)
                float_list.append(float(item))
            except ValueError:
                reject_list.append(item)

        if len(reject_list) >= 1:

            max_value = max(distinct_values_list)
            min_value = min(distinct_values_list)
            range_value = "N/A"

        elif len(reject_list) < 1 and len(float_list) > 0:

            max_value = round(max(float_list),2)
            min_value = round(min(float_list),2)
            range_value = round((max_value - min_value),2)

        else:
            max_value = "N/A"
            min_value = "N/A"
            range_value = "N/A"

        mean_value = get_str_list_mean(all_values_list)
        median_value = get_str_list_median(all_values_list)

        sp("MAX: %%", max_value)
        sp("MIN: %%", min_value)
        sp("MEAN: %%", mean_value)
        sp("MEDIAN: %%", median_value)
        sp("RANGE: %%", range_value)

        dictionary["MIN_VALUE"] = min_value
        dictionary["MAX_VALUE"] = max_value
        dictionary["RANGE_VALUE"] = range_value
        dictionary["MEAN_VALUE"] = mean_value
        dictionary["MEDIAN_VALUE"] = median_value

        distinct_values_list_copy.clear()

        dictionary_list.append(dictionary)


    #calculate the time taken to run the whole script
    end_time = dt.datetime.now() - start_time

    #prints out time taken in seconds rounded to 3 decimal places
    total_seconds = round(end_time.total_seconds(),2)

    sp("\n--------------------------------------------------------------------------------------\n\nSCRIPT COMPLETED IN: %% SECONDS.\n", total_seconds)

    print("*this time excludes time taken to export cleaned dataset. Time taken to export cleaned dataset is included below.\n")

    for dict in dictionary_list:
        dict["SUMM_PROC_TIME"] = total_seconds

    #store clean dataset summary in dataframe
    cleaned_data_summary = pd.DataFrame(dictionary_list)

    #store current date time
    dt_now = dt.datetime.now().strftime("%d-%M-%Y %H:%M:%S %p")

    #EXPORT CLEANED DATASET AS .CSV OR .JSON

    start_data_export = dt.datetime.now()

    cleaned_data_string = "Cleaned dataset exported to '%%' in %% seconds, on %%, as type %%\n"

    if export_data == True:

        export_data_time = (dt.datetime.now() - start_data_export).total_seconds()

        if export_data_type == ".csv":
            data_export_path_csv = export_path + "\\CLEANED_" + name_and_timestamp + export_data_type
            my_data.to_csv(data_export_path_csv, index_label = "ROW_INDEX")
            sp(cleaned_data_string, data_export_path_csv, export_data_time, dt_now, export_data_type)

        elif export_data_type == ".json":
            data_export_path_json = export_path + "\\CLEANED_" + name_and_timestamp + export_data_type
            my_data.to_json(data_export_path_json)
            sp(cleaned_data_string, data_export_path_json, export_data_time, dt_now, export_data_type)

        elif export_data_type == ".html":
            data_export_path_html = export_path + "\\CLEANED_" + name_and_timestamp + export_data_type
            my_data.to_html(data_export_path_html)
            sp(cleaned_data_string, data_export_path_html, export_data_time, dt_now, export_data_type)

    # EXPORT REPORT AS HTML/CSV/JSON AND .TXT

    sp("Text report exported to %% at %%\n", text_export_path, dt_now)
    custom_export_path = export_path + "/REPORT_" + name_and_timestamp + report_data_type
    print(report_data_type)

    if report_export == True and report_data_type == ".csv":
        cleaned_data_summary.to_csv(custom_export_path, index_label = "ROW_INDEX")

    elif report_export == True and report_data_type == ".json":
        cleaned_data_summary.to_json(custom_export_path)

    elif report_export == True and report_data_type == ".html":
        cleaned_data_summary.to_html(custom_export_path)

    sp(report_data_type + " report exported to %% on %%\n", custom_export_path, dt_now)
    
    sys.stdout.close()


#Using gen_data_report with a folder containing multiple .csv, not recommended for folders containing large csvs
test_path = 'C:\\Users\\admin-vicvphq\\PycharmProjects\\untitled\\datasets\\TESTBULK'

#works for bulk .csv only at this point in time
def bulk_gen_data_report(path):
    file_name_clean_list = []
    file_name_path_list = []

    for file_name in os.listdir(path):

        #Check each file name if its a csv
        if file_name.endswith(".csv"):

            #turn file name into a list, to separate the extension from the name itself
            file_name_split = file_name.split(".")

            #store first element of new list in var, this will be the file name (dirty)
            file_name_dirty = file_name_split[0]

            #clean this file name variable using upper, strip and replace spaces with underscores
            file_name_clean = file_name_dirty.replace(" ","_").strip().upper()

            #add file name clean to list and file name path to a list, used as parameters in gen_data_report

            file_name_path = path + "\\" + file_name
            file_name_path_list.append(file_name_path)
            file_name_clean_list.append(file_name_clean)

    for n in range(len(file_name_clean_list)):

        gen_data_report(import_path = file_name_path_list[n],
                        excel_sheet_name = "Sheet1",
                        distinct_threshold_int = 20,
                        report_export = True,
                        report_data_type = ".html",
                        export_data = True,
                        export_data_type = ".csv",
                        export_data_name = file_name_clean_list[n])

expname = "VEHICLE"
fullpath = "/Users/danielcorcoran/Desktop/Vic Crash Stats (Extracted 4-5-2018)/"+expname+".csv"

gen_data_report(import_path= fullpath,
                        export_path= "/Users/danielcorcoran/Desktop/Report Generator/",
                        export_data_name= expname,
                        export_data_type=".csv",
                        excel_sheet_name="Sheet1",
                        distinct_threshold_int=20,
                        report_export=True,
                        report_data_type=".html",
                        export_data=False,
                        data_delimeter=",")
