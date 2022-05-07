import lxml
import requests
from bs4 import BeautifulSoup
import json
import csv
"""
url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

request_url = requests.get(url)

src = request_url.text

with open("index.html", 'w', encoding='utf-8') as file:
    file.write(src)
"""

"""
with open("index.html", 'r', encoding="utf-8") as file:
    f_read = file.read()

soup = BeautifulSoup(f_read, 'lxml')
all_products_links = soup.find_all(class_="mzr-tc-group-item-href")

all_categories = dict()
for item in all_products_links:
    item_text = item.text
    item_link = "https://health-diet.ru" + item.get("href")
    all_categories[item_text] = item_link
    
with open("all_categories_links.json", 'w', encoding="utf-8") as file:
    json.dump(all_categories, file, indent=4, ensure_ascii=False)
"""

all_categories = []
with open("all_categories_links.json", 'r', encoding="UTF-8-sig") as file:
    all_categories = json.load(file)

count = 0
print(f"Total iterations: {len(all_categories) - 1}")
#data = []
for cat_name, cat_link in all_categories.items():
    replace_sym = [",", " ", "-", "'"]
    for item in replace_sym:
        if item in cat_name:
            cat_name = cat_name.replace(item, "_")
    request_url = requests.get(cat_link)
    res = request_url.text
    with open(f"data/{count}_{cat_name}.html", 'w', encoding="UTF-8-sig") as file:
        file.write(res)

    with open(f"data/{count}_{cat_name}.html", 'r', encoding="UTF-8-sig") as file:
        f_read = file.read()

    soup = BeautifulSoup(f_read, 'lxml')

    alert_block = soup.find(class_="uk-alert-danger")
    if (alert_block is not None):
        continue

    all_data = soup.find(class_="mzr-tc-group-table").find('tr').find_all('th')

    product_type = 'Type'
    product_name = all_data[0].text
    product_calories = all_data[1].text
    product_proteins = all_data[2].text
    product_fats = all_data[3].text
    product_carbohydrates = all_data[4].text

    with open(f"data/{count}_{cat_name}.csv", 'w', encoding="UTF-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow((product_type,
                         product_name,
                         product_calories,
                         product_proteins,
                         product_fats,
                         product_carbohydrates))
    if (count == 0):
        with open(f"all_categories_info.csv", 'w', encoding="UTF-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((product_type, product_name,
                             product_calories,
                             product_proteins,
                             product_fats,
                             product_carbohydrates))

    products_info = soup.find(class_="mzr-tc-group-table").find('tbody').find_all('tr')

    for item in products_info:
        product_type = cat_name
        product_info = item.find_all('td')
        product_name = product_info[0].find('a').text
        product_calories = product_info[1].text
        product_proteins = product_info[2].text
        product_fats = product_info[3].text
        product_carbohydrates = product_info[4].text

        """
        data.append({"Product": product_info,
                    "Calories": product_calories,
                     "Proteins": product_proteins,
                     "Fats": product_fats,
                    "Carbohydrates": product_carbohydrates})"""

        with open(f"data/{count}_{cat_name}.csv", 'a', encoding="UTF-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((product_type,
                             product_name,
                             product_calories,
                             product_proteins,
                             product_fats,
                             product_carbohydrates))

        with open(f"all_categories_info.csv", 'a', encoding="UTF-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((product_type, product_name,
                             product_calories,
                             product_proteins,
                             product_fats,
                             product_carbohydrates))

#    with open("all_categories_info.json", 'a', encoding="UTF-8-sig") as file:
 #       json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"{count}_{cat_name}_downloaded")
    count += 1
