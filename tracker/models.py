# models.py
import urllib.request
import requests
from bs4 import BeautifulSoup
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
import time


class PriceTracker(models.Model):
    url = models.URLField()
    desired_price = models.FloatField()
    alert_time = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"Price Tracker for {self.url}"

    def find_price_amazon(self):
        try:
           r=requests.get(self.url)
           soup=BeautifulSoup(r.text,'lxml')
           price=soup.select_one('.a-price-whole')
           return price
        except Exception as e:
            print(f"Error while fetching price from Amazon: {e}")
            return None


    def find_price_flipkart(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            selected_area = soup.find(class_="_30jeq3 _16Jk6d")
            price = selected_area.text if selected_area else None
            return price
        except Exception as e:
            print(f"Error while fetching price from Flipkart: {e}")
            return None

    def find_price(self):
        if 'amazon' in self.url:
            return self.find_price_amazon()
        elif 'flipkart' in self.url:
            return self.find_price_flipkart()
        else:
            print("Unsupported website")
            return None

    def track_price(self):
        start_time = time.time()

        while True:
            price = self.find_price()

            if price is None:
                print("Invalid link")
                break

            print(f"Your current price is: ₹{price}")

            if price and price <= self.desired_price:
                print(f"Desired price reached! Current price: ₹{price}")
                self.send_email("BUY Now", f"Price reached: ₹{price}, Link: {self.url}")
                break

            elapsed_time = time.time() - start_time

            if elapsed_time >= self.alert_time:
                subject = "Price Alert"
                body = (
                    f"Oops! The price has not changed. "
                    f"Current price is ₹{price}. Consider buying or checking other products."
                )
                self.send_email(subject, body)
                break

            time.sleep(10)  # You can adjust the sleep time as needed

    def send_email(self, subject, body):
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.email]

        print(f'Sending email to {self.email}...')
        send_mail(
            subject,
            body,
            email_from,
            recipient_list,
            fail_silently=False,
        )
        print(f'Email sent to {self.email}!')
