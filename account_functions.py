import random
import pandas
import cv2
from image_functions import unique_ids, check_presence
from selenium import webdriver
from selenium.webdriver.common.by import By


data = {
    "uniqueId": [],
    "name": [],
    "password": [],
    "linkedin_username": [],
    "linkedin_password": [],
    "instagram_username": [],
    "instagram_password": [],
}

class Account():
    def __init__(self):
        self.uniqueId = None
        self.name = None
        self.password = None
        # image details
        self.image = None
        self.face_encodings = None
        # account data
        self.secure_linkedin = False
        self.secure_instagram = False
        self.linkedin_username = None
        self.linkedin_password = None
        self.instagram_username = None
        self.instagram_password = None
        # presence of user
        self.is_login = False
        self.is_using = None
        self.absence_count = 0

    def generate_uniqueId(self, uniqueIds):
        random_no = random.randint(1, 9999)
        if random_no not in uniqueIds:
            return random_no
        else:
            self.generate_uniqueId()

    def sign_up(self):
        self.uniqueId = self.generate_uniqueId(unique_ids)
        cv2.imwrite(f"auto_logout_system/images/{self.uniqueId}.jpg", self.image)
        data["uniqueId"].append(self.uniqueId)
        data["name"].append(self.name.get().title())
        data["password"].append(self.password.get())
        data["linkedin_username"].append(self.linkedin_username.get())
        data["linkedin_password"].append(self.linkedin_password.get())
        data["instagram_username"].append(self.instagram_username.get())
        data["instagram_password"].append(self.instagram_password.get())

        df = pandas.DataFrame(data)
        df.to_csv("auto_logout_system/data.csv")

    def getdata(self):
        csv_data = pandas.read_csv("auto_logout_system/data.csv")
        self.name = csv_data.name[csv_data["uniqueId"]==self.uniqueId].item()
        self.password = csv_data.password[csv_data["uniqueId"]==self.uniqueId].item()
        self.linkedin_username = csv_data.linkedin_username[csv_data["uniqueId"]==self.uniqueId].item()
        self.linkedin_password = csv_data.linkedin_password[csv_data["uniqueId"]==self.uniqueId].item()
        self.instagram_username = csv_data.instagram_username[csv_data["uniqueId"]==self.uniqueId].item()
        self.instagram_password = csv_data.instagram_password[csv_data["uniqueId"]==self.uniqueId].item()
        self.secure_linkedIn = not(csv_data.linkedin_username.isna().item())
        self.secure_instagram = not(csv_data.instagram_username.isna().item())

    def login_linkedin(self, window):
        global driver
        driver = webdriver.Chrome(executable_path="auto_logout_system/chromedriver.exe")
        driver.implicitly_wait(1)
        driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

        username = driver.find_element(By.ID, "username")
        username.send_keys(f"{self.linkedin_username}")
        pword = driver.find_element(By.ID, "password")
        pword.send_keys(f"{self.linkedin_password}" + '\n')
        self.is_login=True
        self.is_using = "linkedin"

    def logout_linkedin(self):
        global driver
        driver.get("https://linkedin.com/m/logout")
        driver.quit()
        self.is_login = False
        cv2.destroyAllWindows()

    def login_instagram(self, window):
        global driver
        driver = webdriver.Chrome(executable_path="auto_logout_system/chromedriver.exe")
        driver.implicitly_wait(1)
        driver.get('https://www.instagram.com/')

        username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        username_input.send_keys(self.instagram_username)
        password_input.send_keys(self.instagram_password)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        self.is_login=True
        self.is_using = "instagram"

    def logout_instagram(self):
        global driver
        driver.get("https://instagram.com/accounts/logout/")
        driver.quit()
        self.is_login = False
        cv2.destroyAllWindows()