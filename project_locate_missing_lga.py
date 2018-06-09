import pandas
import numpy

#sheet6 (couldve been named better), contains values for each indicator on lga grain
data = pandas.read_excel("C:/Users/admin-vicvphq/Desktop/sheet6.xlsx",
                         sheet_name = "Sheet6")

#use below to find columns in dataset
print(data.columns)

#create list of relevant columns (all except 'LGA_NAME')
rel_columns = [1.1,1.2,1.3,2.1,2.2,
3.1,3.2,4.1,4.2,4.3,4.4,
5.1,5.2,5.3,6.1,6.2,6.3,
7.1,7.2,7.3,7.4,8.1,8.2,
8.3,8.4,9.1,9.2,9.3,9.4]

#start iterating through column names in rel_columns list
for column in rel_columns:
    print("\nCHECKING ON COLUMN :: " + str(column))
    #create list to store lga names with missing values for current iteration
    no_value_lgas=[]
    #for each index in number of rows
    for index in range(data.shape[0]):
        #store current value of row in iteration with column of upper loop
        current_value = data.loc[index, column]
        #if value is NaN (not a number), append to the no_value_lgas list
        if numpy.isnan(current_value):
            lga = data.loc[index, "LGA_NAME"]
            no_value_lgas.append(lga)
    #print results
    print("Missing LGA List: " + str(no_value_lgas))
    print("Number of missing LGAs: "+str(len(no_value_lgas)))
