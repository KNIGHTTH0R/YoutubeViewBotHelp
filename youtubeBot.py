import random, time, requests
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup

USER_AGENTS_FILE = "./user_agents.txt"
RUNNING = True

def LoadUserAgents(uafile=USER_AGENTS_FILE) :
    uas = []
    with open (uafile, "rb") as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas

uas = LoadUserAgents()

while RUNNING == True:
    address = []

    response = requests.get("https://www.sslproxies.org")
    soup = BeautifulSoup (response.content, "html.parser")

    rows = soup.findAll("tr")
    
    for row in rows:
        if(len(row.findAll("td")) == 8):
            address.append(row.contents[0].contents[0] + ":" + row.contents[1].contents[0])
  

    random.shuffle(address)
    PROXY = random.choice(address)
    proxy = Proxy({
        "proxyType": ProxyType.MANUAL,
        "httpproxy": PROXY,
        "httpsproxy": PROXY,
        "ftpproxy": PROXY,
        "sslproxy": PROXY,
        "no proxy": ""
        })

    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", random.choice(uas))
    driver = webdriver.Firefox(firefox_profile=profile, proxy=proxy)
    driver.set_page_load_timeout(10)
    try:    
        driver.get("https://ipchicken.com")
        time.sleep(5)
        driver.quit()
    except:
        driver.quit()
