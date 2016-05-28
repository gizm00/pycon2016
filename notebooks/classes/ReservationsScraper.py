# Module for scraping recreation.gov wepbages for reservation availability
# i.e. http://www.recreation.gov/camping/trillium/r/campgroundDetails.do?contractCode=NRSO&parkId=71614

from classes.Scraper import Scraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
from datetime import timedelta, date
import sys
import requests
import config
import numpy as np

class ReservationsScraper(Scraper):

	def __init__(self) :
		self.local_prefix = "http://" + config.LAMP_IP + "/"

		print('starting display')
		self.display = Display(visible=0, size=(1024, 768))
		self.display.start()

		

	def connect_to_page(self, url):
		try:

			self.browser.get(url)
			self.browser.set_script_timeout(30)
			self.browser.set_page_load_timeout(30) # seconds
			print("browsed to reservation.html")

		except Exception as ex:
			print("ReservationsScraper.connect_to_page(): Unable to open url: " + url)
			print(ex)

	def submit_request(self, start_date, end_date) :
		form = self.browser.find_element_by_name('unifSearchForm')
		arrival = form.find_element_by_name('arrivalDate')
		departure = form.find_element_by_name('departureDate')
		arrival.send_keys(start_date)
		departure.send_keys(end_date)
		self.browser.find_element_by_name("submit").click()

	def get_availability(self) :
		element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "matchSummary")))
		soup = BeautifulSoup(self.browser.page_source, 'lxml')
		divs = soup.findAll('div', attrs={"class" : 'matchSummary'})
		query_result = divs[0].text
		availability_info = query_result.split(' ')
		return availability_info[0]

	# input url_df expected to have columns FaciliyLatitude,FacilityLongitude,FacilityName,start_date, stay_lengthand url
	def scrape(self, url_df):
		df_res_info = pd.DataFrame()
		print("getting reservation.html")
		print('setting up web browser')
		p = webdriver.FirefoxProfile()   
		p.set_preference("webdriver.log.file", "/tmp/selenium_firefox")
		self.browser = webdriver.Firefox(p)
		self.browser.set_window_size(1366, 768)
		
		for index,row in url_df.iterrows() :
			self.connect_to_page(self.local_prefix + row.url)
			self.submit_request(row.start_date,row.stay_length)
			sites_available = self.get_availability()

			df_res_info = df_res_info.append(pd.DataFrame({
				'FacilityLatitude':[row.FacilityLatitude],
				'FacilityLongitude':[row.FacilityLongitude],
				'SitesAvailable':[sites_available],
				'FacilityName':[row.FacilityName]
				}))



		# create index
		index_vals = np.arange(df_res_info.FacilityName.count())
		df_res_info.index = index_vals

		# closedown browser
		print("closing browser")
		self.browser.quit()
		self.display.stop()
		return df_res_info

