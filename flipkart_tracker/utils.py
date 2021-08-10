import requests
from bs4 import BeautifulSoup
import lxml

#url = 'https://www.flipkart.com/msi-gf63-thin-core-i5-10th-gen-8-gb-1-tb-hdd-windows-10-home-4-gb-graphics-nvidia-geforce-gtx-1650-max-q-60-hz-10scxr-1618in-gaming-laptop/p/itm76993f27ad4bd?pid=COMG2K9ZJWWV2BGX&lid=LSTCOMG2K9ZJWWV2BGXWYR6AP&marketplace=FLIPKART&store=6bo%2Fb5g&srno=b_1_2&otracker=hp_omu_Top%2BOffers_3_4.dealCard.OMU_XI2Q41K7XRAJ_3&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_3_NA_view-all_3&fm=neo%2Fmerchandising&iid=en_88xLC9tozPrlDC3p08xWvF4be%2F6nOdXkruYGuVEr5o%2B1AJkflbHBXnuhJkfHoUbEVfGT0brMXc7Q5HqI%2FaaGdQ%3D%3D&ppt=hp&ppn=homepage&ssid=449d8hrxog0000001628232917865'


def get_url_link(url):

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        "Accept-Language": "en",
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    title = soup.find("span", {"class": "B_NuCI"}).get_text()
    price = float(soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text()[1:].replace(',', ''))
    return title,price
