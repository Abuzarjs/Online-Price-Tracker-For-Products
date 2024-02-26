# utils.py

import time
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.core.mail import send_mail
from django.conf import settings

def find_price(url, selector):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers={"User-Agent": "Your User Agent"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        selected_area = soup.select_one(selector)
        return selected_area.get_text() if selected_area else None
    except requests.RequestException as e:
        print(f"Error fetching price: {e}")
        return None

def track_price(price_tracker):
    start_time = time.time()

    while True:
        if 'amazon' in price_tracker.url:
            selector = '.a-price-whole'
        elif 'flipkart' in price_tracker.url:
            selector = '._30jeq3._16Jk6d'
        else:
            print("Invalid URL")
            break

        price = find_price(price_tracker.url, selector)

        if price is None:
            print("Invalid link")
            break

        current_price = float(price.replace('₹', '').replace(',', ''))

        print(f"Your current price is: ₹{current_price}")

        if current_price <= price_tracker.desired_price:
            print(f"Desired price reached! Current price: ₹{current_price}")
            send_email("BUY Now", f"Price reached: ₹{current_price}, Link: {price_tracker.url}", price_tracker.email)
            break

        elapsed_time = time.time() - start_time

        if elapsed_time >= price_tracker.alert_time:
            subject = "Price Alert"
            body = f"Price has not changed. Current price is ₹{current_price}. Consider buying or checking other products."
            send_email(subject, body, price_tracker.email)
            break

        time.sleep(10)  # You can adjust the sleep time as needed

def send_email(subject, body, recipient):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient]

    print(f'Sending email to {recipient}...')
    send_mail(
        subject,
        body,
        email_from,
        recipient_list,
        fail_silently=False,
    )
    print(f'Email sent to {recipient}!')
