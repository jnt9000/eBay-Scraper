from bs4 import BeautifulSoup
import requests
from gmail import GMail, Message
import time
from creds import email_creds,email_recipients
import schedule 
    
def get_listings():
    ebay_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=funko+pop&_sacat=0"
    r = requests.get(ebay_url)
    data = r.text
    soup = BeautifulSoup(data)
    listings = soup.find_all('li', attrs={'class': 's-item'})
    price_title_dicts = []
    for listing in listings[1:]:
        price = listing.find(class_='s-item__price').text
        title = listing.find(class_='s-item__title').text.split("New Listing")[-1]
        link = listing.find(href = True)["href"]
        price_title_dicts.append({"price":price,"title":title,"link":link})
    return price_title_dicts

def send_email(filtered_listings): 
    gmail = GMail(email_creds()[0],email_creds()[1])
    msg = Message(subject = "New Listings Of Interest",
                  to = email_recipients(),

                  text = str(filtered_listings) 
                 )
    gmail.send(msg)

def run_funcs():
    price_title_dicts = get_listings()
    filtered_listings = [listing for listing in price_title_dicts if ("dc" in listing["title"].lower() or "marvel" in listing["title"].lower() or "exclusive" in listing["title"].lower())]
    if filtered_listings != []:
        send_email(filtered_listings)
    else:
        print("There were no listings to send :( O")
    
schedule.every(360).minutes.do(run_funcs)
while True:
    schedule.run_pending()
    time.sleep(1)