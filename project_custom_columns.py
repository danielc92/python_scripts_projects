import pandas as pd
import os
import numpy as np
import datetime as dt

#removes single column from dataframe

def del_columns(my_data,
                col_name = ""):
    my_data = my_data.drop([col_name], axis = 1, inplace = True)
    return my_data

def trim_dataset(data,
                 transformation = "none"):

    #transformation options; none, upper, lower, proper
    transformation = transformation.lower().strip()

    if transformation != "none" and transformation != "upper" and transformation != "proper" and transformation != "lower":
        transformation = "none"
    print(transformation)
    dictionary = {}

    for column in data.columns:

        temp_list = data[column].tolist()

        if transformation == "none":
            pass

        elif transformation == "lower":
            for n in range(len(temp_list)):
                temp_list[n] = str(temp_list[n]).strip().lower()

        elif transformation == "upper":
            for n in range(len(temp_list)):
                temp_list[n] = str(temp_list[n]).strip().upper()

        elif transformation == "proper":
            for n in range(len(temp_list)):
                temp_list[n] = str(temp_list[n]).strip().capitalize()

        dictionary[column] = temp_list

    new_data = pd.DataFrame(dictionary)

    return new_data

def left_column(data,
                old_column_name = "",
                new_column_name = "",
                chars = 1):

    if new_column_name == "":
        new_column_name = old_column_name + "_left_" + str(chars)
    else:
        pass

    old_values = []

    for value in data[old_column_name]:
        old_values.append(str(value))

    print(old_values)

    new_values = []

    for value in old_values:
        new_values.append(value[:chars])

    print(new_values)

    series = pd.Series(new_values)

    data = pd.concat([data, series], axis = 1)

    data.rename(columns = {0: new_column_name}, inplace = True)

    return data

def right_column(data,
                old_column_name = "",
                new_column_name = "",
                chars = 1):

    if new_column_name == "":
        new_column_name = old_column_name + "right_" + str(chars)
    else:
        pass

    old_values = []

    for value in data[old_column_name]:
        old_values.append(str(value))

    print(old_values)

    new_values = []

    for value in old_values:
        new_values.append(value[chars:])

    print(new_values)

    series = pd.Series(new_values)

    data = pd.concat([data, series], axis = 1)

    data.rename(columns = {0: new_column_name}, inplace = True)

    return data

def upper_column(data,
                old_column_name = "",
                new_column_name = ""):

    if new_column_name == "":
        new_column_name = old_column_name + "_upper"

    old_values = []

    for value in data[old_column_name]:
        old_values.append(str(value))

    print(old_values)

    new_values = []

    for value in old_values:
        new_values.append(value.upper())

    print(new_values)

    series = pd.Series(new_values)

    data = pd.concat([data, series], axis = 1)

    data.rename(columns = {0: new_column_name}, inplace = True)

    return data

def lower_column(data,
                old_column_name = "",
                new_column_name = ""):

    if new_column_name == "":
        new_column_name = old_column_name + "_lower"

    old_values = []

    for value in data[old_column_name]:
        old_values.append(str(value))

    print(old_values)

    new_values = []

    for value in old_values:
        new_values.append(value.lower())

    print(new_values)

    series = pd.Series(new_values)

    data = pd.concat([data, series], axis = 1)

    data.rename(columns = {0: new_column_name}, inplace = True)

    return data

dictionary = {"name" : ["daniel corcoran", "james cole", "jennifer green", "jessica bartik"],
              "age" : [50,41,42,67],
              "title" : ["mr", "mr", "mrs", "ms"]}

data = pd.DataFrame(dictionary)

# l = []
# for col in data.columns:
#     l.append(col.strip().upper())
# data.columns = l
# print(data)

for col in data.columns:
    col = data.rename(columns = {col : col.strip().upper()}, inplace = True)
    print(col)
print(data)
# split = data["name"].astype(str).str.split(" ")
#
# s1 = []
# s2 = []
#
# for item in split:
#     print(item)
#     print(item[0])
#     print(item[1])
#     s1.append(item[0])
#     s2.append(item[1])
#
# print(s1)
# print(s2)
#
# split_data = pd.concat([pd.Series(s1), pd.Series(s2), data], axis = 1)
#
# print(split_data)