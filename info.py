import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd

baseurl = "https://niceonesa.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

productLinks = []

for x in range(5, 56):
    r = requests.get(f"https://niceonesa.com/ar/perfume?page={x}")
    soup = BeautifulSoup(r.content, "lxml")
    produtList = soup.find_all("a", class_="min-w-[160px] max-w-[450px] rounded-md bg-white relative")
    for link in produtList:
        link.find_all("a", href=True)
        productLinks.append(baseurl + link["href"])
        print("Saving Links...")


productList = []
for link in productLinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        name = soup.find("h1", class_="text-xl mb-4").text.strip()
        discountedPrice = re.findall("[.\d]+", soup.find("div", class_="text-discount-color font-niceone-medium me-2 whitespace-nowrap").text.strip())
        reviews = re.findall("\d+", soup.find("div", class_="van-rate van-rate--readonly px-2").find_next("span").text.strip())[0]
        price = re.findall("\d+\.\d+", soup.find("div", class_="font-niceone-medium").text.strip())
        description = soup.find("div", {"dir" : "rtl"}).text.strip()
        image = soup.find("div", {"id" : "img-container"}).find("img")["src"].strip()
        brand = soup.find("div", class_="text-success").find_next("a").text.strip()
        sizesRaw = soup.find_all("div", class_="text-[11px] mb-1")
        sizes = []
        for size in sizesRaw:
            sizes.append(size.text.strip())    

        cats = soup.find("div", class_="inline-flex items-center").text.strip()
    except:
        name = []
        reviews = []
        price = []
        description = []
        image = []
        brand = []
        discountedPrice = []
        sizes = []
        sizesRaw = []

    product = {
        "name": name,
        "reviews": reviews,
        "price": price,
        "discountedPrice": discountedPrice,
        "brand": brand,
        "sizes": sizes,
        "image": image,
        "cats": cats,
        "description": description,
        "link": link
    }
    productList.append(product)
    print("Saving...", product["link"])

df = pd.DataFrame(productList)
df.to_excel("data.xlsx")