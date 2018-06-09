import pandas as pd
import os

#alligns with lga_code_list, used as reference with index
filename_list = ["otlgaalpine.xlsx",
"otlgaararat.xlsx",
"otlgaballarat.xlsx",
"otlgabanyule.xlsx",
"otlgabasscoast.xlsx",
"otlgabawbaw.xlsx",
"otlgabayside.xlsx",
"otlgabenalla.xlsx",
"otlgaboroondara.xlsx",
"otlgabrimbank.xlsx",
"otlgabuloke.xlsx",
"otlgacampaspe.xlsx",
"otlgacardinia.xlsx",
"otlgacasey.xlsx",
"otlgacentralgoldfields.xlsx",
"otlgacolac-otway.xlsx",
"otlgacorangamite.xlsx",
"otlgadarebin.xlsx",
"otlgaeastgippsland.xlsx",
"otlgafrankston.xlsx",
"otlgagannawarra.xlsx",
"otlgagleneira.xlsx",
"otlgaglenelg.xlsx",
"otlgagreaterbendigo.xlsx",
"otlgagreaterdandenong.xlsx",
"otlgagreatergeelong.xlsx",
"otlgagreatershepparton.xlsx",
"otlgahepburn.xlsx",
"otlgahindmarsh.xlsx",
"otlgahobsonsbay.xlsx",
"otlgahorsham.xlsx",
"otlgahume.xlsx",
"otlgaindigo.xlsx",
"otlgakingston.xlsx",
"otlgaknox.xlsx",
"otlgalatrobe.xlsx",
"otlgaloddon.xlsx",
"otlgamacedonranges.xlsx",
"otlgamanningham.xlsx",
"otlgamansfield.xlsx",
"otlgamaribyrnong.xlsx",
"otlgamaroondah.xlsx",
"otlgamelbourne.xlsx",
"otlgamelton.xlsx",
"otlgamildura.xlsx",
"otlgamitchell.xlsx",
"otlgamoira.xlsx",
"otlgamonash.xlsx",
"otlgamooneevalley.xlsx",
"otlgamoorabool.xlsx",
"otlgamoreland.xlsx",
"otlgamorningtonpeninsula.xlsx",
"otlgamountalexander.xlsx",
"otlgamoyne.xlsx",
"otlgamurrindindi.xlsx",
"otlganillumbik.xlsx",
"otlganortherngrampians.xlsx",
"otlgaportphillip.xlsx",
"otlgapyrenees.xlsx",
"otlgasoutherngrampians.xlsx",
"otlgasouthgippsland.xlsx",
"otlgastonnington.xlsx",
"otlgastrathbogie.xlsx",
"otlgasurfcoast.xlsx",
"otlgaswanhill.xlsx",
"otlgatowong.xlsx",
"otlgawangaratta.xlsx",
"otlgawarrnambool.xlsx",
"otlgawellington.xlsx",
"otlgawestwimmera.xlsx",
"otlgawhitehorse.xlsx",
"otlgawhittlesea.xlsx",
"otlgawodonga.xlsx",
"otlgawyndham.xlsx",
"otlgayarra.xlsx",
"otlgayarraranges.xlsx",
"otlgayarriambiack.xlsx"]
#alligns with filename_list, used as reference with index
lga_code_list = [20110,
20260,
20570,
20660,
20740,
20830,
20910,
21010,
21110,
21180,
21270,
21370,
21450,
21610,
21670,
21750,
21830,
21890,
22110,
22170,
22250,
22310,
22410,
22620,
22670,
22750,
22830,
22910,
22980,
23110,
23190,
23270,
23350,
23430,
23670,
23810,
23940,
24130,
24210,
24250,
24330,
24410,
24600,
24650,
24780,
24850,
24900,
24970,
25060,
25150,
25250,
25340,
25430,
25490,
25620,
25710,
25810,
25900,
25990,
26260,
26170,
26350,
26430,
26490,
26610,
26670,
26700,
26730,
26810,
26890,
26980,
27070,
27170,
27260,
27350,
27450,
27630,]

full_data = pd.DataFrame()

#input folder, path containing lga excel files
#note: make sure only excel files are in this folder
folder_path = "C:/Users/admin-vicvphq/Desktop/lga_ontrack/"

#output folder
output_path = "C:/Users/admin-vicvphq/Desktop/output/"

#start iterating through each excel file in input path
for filename in os.listdir(folder_path):

    #find the lga code for current file name
    index_of_file_name_in_list = filename_list.index(filename)
    lga_code = lga_code_list[index_of_file_name_in_list]

    #import data from current filename
    data = pd.read_excel(folder_path + filename)

    #store first column as list, to find the start of the targetted table
    #the first row contains 'In Education or Training'
    first_col_list = data["Unnamed: 0"].tolist()
    for index in range(len(first_col_list)):
        if "In Education or Training" == first_col_list[index]:
            found_index = index
            break
    #table size is fixed and is 17 rows long, so adding 16 creates that table
    data2 = data[found_index:found_index + 16]

    #clean the data by dropping all columns with 100% nulls and reset the index
    data3 = data2.dropna(how="all", axis=1)
    data3 = data3.reset_index()

    #create a list containing the lga code to append to the data
    lga_code_col_list = []
    for index in range(data3.shape[0]):
        lga_code_col_list.append(lga_code)

    #append lga code list as a series to the data, reset index and drop old index column
    data4 = pd.concat([data3, pd.Series(lga_code_col_list)],axis = 1)
    data4 = data4.reset_index()
    data4 = data4.drop(["index"], axis = 1)

    #rename columns appropriately
    data4.columns = ["INDEX", "CATEGORY", "LGA_COUNT","LGA_PERCENT","VIC_COUNT","VIC_PERCENT", "LGA_CODE"]

    #export data in current iteration (for single lga)
    data4.to_excel(output_path + "ontrack2017_ " + str(lga_code) + ".xlsx")

    #append data in current iteration to full_data dataframe
    full_data = pd.concat([full_data, data4], axis=0)

#export the full data (containing all LGAs)
full_data.to_excel(output_path + "ontrack2017_fulldata.xlsx", index = False)