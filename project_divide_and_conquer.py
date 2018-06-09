import pandas as pd
import datetime as dt
import time
import pygal
from pygal import style

data = pd.read_csv(r"H:\Data\daniel_corcoran_python_files\datasets\ACCIDENT.csv", low_memory= False)

print(data.columns)
dictionaries = {}

#mandatory fields
measure_column_name = ''
columns_list = []
wanted_columns = []
all_the_columns = data.columns

def remove_unwanted_columns(all_the_columns, wanted_columns):
    for item in all_the_columns:
        if item not in wanted_columns:
            all_the_columns.remove(item)

    return all_the_columns

def print_all_columns(data):
    columns = data.columns
    print(columns)

def process(data, columns_list, measure_column_name):
    for column_name in columns_list:

        sub_dictionary = {}
        keys_list = []
        values_list = []

        group = data.groupby([column_name])[measure_column_name].sum()
        dict_group = dict(group)

        for key in dict_group.keys():
            keys_list.append(key)
            values_list.append(group[key])

        total = sum(values_list)

        for n in range(len(keys_list)):
            sub_dictionary[keys_list[n]] = round(values_list[n]/total,4)
        dictionaries[column_name] = sub_dictionary
    return dictionaries

#using process method to aggregate and gather percentages from accidents.csv for speed zone columns
result = process(data, columns_list = ['SPEED_ZONE'], measure_column_name = 'NO_PERSONS_KILLED')

for key in result.keys():
    print(key)
    print(result[key])

speed = result['SPEED_ZONE']

#create new gauge object from pygal
gauge = pygal.SolidGauge(half_pie = False, inner_radius = 0.7, style = style.LightColorizedStyle)
gauge.title=  "VICROADS CRASH STATS FATALITIES BY SPEED ZONE"

#iterate through results from process method and add to gauge as values
for key in speed.keys():
    if key <= 110 and key >= 0:
        gauge.add(str(key) + " km/h zone.",
                  [{'value':speed[key]*100,'label':'percentage of total fatalities.'}],
                  formatter = lambda x:'{0:.2f}%'.format(x))

gauge.render_in_browser()
gauge.render_to_file('gauge.svg')

# pie = pygal.Pie(print_values = True,
#                 inner_radius = .6,
#                 style = style.LightColorizedStyle,
#                 legend_at_bottom = True)
#
# pie.title = "VICROADS FATALITIES BY ZONE"
# for key in speed.keys():
#     if key <= 110 and key >= 0:
#         pie.add("zone: " + str(key), speed[key], formatter = lambda x:'{0:.2f}%'.format(x * 100))
# pie.render_in_browser()