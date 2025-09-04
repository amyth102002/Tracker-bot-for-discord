from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


def get_transaction_links():
    url="https://gunzscan.io/txs"
    # page=requests.get(url)
    options=webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver=webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,"html.parser")

    #Transaction Links#

    transactions_links=[]
    for a in soup.find_all("a",class_="chakra-link css-conlb5"):
        href=a.get("href")
        if href and href.startswith("/tx/"):
            transactions_links.append("https://gunzscan.io"+href)
    driver.quit()
    return transactions_links

def filter_links(links):
    nft_links=[]
    options=webdriver.ChromeOptions()
    


# if __name__ == "__main__":
#     links=get_transaction_links()
#     for link in links[:10]:
#         print(link)

