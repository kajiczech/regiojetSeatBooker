# -*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from .webdriver_management import *
import os
import platform

class SeatFinder:
    url_replacements = {
        'arrival': '$arrival',
        'departure': '$departure',
        'date': '$date',
        'tariff': '$tariff'
    }

    # url with mock strings, which should be replaced with relevant data
    default_url = "https://jizdenky.regiojet.cz/Booking/from/" + url_replacements['departure'] + "/to/" \
                  + url_replacements['arrival'] + "/tarif/" + url_replacements['tariff'] + "/departure/" \
                  + url_replacements['date'] + "/retdep/" \
                  + url_replacements['date'] + "/return/false?0#search-results"

    # Url of the booking webpage (generated from defaultUrl)
    parsed_url = ""

    login_url = 'https://jizdenky.regiojet.cz/Login'
    cities = {'Praha': '10202003', 'Pisek': '17904007', 'C. Budejovice': '17904008'}
    tariffs = {'regular': 'REGULAR', 'student': 'CZECH_STUDENT_PASS_26'}
    page_searches = []

    # label of the button which proceeds to an order
    proceed_to_order_label = 'Pokračovat k objednávce'

    # string to be found on the page, when the user is not logged in
    not_logged_in_label = 'Odhlásit'

    # name of the button which is used to buy a ticket (when the user is logged in)
    buy_button_name = 'buttonContainer:createAndPayTicketButton'
    # name of the button which is used to reserve the ticket (when the user is not logged in)
    reserve_button_name = 'buttonContainer:createTicketButton'

    # we need to accept terms - this is a name of that button (checkbox)
    accept_terms_checkbox_name = 'bottomComponent:termsAgreementCont:termsAgreementCB'

    # just to be completely sure, we add this prefix into the timestamp of the rowid
    seat_search_prefix = 'class="item_blue blue_gradient_our routeSummary free" ybus:rowid="<<b><'

    # selenium driver to control the browser
    selenium_driver = None

    # whether the user is logged in or not
    is_user_logged_in = False

    # class of row with seats
    seat_button_class_name = 'item_blue'

    # class of field with departure
    departure_field_class = 'col_depart'

    def __init__(self, departure, arrival, date, times, tariff='REGULAR', base_url=None, chrome_version=None):
        """
            Sets the url, driver, nad string[s] which is used to find an empty seat on the webpage
        """
        if base_url is None:
            base_url = self.default_url
        date = self.parse_date(date)
        times = self.parse_times(times)
        for one_time in times:
            self.page_searches.append(one_time)

        self.set_parsed_url(departure, arrival, date, tariff, base_url)

        print(
              "Date: {}\n"
              "Times {}\n"
              "From {} to {}\n"
              "Tariff: {}\n"
              "Chrome version: {}\n".format(
                date, str(times), departure, arrival, tariff, chrome_version
            )
        )

        self.selenium_driver = get_chromedriver(chrome_version)

    def find_seat(self):
        """ refreshes page until there is not an empty seat
             @return element of the found seat
               - this is necessary, because user can search for more then one seat (aka time)
        """
        try:
            self.selenium_driver.get(self.parsed_url)
            while 1:
                time.sleep(1)
                elements = self.selenium_driver.find_elements_by_class_name(self.seat_button_class_name)
                for search in self.page_searches:
                    for element in elements:
                        departs = element.find_elements_by_class_name(self.departure_field_class)
                        for depart in departs:
                            if depart.text == search:
                                print('found')
                                return element
                print('not found')
                try:
                    self.selenium_driver.refresh()
                # when the webpage crashes
                except TimeoutException:
                    self.selenium_driver.get(self.parsed_url)
        except WebDriverException:
            print('WebDriverException')
            return False

    # performs the actions necessary to book the seat, when some seat is empty
    def take_seat(self, element):

        self.click_button(element.find_element_by_class_name('col_price'), 1)

        # Brings browser to front
        self.selenium_driver.execute_script('window.alert("Seat found!!!")')
        alert = self.selenium_driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        self.click_button(
            self.selenium_driver.find_element_by_xpath("//*[contains(text(), '" + self.proceed_to_order_label + "')]")
        )
        if self.is_user_logged_in:
            self.take_seat_logged_in()
        else:
            self.take_seat_not_logged_in()

    def take_seat_not_logged_in(self):
        self.click_button(self.selenium_driver.find_element_by_name(self.accept_terms_checkbox_name))
        self.click_button(self.selenium_driver.find_element_by_name(self.reserve_button_name))

    # actions specific to when the user is logged in
    def take_seat_logged_in(self):
        try:
            self.click_button(self.selenium_driver.find_element_by_name(self.buy_button_name))
        except NoSuchElementException:
            self.click_button(self.selenium_driver.find_element_by_name(self.reserve_button_name))

    # clicks given button (or any element, does not have to be explicitly button)
    def click_button(self, button, timeout=0):
        time.sleep(timeout)
        # TODO: http://stackoverflow.com/questions/24411765/how-to-get-an-xpath-from-selenium-webelement-or-from-lxml
        if button.get_attribute('id'):
            wait = WebDriverWait(self.selenium_driver, 10)
            button = wait.until(ec.element_to_be_clickable((By.ID, button.get_attribute('id'))))
            try:
                button.send_keys(Keys.NULL)
            except WebDriverException:
                pass
        button.click()

    # parses times to format ['HHMM',....] (M = minutes...)
    @staticmethod
    def parse_times(times):
        if not times[0]:
            raise ValueError("No times specified")

        if times[0] == '0':
            times = times[1:]
        return times

    # parses date to format 'yyyymmdd'
    @staticmethod
    def parse_date(date):
        if '.' in date:
            parts = date.split('.')
            if len(parts) < 2:
                raise IOError('Invalid date')
            if len(parts[0]) == 1:
                parts[0] = "0" + str(parts[0])
            if len(parts[1]) == 1:
                parts[1] = "0" + str(parts[1])
            date = parts[1] + parts[0]
        if len(date) == 0:
            date = time.strftime("%m%d")
        if len(date) != 4:
            raise IOError('Invalid date' + date)
        year = datetime.datetime.now().year
        return str(year) + date

    # replaces elements in base url so it makes sense
    def set_parsed_url(self, departure, arrival, date, tariff, base_url):
        departure = self.get_city_code(departure)
        arrival = self.get_city_code(arrival)
        tariff = self.get_tariff_code(tariff)
        tmp_url = base_url.replace(self.url_replacements['arrival'], arrival)
        tmp_url = tmp_url.replace(self.url_replacements['departure'], departure)
        tmp_url = tmp_url.replace(self.url_replacements['tariff'], tariff)
        self.parsed_url = tmp_url.replace(self.url_replacements['date'], date)

    # gets code of the city
    def get_city_code(self, city):
        return self.cities[str(city)] if self.cities[str(city)] is not None else city

    # gets code of the tarif
    def get_tariff_code(self, tariff):
        return self.tariffs[str(tariff.lower())] if self.tariffs[str(tariff.lower())] is not None else tariff

    # logs user with given username an password
    def login(self, username, password):
        if len(username) == 0 or len(password) == 0:
            return
        self.selenium_driver.get(self.login_url)
        login = self.selenium_driver.find_element_by_id('login_credit')
        pwd = self.selenium_driver.find_element_by_id('pwd_credit')
        login.send_keys(username)
        pwd.send_keys(password)
        pwd.send_keys(Keys.ENTER)
        while not self.check_logged_in():
            pass
        self.is_user_logged_in = self.check_logged_in()

    def check_logged_in(self):
        """
            checks,whether the user is logged in or not
            It is determined from a string on the page which logs out a user
        """
        time.sleep(1)
        logged = True
        try:
            self.selenium_driver.find_element_by_xpath("//*[contains(text(), '" + self.not_logged_in_label + "')]")
        except NoSuchElementException:
            logged = False
        return logged

