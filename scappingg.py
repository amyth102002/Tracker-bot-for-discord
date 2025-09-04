from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

BASE_URL = "https://gunzscan.io"

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_transaction_links(driver, max_links=200):
    url = f"{BASE_URL}/txs"
    driver.get(url)
    time.sleep(5)  # wait for tx list to load
    print(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []

    for a in soup.find_all("a", class_="chakra-link css-conlb5"):
        href = a.get("href")
        if href and href.startswith("/tx/"):
            links.append(BASE_URL + href)
        if len(links) >= max_links:
            break

    return links

def filter_nft_links(driver, tx_links, min_nfts=10):
    nft_links = []
    wait = WebDriverWait(driver, 5)

    for link in tx_links:
        driver.get(link)
        try:
            # wait only for NFT heading
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.chakra-heading.css-1co3o29")))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            nft_detail = soup.find("h2", class_="chakra-heading css-1co3o29")
            if nft_detail:
                nft_links.append({"name": nft_detail.get_text(strip=True), "link": link})
        except:
            pass  # no NFT here, skip

        if len(nft_links) >= min_nfts:
            break

    return nft_links

if __name__ == "__main__":
    driver = get_driver()

    # Step 1: grab ~200 transaction links
    tx_links = get_transaction_links(driver, max_links=200)

    # Step 2: filter NFT ones
    nft_results = filter_nft_links(driver, tx_links, min_nfts=10)

    driver.quit()

    # Print results
    for nft in nft_results:
        print(f"{nft['name']} -> {nft['link']}")
