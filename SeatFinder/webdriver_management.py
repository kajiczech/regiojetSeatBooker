from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import os
import platform

seat_finder_directory_path = os.path.dirname(os.path.realpath(__file__))

chrome_driver_dir = os.path.join('src', 'chromedrivers')
chromedriver_folder_path = os.path.join(seat_finder_directory_path, 'src', 'chromedrivers')
default_chromedriver_folder_name = 'default'
chromeDriverLocations = {
    'mac': os.path.join(chromedriver_folder_path, default_chromedriver_folder_name, 'mac'),
    'windows': os.path.join(chromedriver_folder_path, default_chromedriver_folder_name, 'win.exe'),
    'linux': os.path.join(chromedriver_folder_path, default_chromedriver_folder_name, 'lin')
}


def get_chrome_driver_path(chrome_version=None):
    system = platform.system()
    if system == 'Windows':
        path = chromeDriverLocations['windows']
    elif system == 'Darwin':
        path = chromeDriverLocations['mac']
    else:
        path = chromeDriverLocations['linux']

    if chrome_version:
        path = path.replace(default_chromedriver_folder_name, str(chrome_version))
    return path


def get_available_chrome_versions():
    versions = []
    for root, subdirs, files in os.walk(chromedriver_folder_path):
        for subdir in subdirs:
            if subdir == default_chromedriver_folder_name:
                continue
            versions.append(subdir)
    versions.sort()
    return versions


def find_chromedriver():
    versions = get_available_chrome_versions()
    for version in versions:
        try:
            return get_chromedriver(version)
        except WebDriverException:
            pass
    return None


def find_latest_chromedriver_version():
    versions = get_available_chrome_versions()
    latest_version = None
    for version in versions:
        try:
            get_chromedriver(version)
            if not latest_version or version > latest_version:
                latest_version = version
        except WebDriverException:
            pass
    return latest_version


def get_chromedriver(chrome_version):
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--no-proxy-server')
    chrome_driver_path = get_chrome_driver_path(chrome_version)
    os.environ["webdriver.chrome.driver"] = chrome_driver_path
    return webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
