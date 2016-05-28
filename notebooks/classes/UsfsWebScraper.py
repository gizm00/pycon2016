# Module for scraping USFS wepbages
# i.e. http://www.fs.usda.gov/recarea/mthood/recarea/?recid=53228

import pandas as pd
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from classes.Scraper import Scraper
import requests
import config
import numpy as np

class UsfsWebScraper(Scraper):

	# helper functions to extract specific fields
	def get_area_status(self, soup) :
		status = None
		try :
			for strong_tag in soup.find_all('strong'):
				if ('Area Status' in unidecode(strong_tag.text)):
					status = unidecode(strong_tag.next_sibling).strip()
		except Exception:
			print('couldnt get area status')

		return status

	# for extracting Latitude,Longitude, and Elevation
	def get_location(self, soup, search_field):
		return_value = None
		try :
			field_div = soup.find_all('div', text=re.compile(search_field))
			value_div = [row.next_sibling.next_sibling for row in field_div]
			return_value  = value_div[0].text.strip()

		except Exception:
			print('couldnt get location info')

		return return_value

	# returns a dataframe of basic campground info
	def get_campground_info(self, soup):
		reservations = conditions = openseason = water = restroom = None
		try :
			tables = soup.find_all('div', {'class': 'tablecolor'})
		except Exception:
			print('couldnt get tables')
			return pd.DataFrame()

		try :
			rows = tables[0].find_all('tr')
			for row in rows:
				if row.th.text == 'Reservations:':
					reservations = unidecode(row.td.text).strip()
				if row.th.text == 'Open Season:':
					openseason = unidecode(row.td.text).strip()
				if row.th.text == 'Current Conditions:':
					conditions = unidecode(row.td.text).strip()
				if row.th.text == 'Water:':
					water = unidecode(row.td.text).strip()
				if row.th.text == 'Restroom:':
					restroom = unidecode(row.td.text).strip()
		except Exception as ex:
			print('couldnt get basic campground info')
			print(ex)
			return pd.DataFrame()
			
		df_info = pd.DataFrame({
				'Reservations':[reservations],
				'OpenSeason':[openseason],
				'CurrentConditions':[conditions],
				'Water':[water],
				'Restroom':[restroom]
			})

		return df_info

	def get_soup(self, row): 
		cg_req = requests.get("http://" + config.LAMP_IP + "/" + row['url'])
		cg_soup = BeautifulSoup(cg_req.text, 'lxml')
		return cg_soup

	# extract information from USFS webpages
	# expects row with columns url and facilityname
	# returns a df with scrape results
	def scrape(self, url_df):
		df_out = pd.DataFrame()
		for index,row in url_df.iterrows() :
			cg_name = row.facilityname
			cg_soup = self.get_soup(row)

			cg_status = self.get_area_status(cg_soup)
			cg_lat = self.get_location(cg_soup, 'Latitude')
			cg_long = self.get_location(cg_soup, 'Longitude')
			cg_elev = self.get_location(cg_soup, 'Elevation')

			df_cg_info = self.get_campground_info(cg_soup)

			df_cg_info = df_cg_info.assign(
				FacilityStatus=cg_status,
				FacilityLatitude=cg_lat,
				FacilityLongitude=cg_long,
				FacilityElevation=cg_elev,
				FacilityName=cg_name
				)

			df_out = df_out.append(df_cg_info)

		# create index
		index_vals = np.arange(df_out.FacilityName.count())
		df_out.index = index_vals
		return df_out

