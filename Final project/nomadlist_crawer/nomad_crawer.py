import requests
from bs4 import BeautifulSoup
import time
import string
import fire
import re
import operator
import pandas as pd
import json
import numpy as np
import csv
class Crawler:
	def crawl(self):
		file = open("index.txt", "r")
		index_html = file.read()
		soup = BeautifulSoup(index_html, 'html.parser')
		cities = soup.find_all("div", attrs={"data-type":"cities"})
		with open('citylist.txt', "w") as f:
			for i, city in enumerate(cities):
				city_slug = city['class'][-1]
				f.write(city_slug+'\n')
		f.close()
		print("Output city clug to citylist.txt")

	def crawlProfile(self):
		print("Crawl nomadlist people profile")
		with open("allPeopleList.txt", "r") as f:
			people_list = f.readlines()
		f.close()
		f_user = open('UserProfile.csv', 'a')
		writer_user = csv.writer(f_user)
		writer_user.writerow(['user', 'trips-count', 'contries_count', 'cities_count'])

		f_trip = open('UserTrips.csv', 'a')
		writer_trip = csv.writer(f_trip)
		for people in people_list:
			resp = requests.get("https://nomadlist.com"+people)
			soup = BeautifulSoup(resp.text, 'html.parser')
			print(people)
			try:
				uid = people[2:]
				trip_count = soup.find('div', class_='trips-count count').contents[0].text
				contries_count = soup.find('div', class_='countries-count count').contents[0].text
				cities_count = soup.find('div', class_='cities-count count').contents[0].text
				# print([uid,trip_count,contries_count,cities_count])
				writer_user.writerow([uid,trip_count,contries_count,cities_count])
			
			except:
				pass
			blocks = soup.find_all('tr', class_=re.compile(r'trip$'))
			for p in blocks:
				try:
					trip_start = p.find('td', class_='trip_start').text
					# trip_length = p.find('td', class_='trip_length').text
					trip_end = p.find('td', class_='trip_end').text
					trip_city = p.find('td', class_='name').contents[0].contents[0].text
					trip_country = p.find('td', class_='country').text

					writer_trip.writerow([uid, trip_start, trip_end, trip_city, trip_country])
				except:
					pass

	def crawlPeople(self):
		print("Crawl nomadlist people")
		people_list = []
		with open("citylist.txt", "r") as f:
			city_slugs = f.readlines()
		f.close()
		for city_slug in city_slugs[300:400]:
			print(city_slug)
			resp = requests.get("https://nomadlist.com/trips/"+city_slug)
			soup = BeautifulSoup(resp.text, 'html.parser')
			blocks = soup.find_all('a', attrs={"class":re.compile(r'avatar'), "href":re.compile(r'@')})
			for p in blocks:
				people_list.append(p['href'])
		people_bag = set(people_list)

		with open("peoplelist.txt", "w") as f:
			for p in people_bag:
				f.write(p+'\n')
		f.close()

	def mergePeople(self):
		merge_peope = set()
		for i in range(4):
			with open("peoplelist"+str(i+1)+'.txt', 'r') as f:
				mini = f.readlines()
				merge_peope.update(mini)
			f.close()
		with open("allPeopleList.txt", "w") as f:
			for p in merge_peope:
				f.write(p)
		f.close()

	def crawlCity(self):
		cities_slugs = []
		print("Crawl nomadlist")
		file = open("index.txt", "r")
		index_html = file.read()
		soup = BeautifulSoup(index_html, 'html.parser')
		cities = soup.find_all("div", attrs={"data-type":"cities"})
		# print(cities[0])
		data = {}
		data_continent = np.full(len(cities),'data_city_continent')
		data_city_name = np.full(len(cities),'data_city_name')
		data_city_country = np.full(len(cities),'data_city_country')
		data_nomad_score = np.zeros([len(cities)])
		data_cost = np.zeros([len(cities)])
		data_internet = np.zeros([len(cities)])
		data_weather = np.zeros([len(cities)])
		data_air_quality = np.zeros([len(cities)])
		data_leisure_quality = np.zeros([len(cities)])
		data_safety = np.zeros([len(cities)])
		data_life = np.zeros([len(cities)])
		data_walk = np.zeros([len(cities)])
		data_fragile_states = np.zeros([len(cities)])
		data_traffic = np.zeros([len(cities)])
		data_healthcare = np.zeros([len(cities)])
		data_happliness = np.zeros([len(cities)])
		data_nightlife = np.zeros([len(cities)])
		data_adult_nightlife = np.zeros([len(cities)])
		data_wifi_availability = np.zeros([len(cities)])
		data_places_to_work = np.zeros([len(cities)])
		data_ac_availability = np.zeros([len(cities)])
		data_friendliness_to_foreigners = np.zeros([len(cities)])
		data_english_speaking = np.zeros([len(cities)])
		data_press_freedon_indes = np.zeros([len(cities)])
		data_female_friendly = np.zeros([len(cities)])
		data_lgbt_friendly = np.zeros([len(cities)])
		data_startup = np.zeros([len(cities)])
		
		for i, city in enumerate(cities):
			city_slug = city['class'][-1]
			cities_slugs.append(city_slug)

			resp = requests.get('https://nomadlist.com/'+city_slug) #craw a city
			soup = BeautifulSoup(resp.text, 'html.parser')
			try:
				city_name = soup.find(class_ = "itemName", itemprop="name").text
				data_city_name[i] = city_name

				city_continent = soup.find('a', class_="breadcrumb_2").contents[0].text
				data_continent[i] = city_continent
			except AttributeError:
				print("city_name AttributeError")
				print(city)
				continue
			city_country = soup.find(class_="itemSub").text
			data_city_country[i] = city_country
			print("City: ",city_name, " Country: ", city_country, " Continent: ", city_continent)
			if(city_country in data):
				data[city_country][city_name]={}
			else:
				data[city_country]={}
				data[city_country][city_name]={}
			cells = soup.find('table', class_="details").find_all("tr")
			nomad_score = cells[0].find(xitemprop="ratingValue").text
			data[city_country][city_name]['nomad_score'] = nomad_score
			data_nomad_score[i] = nomad_score
			for cell in cells[1:]:
				rating = cell.find(class_='rating')
				try:
					key = rating.parent.parent["data-key"].strip()
				except KeyError:
					key = "internet"
				score = rating['class'][-1][-1]
				data[city_country][city_name][key] = score
				if(key=='cost_score'):
					data_cost[i] = score
				elif(key=='internet'):	
					data_internet[i] = score
				elif(key=='weather_score tooltip'):
					data_weather[i] = score
				elif(key=='air_quality_score'):
					data_air_quality[i] = score
				elif(key=='leisure_quality'):
					data_leisure_quality[i] = score
				elif(key=='safety_level'):
					data_safety[i] = score
				elif(key=='life_score'):
					data_life[i] = score
				elif(key=='walkScore_score'):
					data_walk[i] = score
				elif(key=='fragile_states_index_score'):
					data_fragile_states[i] = score
				elif(key=='road_traffic_score'):
					data_traffic[i] = score
				elif(key=='healthcare_score'):
					data_healthcare[i] = score
				elif(key=='happiness_score'):
					data_happliness[i] = score
				elif(key=='nightlife'):
					data_nightlife[i] = score
				elif(key=='adult_nightlife'):
					data_adult_nightlife[i] = score
				elif(key=='wifi_availability'):
					data_wifi_availability[i] = score
				elif(key=='places_to_work_score'):
					data_places_to_work[i] = score
				elif(key=='ac_availability'):
					data_ac_availability[i] = score
				elif(key=='friendliness_to_foreigners'):
					data_friendliness_to_foreigners[i] = score
				elif(key=='english_speaking'):
					data_english_speaking[i] = score
				elif(key=='press_freedom_index_score'):
					data_press_freedon_indes[i] = score
				elif(key=='female_friendly'):
					data_female_friendly[i] = score
				elif(key=='lgbt_friendly'):
					data_lgbt_friendly[i] = score
				elif(key=='startup_score'):
					data_startup[i] = score

		with open('data.json', 'w') as fp:
			json.dump(data, fp)
		
		frame = {'country':data_city_country,
				'city':data_city_name,
				'continent':data_continent,
				'nomad_score': data_nomad_score,
				'cost': data_cost,
				'internet': data_internet,
				'weather': data_weather,
				'air_qiality': data_air_quality,
				'leisure_quality': data_leisure_quality,
				'safety_level': data_safety,
				'life_score': data_life,
				'walkScore_score': data_walk,
				'fragile_states_index_score': data_fragile_states,
				'road_traffic_score': data_traffic,
				'healthcare_score': data_healthcare,
				'happiness_score':data_happliness,
				'nightlife': data_nightlife,
				'adult_nightlife': data_adult_nightlife,
				'wifi_availability': data_wifi_availability,
				'places_to_work_score': data_places_to_work,
				'ac_availability':data_ac_availability,
				'english_speaking':data_english_speaking,
				'press_freedom_index_score':data_press_freedon_indes,
				'lgbt_friendly':data_lgbt_friendly,
				'startup_score':data_startup}

		df = pd.DataFrame.from_dict(frame)
		df.to_csv("data.csv")
		file.close()


if __name__ == "__main__":
	fire.Fire(Crawler)