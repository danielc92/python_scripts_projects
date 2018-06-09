import pandas as pd
import numpy as np

with open("datasets\\englishdictionary_clean.txt", "r") as ins:
    word_list = []

    for line in ins:
        word_list.append(line)

big_list = []
for string in word_list:
    small_list = []
    small_list.append(string.split(","))
    big_list.extend(small_list)

dict = {}

alpha_list = []
type_list = []

for n in range(len(big_list)):
    alpha_list.append(big_list[n][0])
    type_list.append(big_list[n][1])

for n in range(len(alpha_list)):
    alpha_list[n] = alpha_list[n].replace("'","")
    type_list[n] = type_list[n].replace("'","")

print(alpha_list)
print(type_list)

alpha_series = pd.Series(alpha_list)
type_series = pd.Series(type_list)

data = pd.concat([alpha_series, type_series], axis = 1)

print(data.head(5))

data.rename(columns = {0: "word_name", 1: "word_type"}, inplace = True)

print(data.head(5))

data.to_csv("datasets/english_words_types.csv",index_label = 'row_index')