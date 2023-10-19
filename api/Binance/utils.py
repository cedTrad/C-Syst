import requests
from urllib.parse import urljoin
import time
import datetime



def serverGap():
    path = "/fapi/v1/time"
    URL = "https://testnet.binancefuture.com"
    url = urljoin(URL, path)
    server_time = requests.get(url)
    gap = (server_time.json()['serverTime'] - time.time()*1000)/1000
    return gap


def info():
    path = "/fapi/v1/exchangeInfo"
    URL = "https://testnet.binancefuture.com"
    url = urljoin(URL, path)
    info = requests.get(url)
    return info.json()

