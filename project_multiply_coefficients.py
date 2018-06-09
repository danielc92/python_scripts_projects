import pandas
import math

intercept = 1.25
column_names = ["x1","x2","x3"]
coefficients = [.6,-.7,.0001]

data = pandas.DataFrame({
    "x1":[.1,.4,.4,.6,.3],
    "x2":[3,4,3,2,7],
    "x3":[1,2,5,4,3],
    "y":[1,0,1,1,0]})

match_column_name = "_matchIndicator"
correct_output_column_name = "y"
predicted_output_column_name = "_predictedOutcome"

partial_total = intercept

number_of_columns = len(column_names)

for index in range(number_of_columns):
    partial_total = partial_total + data[column_names[index]] * coefficients[index]

full_formula = 1/(1 + math.exp(1) ** - (partial_total))

print("•"*200)

data = pandas.concat([data, full_formula.ge(.5).replace([True, False],[1, 0]).rename(predicted_output_column_name)], axis = 1)

print(data)

print("•"*200)

match_list = []

number_of_rows = data.shape[0]

for row_number in range(number_of_rows):
    if data[predicted_output_column_name][row_number] == data[correct_output_column_name][row_number]:
        match_list.append(1)
    else:
        match_list.append(0)

data_output = pandas.concat([data, pandas.Series(match_list).rename(match_column_name)], axis = 1)

print(data_output)

accuracy = data_output[match_column_name].sum()/data_output.shape[0]


print(str(accuracy * 100) + " %")































