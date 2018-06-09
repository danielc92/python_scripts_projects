import bs4
import requests

request = requests.get("https://knowyourcouncil.vic.gov.au/councils")
request_text = request.text
soup = bs4.BeautifulSoup(request_text, "lxml")

council_links_box = soup.find("div", {"class":"myc-promo council-list-section"})

council_links = council_links_box.find_all("a")

links_dictionary = {}

for link in council_links:

    url = link.get("href")
    council_name = link.text
    links_dictionary[council_name]=url

    request = requests.get(url)
    request_text = request.text
    soup = bs4.BeautifulSoup(request_text, "lxml")

    download_links_box = soup.find("ul", {"class":"download-options kyc-dropdown-menu"})
    download_links_group = download_links_box.find_all("a")

    for link in download_links_group:
        text = link.text
        if text == "Results CSV":
            csv_download_url = link.get("href")
            r = requests.get(csv_download_url, allow_redirects = True)
            open("C:/Users/admin-vicvphq/danielc_pycharm_project/projects_work/kyc_Data/" +council_name + ".csv", "wb").write(r.content)

