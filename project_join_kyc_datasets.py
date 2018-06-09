import os
import pandas

#create a dataframe to store all the sub datasets in
full_data = pandas.DataFrame()

#folder containing all the csv files for each council from the 'work_pull_councils' script
path = "C:/Users/admin-vicvphq/danielc_pycharm_project/projects_work/kyc_Data/"

#for each filename in path do this
for filename in os.listdir(path):

    #store csv as dataframe
    data = pandas.read_csv(path + filename)

    #rename the columns so that they can be unioned with one another
    new_columns = ['SERVICE AREA', 'INDICATOR', 'MEASURE DESCRIPTION',
       "LGA_DATA", 'SIMILAR COUNCILS', 'ALL COUNCILS', 'TREND',
       'COUNCIL SAYS']
    data.columns = new_columns

    #create a new column that appends the filename, so that council can be identified in the full dataframe
    list = []
    for n in range(data.shape[0]):
        list.append(filename)

    series = pandas.Series(list)

    data2 = pandas.concat([data, series.rename("FILE_NAME")], axis = 1)

    #join data to full data
    full_data = pandas.concat([full_data, data2], axis = 0)

#Export data
full_data.to_csv("full_data_kyc.csv")