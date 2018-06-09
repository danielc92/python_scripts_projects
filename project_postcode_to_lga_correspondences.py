import pandas
import datetime

#import excel data, specifying sheet name also
data = pandas.read_excel("C://Users/admin-vicvphq/PycharmProjects/datasets/postcode_to_lga_correspondences.xls",
                         sheetname = "Table 3")

#store relevant column headers in variables
postcode_column_name = "POSTCODE"
lga_code_column_name = "LGA_CODE_2011"
value_column_name = "PERCENTAGE"


#create new list to store output lga codes
row_iterator = data.shape[0]
lga_with_max_value_list = []

#iterate through each row index of data
#create sub data set, find maximum value
#find lga code for that value, append code to lga_with_max_value_list

for index in range(row_iterator):

    #store postcode from current row
    current_postcode = data.loc[index, postcode_column_name]

    #create sub data set using current postcode
    sub_data = data[data[postcode_column_name] == current_postcode]
    sub_data = sub_data.reset_index()

    #store row index of maximum value in sub data
    index_of_maximum_value = sub_data[value_column_name].idxmax()

    #find lga code of the maximum value within the sub data set and append to the lga_with_max_value_list
    lga_code_of_maximum_value = sub_data[lga_code_column_name][index_of_maximum_value]
    lga_with_max_value_list.append(lga_code_of_maximum_value)

#create new dataframe combining original with lga codes
data2 = pandas.concat([data, pandas.Series(lga_with_max_value_list).rename("LGA_MAX")], axis = 1)

#create timestamp
stamp = datetime.datetime.now()
string_stamp = stamp.strftime("(d%d%m%y_t%H%M)")

#export new data with timestamp appended
data2.to_csv("data"+string_stamp+".csv")