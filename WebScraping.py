import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Necessary information for sending email
sender_email = "pythondeneme25@gmail.com"
sender_password = "hwad jpvi gnar eoid"
receiver_email = "beediaoguz@gmail.com"

def send_email(product_name, product_link, new_price):
    subject = "Ürün fiyatı düştü!"
    body = f"Merhaba,\n\n{product_name} ürününün fiyatı düştü! Yeni fiyat: {new_price} TL \n\nÜrüne şu linkten erişebilirsiniz: {product_link}"

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

previous_prices = {}

def CheckProduct():
 # Start the Chrome driver
 service = Service(ChromeDriverManager().install())
 driver = webdriver.Chrome(service=service)

 URL = 'https://www.trendyol.com/sr?wb=101470&wc=103498&attr=292|1218519_1218520_1218522'
 
 # Open the page
 driver.get(URL)

 # Wait for the page to fully load
 driver.implicitly_wait(10)

 # Get the page source
 content = driver.page_source

 # Analyze the content using BeautifulSoup
 soup = BeautifulSoup(content, 'html.parser')

 # Create a dictionary containing phone links, names, and prices
 phone_dict = {}

 # Get href attributes of <a> tags, alt attributes of <img> tags and price information within each <div> element
 for div in soup.find_all("div", class_="p-card-wrppr with-campaign-view"):
    phone_link = div.find("a")
    phone_name = div.find("img")
    price_tag = div.find("div", class_="prc-box-dscntd").text.strip()
    if phone_link and phone_name and price_tag:
        link = "https://www.trendyol.com" + phone_link['href']
        phone_dict[phone_name['alt']] = {'link': link, 'price': price_tag}

 # Print the created dictionary to the screen
 for phone, details in phone_dict.items():
    print(f"Telefon: {phone}")
    print(f"Link: {details['link']}")
    print(f"Fiyat: {details['price']}")
    
    new_price = float(details['price'].strip('TL').replace(',', '.'))

    # If the previous price exists and the new price is lower than the previous one
    if phone in previous_prices and new_price < previous_prices[phone]:
        send_email(phone, details['link'], new_price)  # Send email
        print("Fiyat düştü! E-posta gönderildi. \n")
    
    #update previous price 
    previous_prices[phone] = new_price

 driver.quit()

while True:
   CheckProduct()
   time.sleep(3600)