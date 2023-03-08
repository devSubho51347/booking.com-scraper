import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .constants import url,email,password
from selenium.webdriver.common.keys import Keys
from datetime import date
from time import sleep
import pandas as pd


# Now we have to create a class which will inherit the webdriver class
# We are doing this so that along with webdriver methods we can also create our custome methods and use them

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\Selenium Drivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        # We want to instantiate the webdriver.Chrome class along the way so we use super
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        # Maximize the window
        self.maximize_window()
        self.dict = {"Hotel": []}

    # This method will automatically close the class
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_first_page(self):
        self.get(url)

    def sign_in(self):
        # sign_in_btn = WebDriverWait(self,20).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME,"bui-button bui-button--secondary js-header-login-link selectorgadget_suggested"))
        # )
        # print(sign_in_btn)
        sign_in_btn = self.find_elements(By.CLASS_NAME, "js-header-login-link")
        print(sign_in_btn)
        sign_in_btn = sign_in_btn[1]
        sign_in_btn.click()
        # sign_in_btn.click()
        my_email = self.find_element(By.CLASS_NAME, "_2XLcoGj27PmEfeIS8BIkNh")
        my_email.send_keys(email)
        email_btn = self.find_element(By.CSS_SELECTOR, "._2__0gVPBP36LBlyHwThlOQ")
        print(email_btn)
        email_btn.click()
        # email_btn.click()
        my_password = self.find_element(By.ID, "password")
        my_password.send_keys(password)
        password_btn = self.find_element(By.CSS_SELECTOR, "._2__0gVPBP36LBlyHwThlOQ")
        password_btn.click()

    def select_place_to_go(self):
        search_field = self.find_elements(By.CSS_SELECTOR, "#\:Ra9\:")[0]
        # Before we enter anything in the iput field it is very imp to clear previous text
        # search_field.clear()
        print("Enter the name of the place:")
        place = input()
        search_field.send_keys(place, Keys.ENTER)

    def get_hotels_info(self):

        ## Add the scroll functionality
        self.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        scroll = 12
        sleep(2)
        for i in range(scroll):
            self.find_element(By.TAG_NAME, "html").send_keys(Keys.SPACE)
            sleep(1)

        ## Extracting hotel names

        hotel_names = self.find_elements(By.CSS_SELECTOR, ".fcab3ed991.a23c043802")
        # prices = self.find_elements(By.CSS_SELECTOR, ".fd1924b122.d4741ba240")
        print(len(hotel_names))
        # print(len(prices))

        for ele in hotel_names:
            self.dict["Hotel"].append(ele.text)

        ## Extracting price of hotel


        # print(prices)
        #
        # for ele in prices:
        #
        #     self.dict["Price"].append(ele.text)

        ## Adding functionality to move on to the next page
        print(self.dict)
        print(len(self.dict["Hotel"]))


        nxt_button = self.find_element(By.CSS_SELECTOR, ".f32a99c8d1.f78c3700d2")
        print(nxt_button)
        nxt_button = nxt_button.find_element(By.TAG_NAME, "button")
        nxt_button.click()

    def create_dataframe(self):

        df = pd.DataFrame(self.dict)
        df.to_csv("mumbai_hotels1.csv")
