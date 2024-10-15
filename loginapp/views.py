# views.py
import time

from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from rest_framework import status
from rest_framework.views import APIView
from seleniumwire import webdriver as wire_webdriver

from ApolloTest.settings import (
    APOLLO_PASSWORD, APOLLO_EMAIL,
    APOLLO_LOGIN_URL, APOLLO_API_REQUEST_URL,
    APPOLLO_API_ENDPOINT_TO_FIND
)
from loginapp.models import RequestData


class LoginAndSaveCookiesView(APIView):
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/129.0.0.0 Safari/537.36")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    def get_cookies(self, email: str, password: str):
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            # Open the login page
            driver.get(APOLLO_LOGIN_URL)
            time.sleep(10)  # Wait for the login page to load
            # Find and fill in the email field using XPath
            email_field = driver.find_element(By.XPATH,
                                              '/html/body/div[2]'
                                              '/div/div[2]'
                                              '/div/div[1]/'
                                              'div/div[2]/div/div[2]'
                                              '/div/form/div[2]'
                                              '/div/div/input')
            email_field.clear()
            email_field.send_keys(email)
            # Find and fill in the password field using XPath
            password_field = driver.find_element(By.XPATH,
                                                 '/html/body/div[2]'
                                                 '/div/div[2]/div/div[1]'
                                                 '/div/div[2]/div/div[2]'
                                                 '/div/form/div[3]/div/'
                                                 'div[1]/div/input')
            password_field.clear()
            password_field.send_keys(password)

            # Submit the form
            password_field.send_keys(Keys.RETURN)
            time.sleep(15)  # Wait for the login process to complete

            # Check if login was successful
            try:
                after_login_element_xpath = '/html/body/div[2]/div/' \
                                            'div[2]/div[2]/div/div' \
                                            '[2]/div/div[2]/div[2]/' \
                                            'div[1]/div[1]/div[2]' \
                                            '/div[3]/div[3]/div/' \
                                            'button/div'
                driver.find_element(By.XPATH,
                                    after_login_element_xpath)
                # that indicates a successful login
                # Retrieve cookies from the Selenium session
                cookies = driver.get_cookies()
                return cookies
            except Exception:
                return None  # Login failed or the element wasn't found
        finally:
            driver.quit()

    def get_driver_requests(self, cookies):
        driver = wire_webdriver.Chrome(options=self.chrome_options)
        # Set cookies for the new session
        driver.get(APOLLO_API_REQUEST_URL)  # First,
        # get the main page to set the domain
        for cookie in cookies:
            driver.add_cookie(cookie)  # Add each cookie to the driver
        driver.get(APOLLO_API_REQUEST_URL)  # Navigate again to load
        # resources with the cookies
        # Access requests via the `requests` attribute
        time.sleep(30)
        return driver.requests

    def is_request_writen_to_db(self, cookies, driver_requests):
        # Initialize the WebDriver again for capturing requests
        for request in driver_requests:
            # Check if the request has a response
            if request.url == APPOLLO_API_ENDPOINT_TO_FIND:
                request_payload = request.body.decode('utf-8')
                request_cookie = request.headers.get("cookie", "")
                request_data = RequestData(
                    url=request.url,
                    headers=request.headers,
                    payload=request_payload,
                    cookies=request_cookie
                )
                request_data.save()
                return True
        return False

    def post(self, request):
        # Get cookies after successful login
        cookies = self.get_cookies(email=APOLLO_EMAIL,
                                   password=APOLLO_PASSWORD)
        if not cookies:
            return JsonResponse({'error': 'Login failed. '
                                          'Please check your credentials.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        driver_requests = self.get_driver_requests(cookies=cookies)
        is_writen = self.is_request_writen_to_db(cookies=cookies,
                                                 driver_requests=driver_requests)
        if is_writen:
            return JsonResponse({'message': 'Request successfully '
                                            'written to the database.'},
                                status=status.HTTP_200_OK)
        return JsonResponse({'message': 'The needed request was '
                                        'not found and '
                                        'information was not written'})
