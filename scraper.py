import requests
from bs4 import BeautifulSoup
import time
import smtplib

#Any error in input is caught here
try:
    URL = input('Enter the URL: ')
    pricedrop = int(input('[+]Enter the price drop value: '))
    email = input('[+] Enter your email for updates: ')
    email2 = input('[+] Enter another email for logging into smtp: ')
    password = input('[*] Password for logging into the smtp server: ')
    header = {"User-Agent": 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'} #replace with your user-agent
    interval = int(input('[+] Enter the time interval you want to check for price drop in seconds: '))
except:
    print("Error with URL/email/useragent")

#logging into the server and estalishing connection
def sendmail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    try:
        server.login(email2, password)
    except:
        print('Authentication error with smtp server')
    subject ='PRICE ALERT'
    body = f"check amazon link {URL}"
    msg = f"subject:{subject}\n\n{body}"
    server.sendmail(email2, email, msg)
    print("Email sent")
    server.quit()

#scraping and finding product id and the original price
def get_price():

    page = requests.get(URL, headers=header)
    htmlpage = BeautifulSoup(page.content, 'html.parser')
    product_title = htmlpage.find(id="productTitle").get_text()
    product_value = htmlpage.find(id="priceblock_ourprice").get_text() #this code might break in amazon sometimes!!!
    if(',' in product_value):
        converted_product_value = product_value[1:].replace(',', '')
    else:
        converted_product_value = product_value[1:]
    if(float(converted_product_value) < pricedrop):
            sendmail()



while (True):
    get_price()
    print('[+] Script running...')
    time.sleep(interval)
