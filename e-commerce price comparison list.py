from bs4 import BeautifulSoup
import requests 
import numpy as np
import csv
from datetime import datetime

LINK ="https://www.amazon.ca/?tag=hydcaabkg-20&hvadid=677796472754&hvpos=&hvnetw=g&hvrand=15072934465970188752&hvpone=&hvptwo=&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1002131&hvtargid=kwd-31636821&ref=pd_sl_2gqjnc4wf3_e&hydadcr=11828_13481604"


def get_prices_by_link(link):
    r = requests.get(link)
    page_parse = BeautifulSoup(r.text, 'html.parser')
    search_results = page_parse.find("ul",{"class":"srp-results"}).find_all("li",{"class":"s-item"})

    item_prices = []

    for result in search_results:
        price_as_text = result.find("span",{"class":"s-item__price"}).text
        if "to buy" or "To Buy" in price_as_text:
            continue
        price = float(price_as_text[1:].replace(",",""))
        item_prices.append(price)
    return item_prices

def remove_outliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def get_average(prices):
    return np.mean(prices)

def save_to_file(prices):
    fields=[datetime.today().strftime("%B-%D-%Y"),np.around(get_average(prices),2)]
    with open('prices.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == "__main__":
    prices = get_prices_by_link(LINK)
    prices_without_outliers = remove_outliers(prices)
    print(get_average(prices_without_outliers))
    save_to_file(prices)
    



    
    