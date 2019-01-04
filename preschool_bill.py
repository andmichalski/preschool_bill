import datetime
import os
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CURRENT_PATH = os.getcwd()
CHROMEDRIVER_PATH = CURRENT_PATH + '/chromedriver'
LOGIN_FILE_PATH = CURRENT_PATH + '/login.txt'


class PreschoolBill():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument(
        #     '--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=self.chrome_options,
                                       service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        self.login = None
        self.password = None

    def parse_base_user_data(self):
        with open(LOGIN_FILE_PATH, "r") as file:
            data = [line.replace('\n', '').split(" ")[1] for line in
                    file.readlines()]
            self.login = data[0]
            self.password = data[1]

    def login_to_site_and_get_data(self):
        self.driver.get('https://edziecko.dipolpolska.pl/')
        time.sleep(1)

        login_element = self.driver.find_element_by_name('user')
        login_element.send_keys(self.login)

        pass_element = self.driver.find_element_by_name('pwd')
        pass_element.send_keys(self.password)
        pass_element.send_keys(Keys.RETURN)

        time.sleep(2)
        bill_element = self.driver.find_element_by_css_selector(("a[href*='accountancy/rozliczenie_dla_rodzicow']"))
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

    def check_mail_was_sent_in_month(self, data_text, amount):
        today = datetime.datetime.now()
        current_month = today.strftime("%Y %B")
        if not amount in data_text and not current_month in data_text:
            data_text += current_month + ' ' + amount + '\n'
            self._write_data(data_text)
            # TODO sent email

    def _write_data(self, data_text):
        with open('data.txt', 'w') as f:
            f.write(data_text)


if __name__ == '__main__':
    pb = PreschoolBill()
    pb.parse_base_user_data()
    data_text = pb.open_data()
    source = pb.login_to_site_and_get_data()
    amount = pb.parse_data(source)
    pb.check_mail_was_sent_in_month(data_text, amount)
