import pandas
import math

#store the intercept, column names, coefficients and output column from the logistic regression model
#note: these variables/lists were manually pasted from the logistic regression notebook outputs

intercept = -0.08866126

column_names = ['height_B', 'reach_A', 'won_B', 'lost_A', 'lost_B', 'drawn_A',
       'drawn_B', 'kos_B', 'age_diff', 'kd_diff_B', 'stance_A_southpaw',
       'stance_B_southpaw']

coefficients = [-0.07613955130631525, 0.08792269033144667, 0.012717343788134591, 0.06382816324456637, 0.04079810288500522, 0.23641979547725042, 1.1385042268091596, -0.02620634884784423, -0.21677967396359427, -0.028080759096910084, 0.4008830872886278, 0.4008830872886278]

output_y = "result"

#read in test data, this was the subset exported from the larger dataset
data = pandas.read_csv("/Users/danielcorcoran/PycharmProjects/daniels_mac_proj/jupyter_notebooks/logistic regression/boxing_last_x_records.csv")

partial_total = intercept

#calculate the predicted value using logistic regression formula
for index in range(len(column_names)):
    partial_total = partial_total + data[column_names[index]] * coefficients[index]

full_formula = 1/(1 + math.exp(1) ** - (partial_total))

#calculate a column which rounds predicted outcome to 0 or 1
# 1 if greater than 0.5, 0 if less than 0.5
data = pandas.concat([data, full_formula.ge(.5).replace([True, False],[1, 0]).rename("_ypred")], axis = 1)

old_result_list = data[output_y].tolist()
new_result_list = data["_ypred"].tolist()

total_possible = len(old_result_list)

match_list = []

for n in range(len(old_result_list)):
    if old_result_list[n] == new_result_list[n]:
        match_list.append(1)
    else:
        match_list.append(0)

data = pandas.concat([data, pandas.Series(match_list).rename("_matchflag")], axis = 1)

print(data)

accuracy = data["_matchflag"].sum()/data.shape[0]

print(str(accuracy * 100) + " %")

data.to_csv("boxing.csv")