# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import string
import fire
import re
import operator

class Crawler:
	def has_keyword(self, article, keyword):
		try:
			range_end = article.find('span', class_='f2', string=re.compile("^※ 發信站"))
			if(range_end.find_previous(string=re.compile(keyword))):
				return True
			else:
				return False
		except Exception:
			print("Find exception in ", article.find('title').text)
		return False
	
	#找符合輸入日期區間而且含有輸入keyword的文章，輸出那些文章所含的所有圖片url
	def keyword(self, keyword, start_date, end_date):
		print("Find articles with keyword", keyword)
		all_image_urls = []
		f = open("all_articles.txt", "r")
		for line in f:
			raw = line.split(',')
			date = raw[0]
			url = raw[-1]
			#print(url)
			if(int(date)>=int(start_date) and int(date)<=int(end_date)):
				#print('#Article: ',url)
				resp = requests.get(url.strip())
				soup = BeautifulSoup(resp.text,'html.parser')
				if(self.has_keyword(soup, keyword)):
					#print('Article: ', url)
					image_urls = self.find_article_image_url(soup)
					all_image_urls += image_urls
				
			if(int(date) > int(end_date)):
				break
		with open('keyword('+keyword+')['+str(start_date)+'-'+str(end_date)+'].txt', 'a') as f:
			for u in all_image_urls:
				#print(u)
				f.write(u+'\n')

	def find_article_image_url(self, article):
		image_urls = []
		try:
			content = article.find('div', id='main-container')
			links = content.find_all('a')
			for link in links:
				url = link['href']
				img_format = ['.jpg', '.jpeg', '.png', 'gif'] #用來判斷是否為文章連結的字尾串
				if (any(url.endswith(end) for end in img_format)):
					image_urls.append(url)
		except Exception:
			print("Find exception in ", article.find('title').text)
			pass
		return image_urls

	#計算輸入日期區間的爆文數量，並輸出爆文內所有圖片的url
	def popular(self, start_date, end_date):
		print("Find popular in ", start_date, "-", end_date)
		
		pop_num = 0 #爆文數量
		all_image_urls = [] #爆文內所有圖片的url
		f = open("all_popular.txt", "r") #從爬下來的爆文列表中找
		for line in f:
			raw = line.split(',')
			date = raw[0]
			url = raw[-1]
			#print(url)
			if(int(date)>=int(start_date) and int(date)<=int(end_date)): #判斷符合時間區間的文章
				#print('#Article: ',url)
				pop_num += 1
				resp = requests.get(url.strip())
				soup = BeautifulSoup(resp.text,'html.parser')
				image_urls = self.find_article_image_url(soup)
				all_image_urls += image_urls
				
			if(int(date) > int(end_date)):
				break
		# Output result
		with open('popular['+str(start_date)+'-'+str(end_date)+'].txt', 'a') as f:
			print('number of popular articles:', pop_num)
			f.write('number of popular articles: '+str(pop_num)+'\n')
			for u in all_image_urls:
					f.write(u+'\n')

	def find_article_push_boo(self, article, push_user, boo_user, total_push, total_boo):
		# container = article.find('div', id="main-content")
		all_push_boo = article.find_all('div',class_='push')

		for push_boo in all_push_boo:
			#print(push_boo)
			try:
				mark = push_boo.span.text.strip()
				if(mark=="推"):
					total_push += 1
					userid = push_boo.find('span', class_='f3 hl push-userid').text
					if(userid in push_user):
						push_user[userid] += 1
					else:
						push_user[userid] = 1
				elif(mark=="噓"):
					total_boo += 1
					userid = push_boo.find('span', class_='f3 hl push-userid').text
					if(userid in boo_user):
						boo_user[userid] += 1
					else:
						boo_user[userid] = 1
			except Exception as inst:
				print(push_boo)
				pass

		return push_user, boo_user, total_push, total_boo

	#計算在輸入的日期範圍內文章的推噓文數量，以及前十名推文、前十名虛文的user id
	def push(self,start_date, end_date):
		print("Find push in ", start_date, "-", end_date)
		
		push_user = {} #所有推文的user
		boo_user = {} #所有噓文的user
		total_push = 0 #總推文量
		total_boo = 0 #總需文量
		
		f = open("all_articles.txt", "r")
		for line in f:
			raw = line.split(',')
			date = raw[0]
			url = raw[-1]
			#print(url)
			if(int(date)>=int(start_date) and int(date)<=int(end_date)):
				#print(url)
				resp = requests.get(url.strip())
				soup = BeautifulSoup(resp.text,'html.parser')
				push_user, boo_user, total_push, total_boo = self.find_article_push_boo(soup, push_user, boo_user, total_push, total_boo)
			if(int(date) > int(end_date)):
				break

		sorted_push_user = sorted(push_user.items(), key=operator.itemgetter(1), reverse=True)
		sorted_boo_user = sorted(boo_user.items(), key=operator.itemgetter(1), reverse=True)
		
		with open('push['+str(start_date)+'-'+str(end_date)+'].txt', 'a') as f:
			print("all like: "+str(total_push))
			print("all boo: "+str(total_boo))
			f.write("all like: "+str(total_push)+'\n')
			f.write("all boo: "+str(total_boo)+'\n')
			for i in range(0,10):
				print("like #"+str(i+1)+": "+str(sorted_push_user[i][0])+' '+str(sorted_push_user[i][1]))
				f.write("like #"+str(i+1)+": "+str(sorted_push_user[i][0])+' '+str(sorted_push_user[i][1])+'\n')
			for i in range(0,10):
				print("boo #"+str(i+1)+": "+str(sorted_boo_user[i][0])+' '+str(sorted_boo_user[i][1]))
				f.write("boo #"+str(i+1)+": "+str(sorted_boo_user[i][0])+' '+str(sorted_boo_user[i][1])+'\n')

	def crawl_article(self, article):
		if(article.text.find('※ 發信站')==-1): #不含‘※ 發信站’的文章認定為不符合格式
			# print("# Ignore article: ", article.find('span', class_='article-meta-value').text)
			return False
		
		#找時間，2017很多文章時間格式不對，沒有想到更好的方法所以這裡有點用暴力法解決
		#本來應該要判斷是否為2017年，這裡為了避免去處理各種例外，所以改成判斷'不是2018握2016的文章'
		#因為在限制的文章列表頁面張已經確認過只有符合時間標準格式的2018, 2016年文章，所以比較好處理
		content = article.find("div", id="main-content").text.replace('時間: ', '時間')
		p = content.find('時間') #找到第一個「時間」出現的位置
		#print("place", p)
		year = 'time error'
		if(p >-1):
			article_time = content[p+2:p+26] #找到「時間」之後一般會時間的字串，但是「時間」也有可能出現在標題
			print(article_time)
			try:
				struct_time = time.strptime(article_time, '%a %b %d %H:%M:%S %Y')
				year = struct_time.tm_year
			except ValueError: #這裡處理「時間出現在標題的時候」，從第一個「時間」位置之後往下找第二的「時間」出現的位置
				p = content.find('時間', p+2)
				article_time = content[p+2:p+26]
				try:
					struct_time = time.strptime(article_time, '%a %b %d %H:%M:%S %Y')
					year = struct_time.tm_year
					print("correct:", article_time)
				except:
					pass

		if(year!=2018 and year!=2016): #如果年份不是2018, 2016就是我們要的2017年的文章
			return True
		
	def crawl_page(self, page):
		article_list = page.find_all("div", class_="r-ent") #從文章列表裡取得該頁的文章
		for article in article_list:	#for loop訪問一頁中的每個文章，取得符合條件的文章，並輸出該文章的標題、日期、連結
			title = article.find('div', 'title')
			if(title.text.split(' ')[0].strip().find("公告")==-1): #忽略公告文文章
				#print(title.text)
				if(title.find('a')):  # 有超連結，表示文章存在未被刪除
					href = title.find('a')['href']
					resp = requests.get('https://www.ptt.cc'+href)
					soup = BeautifulSoup(resp.text, 'html.parser')
					if(self.crawl_article(soup)): #訪問文章頁面確認格式符合、年份符合
						date = article.find('div', class_='date').text.strip().replace('/','')
						title = title.text.strip('\n')
						url = href
						with open('all_articles.txt', 'a') as f: #輸出一行該文章資訊到all_articles.txt
							f.write(date+','+title+','+'https://www.ptt.cc'+url+'\n')

						if(article.find('div', 'nrec').text.find("爆")>-1): #如果是爆文則也要輸出到all_popular.text
							with open('all_popular.txt', 'a') as f:
								f.write(date+','+title+','+'https://www.ptt.cc'+url+'\n')

	#Crawl 2017 ptt Beauty版文章，輸出所有文章的list，輸出所有爆文的list
	def crawl(self):
		print("Crawl 2017 ptt Beauty版文章")
		
		for i in range(1999,2352): #爬2017年文章所在的頁面
			resp = requests.get('https://www.ptt.cc/bbs/Beauty/index'+str(i)+'.html')
			soup = BeautifulSoup(resp.text, 'html.parser')
			self.crawl_page(soup)
		
		print("Output file: all_articles.txt, all_popular.txt")

if __name__ == "__main__":
	fire.Fire(Crawler)