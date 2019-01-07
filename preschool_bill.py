import datetime
import os
import re
import time

import yagmail
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CURRENT_PATH = os.getcwd()
CHROMEDRIVER_PATH = CURRENT_PATH + '/chromedriver'
LOGIN_FILE_PATH = CURRENT_PATH + '/user_data.txt'


class PreschoolBill():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH,
                                       chrome_options=self.chrome_options,
                                       service_args=['--verbose',
                                                     '--log-path=/tmp/chromedriver.log'])
        self.login = None
        self.password = None
        self.emails = None
        self.gmail_user = None
        self.gmail_pass = None

    def parse_base_user_data(self):
        with open(LOGIN_FILE_PATH, "r") as file:
            data = [line.replace('\n', '') for line in
                    file.readlines()]
            for line in data:
                splitted_line = line.split(' ')
                if splitted_line[0] == 'LOGIN':
                    self.login = data[0].split(" ")[1]
                elif splitted_line[0] == 'PASSWORD':
                    self.password = data[1].split(" ")[1]
                elif splitted_line[0] == 'EMAILS':
                    self.emails = data[2].split(" ")[1:]
                elif splitted_line[0] == 'GMAIL_USER':
                    self.gmail_user = data[3].split(" ")[1]
                elif splitted_line[0] == 'GMAIL_PASS':
                    self.gmail_pass = data[4].split(" ")[1]
                else:
                    raise ValueError

    def login_to_site_and_get_data(self):
        self.driver.get('https://edziecko.dipolpolska.pl/')
        time.sleep(1)

        login_element = self.driver.find_element_by_name('user')
        login_element.send_keys(self.login)

        pass_element = self.driver.find_element_by_name('pwd')
        pass_element.send_keys(self.password)
        pass_element.send_keys(Keys.RETURN)

        time.sleep(2)
        bill_element = self.driver.find_element_by_css_selector(
            ("a[href*='accountancy/rozliczenie_dla_rodzicow']"))
        bill_element.click()

        main_html = self.driver.find_element_by_class_name('panel-body')
        source_html = main_html.get_attribute('innerHTML')
        return source_html

    def parse_data(self, source):
        data = BeautifulSoup(source, 'html.parser')
        text = data.find('h3').text.strip()
        amount = re.findall(r'\d+.\d+', text)[0]
        return amount

    def open_data(self):
        with open('data.txt', 'r+') as f:
            data_text = f.read()
            return data_text

    def check_mail_and_send(self, data_text, amount):
        today = datetime.datetime.now()
        current_month = today.strftime("%Y %B")
        if not amount in data_text and not current_month in data_text:
            data_text += current_month + ' ' + amount + '\n'

            yag = yagmail.SMTP(self.gmail_user, self.gmail_pass)
            subject = 'Pre-School Bill ' + current_month
            text = 'There is a bill for ' + current_month + ' for amount ' + amount + ' zl'
            for email in self.emails:
                pass
                yag.send(to=email, subject=subject, contents=text)
            self._write_data(data_text)

    def _write_data(self, data_text):
        with open('data.txt', 'w') as f:
            f.write(data_text)


if __name__ == '__main__':
    pb = PreschoolBill()
    pb.parse_base_user_data()
    data_text = pb.open_data()
    source = pb.login_to_site_and_get_data()
    amount = pb.parse_data(source)
    pb.check_mail_and_send(data_text, amount)
