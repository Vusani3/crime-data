import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

YEAR = 2004
CURRENT_YEAR = 2023
extracted_info = []
headers = {
    "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "Accept": "text/plain, */*; q=0.01",
    "Referer": "https://www.crimestatssa.com/index.php",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Linux"',
}

while YEAR <= 2023:
    URL = f"https://www.crimestatssa.com/ajax/getData.php?v8&crimecats=&year={YEAR}&province="
    response = requests.get(URL, headers=headers, verify=False)
    data = response.json
    data = eval(response.text)

    for item in data:
        name = item[2]
        value = item[3]
        year = YEAR
        extracted_info.append((name, year, value))
    YEAR += 1

    # Create a DataFrame
df = pd.DataFrame(extracted_info, columns=["Name", "Year", "Value"])
final_data = []
for index, row in df.iterrows():
    name = row["Name"]
    value = row["Value"]
    year = row["Year"]
    params = {
        "id": f"{value}",
        "crimecats": "",
        "year": f"{year}",
        "geoloc": "false",
    }

    response = requests.get(
        "https://www.crimestatssa.com/ajax/getDetails.php",
        params=params,
        headers=headers,
        verify=False,
    )
    crime = BeautifulSoup(response.text, "html.parser").find("span", class_="badge")
    time.sleep(10)
    if crime:
        crime = crime.get_text()
        span_tag = BeautifulSoup(response.text, "html.parser").find(
            "span", style="color:#95191c"
        )
        name = span_tag.get_text()
        print(crime)
        print(name)
        print(year)
    else:
        crime = 0
    final_data.append((name, year, crime))
    # Save DataFrame to a CSV file
    csv_filename = "data.csv"
    dataset = pd.DataFrame(final_data, columns=["Name", "Year", "Crime"])
    dataset.to_csv(csv_filename, index=False)
print("DataFrame saved as CSV:", csv_filename)
