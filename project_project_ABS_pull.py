import requests
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd

######INPUTS######
base_path ="H:/Data/daniel_corcoran_python_files/datasets/abs/"

#base_url = "http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/3222.02012%20(base)%20to%202101?OpenDocument"
base_url = "http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/3412.02015-16?OpenDocument"

#create dictionary for csv creation
dict = {
    "abs_title_main": [], #1 title main
    "abs_release_date": [], #2 release date
    "abs_base_url": [], #3 base url
    "date_extracted": [], #4 date extracted
    "abs_file_desc":[], #5 file description
    "abs_file_dir_name":[], #6 file dir name
    "abs_file_down_link":[], #7 file download link
    "abs_file_size":[] # 8 file size
}


#4 date extracted
current_dt = dt.datetime.now()

#create soup
response = requests.get(base_url)
response_text = response.text
soup = BeautifulSoup(response_text, "lxml")

def abs_clean(text):
    while "  " in text:
        text = text.replace("  "," ") #remove ALL double spaces
    text = text.replace(",", " |") #remove commas
    text = text.replace("\n","") #remove new lines
    return text

def get_default_release_date(release_text):

    default_release_date_string = release_text.strip()
    default_release_date_list = default_release_date_string.split(" ")
    default_release_date_text = default_release_date_list[len(default_release_date_list) - 1]
    default_release_full = "Released " + default_release_date_text

    return default_release_full

#1 title main
title_resultset = soup.find_all("div", {"id":"titlemain"})
title_text = title_resultset[0].text
title_text = abs_clean(title_text)


#2 release date
release_resultset = soup.find_all("div", {"id":"Release"})
release_text = release_resultset[0].text
release_text = abs_clean(release_text)


#create resultset for all tr elements of listentry class
listentry_resultset = soup.find_all("tr", {"class":"listentry"})


#add only xls rows to the xls_list
xls_html_list = []
xls_name_list = []

for item in listentry_resultset:
    string_item = str(item)
    if ".xls" in string_item:
        xls_html_list.append(item)
        abs_file_desc = item.text
        abs_file_desc = abs_clean(abs_file_desc)
        xls_name_list.append(abs_file_desc)


total_items = len(xls_html_list)
print("This url contains "+ str(total_items) +" .xls downloadable files")

for n in range(len(xls_html_list)):
    #print("___________________________________________________________________________________________\n")

    html = xls_html_list[n]
    file_number = str(n+1) #n starts at 0 but file number starts 1

    # create default release date variable for elements without a 'Released' class
    # to be overriden if class of Released EXISTS
    default_release_full = get_default_release_date(release_text)

    #start timer
    start = dt.datetime.now()


    #find and clean href link containins .xls only
    href_code = html.select_one("a[href*=.xls]")
    dirty_href = href_code.get("href")

    rel = html.find("td", {"class":"release"})
    rel_string = str(rel)

    #determine if release date needs to be updated to one in table element
    if "Released" in rel_string:
        rel_index = rel_string.find("Released")
        rel_substring = rel_string[rel_index:len(rel_string)-1]
        substring_index = rel_substring.find("</td")
        rel_substring2 = rel_substring[0:substring_index]
        release = rel_substring2.strip()
        #print(release)
    else:
        release = default_release_full
        #print(release)

    #find and clean href link
    clean_href = dirty_href.replace(" ","%20").replace("&amp;","&")
    full_clean_href = "http://www.abs.gov.au" + clean_href


    #find file name and append to base directory
    index_start = clean_href.find("openagent&")
    index_end = clean_href.find(".xls")
    file_name = clean_href[index_start + 10: index_end + 4]
    download_directory_path = base_path + file_name


    #gather file size and convert from bytes to megabytes
    file_size_bytes = requests.get(full_clean_href, stream= True).headers['Content-length']
    file_size_megabytes = float(file_size_bytes) / 1048576


    try:
        response = requests.get(full_clean_href)
        if response.status_code == 200:
            with open(download_directory_path, "wb") as f:
                f.write(response.content)
        print(file_number + "/" + str(total_items) + ". " + full_clean_href + " \nHas successfully downloaded to " + download_directory_path + " in "+ str(dt.datetime.now()-start))

        # create dictionary storing abs base_url/file details
        # each iteration of this equates to one record in the table
        dict["abs_title_main"].append(title_text)
        dict["abs_release_date"].append(release_text)
        dict["abs_base_url"].append(base_url)
        dict["date_extracted"].append(current_dt)
        dict["abs_file_desc"].append(xls_name_list[n])
        dict["abs_file_dir_name"].append(download_directory_path)
        dict["abs_file_down_link"].append(full_clean_href)
        dict["abs_file_size"].append(file_size_megabytes)

    #handle error
    except:
        print(full_clean_href + " has failed downloading.")


#turn dict into dataframe
data = pd.DataFrame(dict)
data.to_csv(base_path + "abs_log.csv", index_label= "row_index", sep = "^")
