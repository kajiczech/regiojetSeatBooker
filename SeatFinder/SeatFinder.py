# -*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import platform
import inspect

dir_path = os.path.dirname(os.path.realpath(__file__))


class SeatFinder:
    urlReplacements = {
        'arrival': '$arrival',
        'departure': '$departure',
        'date': '$date',
        'tariff': '$tariff'
    }

    # url with mock strings, which should be replaced with relevant data
    defaultUrl = "https://jizdenky.regiojet.cz/Booking/from/" + urlReplacements['departure'] + "/to/" \
                 + urlReplacements['arrival'] + "/tarif/" + urlReplacements['tariff'] + "/departure/" \
                 + urlReplacements['date'] + "/retdep/" \
                 + urlReplacements['date'] + "/return/false?0#search-results"

    # Url of the booking webpage (generated from defaultUrl)
    parsedUrl = ""
    chromeDriverDir = os.path.join('src', 'chromedrivers')
    chromedriver_folder_path = os.path.join(dir_path, 'src', 'chromedrivers')
    default_chromedriver_folder_name = 'default'
    chromeDriverLocations = {
        'mac': os.path.join(chromedriver_folder_path, default_chromedriver_folder_name, 'mac'),
        'windows': os.path.join(chromeDriverDir, default_chromedriver_folder_name, 'win.exe'),
        'linux': os.path.join(chromeDriverDir, default_chromedriver_folder_name, 'lin')
    }
    loginUrl = 'https://jizdenky.regiojet.cz/Login'
    cities = {'Praha': '10202003', 'Pisek': '17904007', 'C. Budejovice': '17904008'}
    tariffs = {'regular': 'REGULAR', 'student': 'CZECH_STUDENT_PASS_26'}
    pageSearches = []

    # label of the button which proceeds to an order
    proceedToOrder = 'Pokračovat k objednávce'

    # string to be found on the page, when the user is not logged in
    notLoggedIn = 'Odhlásit'

    # name of the button which is used to buy a ticket (when the user is logged in)
    buyButtonName = 'buttonContainer:createAndPayTicketButton'
    # name of the button which is used to reserve the ticket (when the user is not logged in)
    reserveButtonName = 'buttonContainer:createTicketButton'

    # we need to accept terms - this is a name of that button (checkbox)
    acceptTerms = 'bottomComponent:termsAgreementCont:termsAgreementCB'

    # just to be completely sure, we add this prefix into the timestamp of the rowid
    searchPrefix = 'class="item_blue blue_gradient_our routeSummary free" ybus:rowid="<<b><'

    # selenium driver to controll the browser
    driver = None

    # whether the user is logged in or not
    loggedIn = False

    # class of row with seats
    seatClass = 'item_blue'

    # class of field with departure
    departureClass = 'col_depart'

    def __init__(self, departure, arrival, date, hours, tariff='REGULAR', baseUrl=None, chrome_version=None):
        """
            Sets the url, driver, nad string[s] which is used to find an empty seat on the webpage
        """
        if baseUrl is None:
            baseUrl = self.defaultUrl
        date = self.parseDate(date)
        hours = self.parseHours(hours)
        for hour in hours:
            self.pageSearches.append(self.createPageSearch(hour, date))

        self.setParsedUrl(departure, arrival, date, tariff, baseUrl)
        chrome_options = Options()
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-proxy-server')
        chrome_driwer_path = self.getChromeDriverPath(chrome_version)
        print(chrome_driwer_path)
        os.environ["webdriver.chrome.driver"] = chrome_driwer_path
        self.driver = webdriver.Chrome(chrome_driwer_path, chrome_options=chrome_options)


    def findSeat(self):
        """ refreshes page until there is not an empty seat
             @return element of the found seat
               - this is necessary, because user can search for more then one seat (aka time)
        """
        try:
            self.driver.get(self.parsedUrl)
            while 1:
                time.sleep(1)
                elements = self.driver.find_elements_by_class_name(self.seatClass)
                for search in self.pageSearches:
                    for element in elements:
                        departs = element.find_elements_by_class_name(self.departureClass)
                        for depart in departs:
                            if depart.text == search:
                                print('found')
                                return element
                print('not found')
                try:
                    self.driver.refresh()
                # when the webpage crashes
                except TimeoutException:
                    self.driver.get(self.parsedUrl)
        except WebDriverException:
            print('WebDriverException')
            return False

    # performs the actions necessary to book the seat, when some seat is empty
    def takeSeat(self, element):

        self.clickButton(element.find_element_by_class_name('col_price'), 1)

        # Brings browser to front
        self.driver.execute_script('window.alert("Seat found!!!")')
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        self.clickButton(self.driver.find_element_by_xpath("//*[contains(text(), '" + self.proceedToOrder + "')]"))
        if self.loggedIn:
            self.takeSeatLoggedIn()
        else:
            self.takeSeatNotLoggedIn()

    # actions specific when the user is not logged in
    @classmethod
    def getChromeDriverPath(cls, chrome_version=None):
        system = platform.system()
        basepath = os.path.dirname(__file__)
        if system == 'Windows':
            path = os.path.abspath(os.path.join(basepath, cls.chromeDriverLocations['windows']))
        elif system == 'Darwin':
            path = os.path.abspath(os.path.join(basepath, cls.chromeDriverLocations['mac']))
        else:
            path = os.path.abspath(os.path.join(basepath, cls.chromeDriverLocations['linux']))

        if chrome_version:
            path = path.replace(cls.default_chromedriver_folder_name, str(chrome_version))
        return path

    def takeSeatNotLoggedIn(self):
        self.clickButton(self.driver.find_element_by_name(self.acceptTerms))
        self.clickButton(self.driver.find_element_by_name(self.reserveButtonName))

    # actions specific to when the user is logged in
    def takeSeatLoggedIn(self):
        try:
            self.clickButton(self.driver.find_element_by_name(self.buyButtonName))
        except NoSuchElementException:
            self.clickButton(self.driver.find_element_by_name(self.reserveButtonName))

    # clicks given button (or any element, does not have to be explicitly button)
    def clickButton(self, button, timeout=0):
        time.sleep(timeout)
        # TODO http://stackoverflow.com/questions/24411765/how-to-get-an-xpath-from-selenium-webelement-or-from-lxml
        if button.get_attribute('id'):
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.ID, button.get_attribute('id'))))
            try:
                button.send_keys(Keys.NULL)
            except WebDriverException:
                pass
        button.click()

    # parses hours to format ['HHMM',....] (M = minutes...)
    # hotfix - don't set hour so utc
    def parseHours(self, hours):
        # tm = time.localtime()
        # for i in range(len(hours)):
        #     hour = int(hours[i].replace(':', '')) - (200 if tm.tm_isdst else 100)
        #     hours[i] = '0' + str(hour) if hour < 1000 else str(hour)

        if not hours[0]:
            raise ValueError("No hours specified")

        if hours[0] == '0':
            hours = hours[1:]
        return hours

    # parses date to format 'yyyymmdd'
    def parseDate(self, date):
        if '.' in date:
            parts = date.split('.')
            if len(parts ) < 2:
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
    def setParsedUrl(self, departure, arrival, date, tariff, baseUrl):
        departure = self.getCityCode(departure)
        arrival = self.getCityCode(arrival)
        tariff = self.getTariffCode(tariff)
        tmpUrl = baseUrl.replace(self.urlReplacements['arrival'], arrival)
        tmpUrl = tmpUrl.replace(self.urlReplacements['departure'], departure)
        tmpUrl = tmpUrl.replace(self.urlReplacements['tariff'], tariff)
        self.parsedUrl = tmpUrl.replace(self.urlReplacements['date'], date)

    # gets code of the city
    def getCityCode(self, city):
        return self.cities[str(city)] if self.cities[str(city)] is not None else city

    # gets code of the tarif
    def getTariffCode(self, tariff):
        return self.tariffs[str(tariff.lower())] if self.tariffs[str(tariff.lower())] is not None else tariff

    # creates one page search in format searchPrefixddmmHHMM
    # hotfixing - now searching by time in col_depart value which is H:MM
    def createPageSearch(self, hour, date):
        return hour

    # logs user with given username an password
    def login(self, username, password):
        if len(username) == 0 or len(password) == 0:
            return
        self.driver.get(self.loginUrl)
        login = self.driver.find_element_by_id('login_credit')
        pwd = self.driver.find_element_by_id('pwd_credit')
        login.send_keys(username)
        pwd.send_keys(password)
        pwd.send_keys(Keys.ENTER)
        while not self.checkLoggedIn():
            pass
        self.loggedIn = self.checkLoggedIn()

    def checkLoggedIn(self):
        """
            checks,whether the user is logged in or not
            It is determined from a string on the page which logs out a user
        """
        time.sleep(1)
        logged = True
        try:
            self.driver.find_element_by_xpath("//*[contains(text(), '" + self.notLoggedIn + "')]")
        except NoSuchElementException as e:
            logged = False
        return logged

    @classmethod
    def get_available_chrome_versions(cls):
        versions = []
        for root, subdirs, files in os.walk(cls.chromedriver_folder_path):
            for subdir in subdirs:
                if subdir == cls.default_chromedriver_folder_name:
                    continue
                versions.append(subdir)
        return versions


