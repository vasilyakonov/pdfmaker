# -*- coding: utf-8 -*-
import dropbox
import os
import fpdf
import uuid
import json
import requests
import shutil
import random
from urllib2 import urlopen
import urllib
import uuid
import logging
import aggdraw
import tweepy
from time import strftime, gmtime
logging.basicConfig(filename='myapp.log',level=logging.DEBUG)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

subscription_key = os.environ['MicroKEy']
assert subscription_key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
search_response = requests.get('https://botwiki.org/api/corpora/data/technology/new_technologies.json')
the_search = search_response.json()
search_list = []
for f in the_search["technologies"]:
  #for k, v in f.iteritems():
    search_list.append(f)
n = random.randint(0,len(search_list))
search = search_list[n]
if not search_list:
  print("List is empty")
  logging.info("List is empty")
search_term = "%s" % search
print search_term
logging.info(search_term)
import requests
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = {"q": search_term, "license": "Any", "imageType": "photo", 'size':'large'}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"]]#[:100]]

print (thumbnail_urls)
logging.info (thumbnail_urls)

d = thumbnail_urls

j = json.dumps(d, indent=4)
f = open('cool.json', 'w')
print >> f, j
f.close()

'''dbx = dropbox.Dropbox(os.environ['A_TOKEN2'])
dbx.users_get_current_account()
dbx.files_download_to_file('/app/cool.json', '/cavs vs warriors/urls.json')'''


images_response = open('cool.json').read()
the_images = json.loads(images_response)
images_list = []

for f in the_images:
   images_list.append(f)
print len(images_list)
logging.info(len(images_list))

url = 'https://cdn.glitch.com/d232fe49-a0b6-47bc-aa18-89366467f9a0%2Fstandard-book-webfont.ttf?1520626665885'
response = requests.get(url, stream=True)
 #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
with open('font.ttf', 'wb') as out_file:
  shutil.copyfileobj(response.raw, out_file)

url2 = 'https://cdn.glitch.com/d232fe49-a0b6-47bc-aa18-89366467f9a0%2F%D0%91%D0%B5%D0%B7%D1%8B%D0%BC%D1%8F%D0%BD%D0%BD%D1%8B%D0%B8%CC%86-2.png?1520765729676'
response = requests.get(url2, stream=True)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
with open('cover.png', 'wb') as out_file:
  shutil.copyfileobj(response.raw, out_file)
if len(images_list) < 31:
  print "Sorry, Not Enough Urls!"
  logging.info("Less than 29, did not allow")
else:
  #Create pdf
  from fpdf import FPDF

  class PDF(FPDF):

      '''def header(self):
          # Logo
          self.image('logo_pb.png', 10, 8, 33)
          # Arial bold 15
          self.set_font('Arial', 'B', 15)
          # Move to the right
          self.cell(80)
          # Title
          self.cell(30, 10, 'Title', 1, 0, 'C')
          # Line break
          self.ln(20)

      # Page footer
      def footer(self):
          # Position at 1.5 cm from bottom
          self.set_y(-15)
          self.set_x(60)
          # Arial italic 8
          self.set_font('ARIAL', '', 10)
          # Page number
          self.cell(0, 10, str(self.page_no()), 0, 0, 'L')'''

  # Instantiation of inherited class
  pdf = PDF()
  #pdf.set_compression('on')
  #Get a nice font
  pdf.add_font('fonty', '', 'font.ttf', uni=True)
  #pdf.add_font('fonble', '', '/app/font2.ttf', uni=True)
  #pdf.add_font('font2', '', 'font2.ttf', uni=True)
   # Page footer


  #Make it work oooh yea
  #pdf.add_font('sysfont', '', r"/app/font.ttf", uni=True)

  pdf.alias_nb_pages()
  pages = 10
  pdf.set_left_margin(30)
  #Cover
  pdf.add_page('P', 'A4', False)
  pdf.image('cover.png', x = 0, y = 0, w = 210, h = 297, type = 'png', link = '')
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('cover.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('cover.jpg', x = 104.9, y = 1.5, w = 103.7, h = 85, type = 'jpg', link = '')
  os.remove('/app/cover.jpg')

  pdf.set_font('fonty', '', 6)
  pdf.set_left_margin(103.8)
  issue_id = uuid.uuid4()
  #pdf.set_y = 57.5
  pdf.cell(0, 160,'Issue id: %s' % uuid.uuid4(), 0, 1, 'L')
  logging.info(issue_id)
  pdf.set_left_margin(30)
  pdf.add_page('P', 'A4', False)
  #pdf.set_top_margin(10)
  #2
  pdf.add_page('P', 'A4', False)
  f = open('text_page.txt')
  file = f.read()
  pdf.set_font('fonty', '', 10)
  #for i in range(1, 20):
  pdf.multi_cell(120, 9, file, 0, 1)
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

 #3
  '''pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('1.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('1.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/1.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 1), 0, 0, 'L')'''
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('2.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('2.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/2.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('3.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('3.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/3.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('4.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('4.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/4.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('5.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('5.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/5.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('6.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('6.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/6.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('7.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('7.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/7.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('8.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('8.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/8.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('9.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('9.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/9.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('10.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('10.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/10.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('11.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('11.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/11.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('12.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('12.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/12.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('13.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('13.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/13.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('14.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('14.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/14.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('15.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('15.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/15.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('16.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('16.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/16.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('17.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('17.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/17.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('18.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('18.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/18.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('19.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('19.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/19.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('20.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('20.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/20.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('21.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('21.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/21.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('22.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('22.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/22.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('23.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('23.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/23.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('24.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('24.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/24.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('25.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('25.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/25.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('26.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('26.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/26.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')


  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('27.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('27.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/27.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')

  '''#4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('28.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('28.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/28.jpg')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('29.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('29.jpg', x = 30, y = 30, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/29.jpg')
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('30.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('30.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/30.jpg')

  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('31.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('31.jpg', x = 30, y = 30, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/31.jpg')'''
  #4    
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  print url
  logging.info(url)
  response = requests.get(url, stream=True)
  images_list.remove(url)
  print len(images_list)
  logging.info(len(images_list))
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('32.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('32.jpg', x = 0, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/32.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  #3
  pdf.add_page('P', 'A4', False)
  url = '%s' % (random.choice(tuple(images_list)))
  response = requests.get(url, stream=True)
  images_list.remove(url)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('27.jpg', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('27.jpg', x = 30, y = 0, w = 0, h = 0, type = 'jpg', link = '')
  os.remove('/app/27.jpg')
  pdf.set_y(265)
  pdf.set_x(60)
  pdf.cell(0, 10, str(pdf.page_no() - 2), 0, 0, 'L')
  pdf.add_page
  pdf.image('cover.png', x = 0, y = 0, w = 210, h = 297, type = 'png', link = '')
  url = 'https://cdn.glitch.com/d232fe49-a0b6-47bc-aa18-89366467f9a0%2FGUIDE.png?1520862093240'
  response = requests.get(url, stream=True)
  #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
  with open('GUIDE.png', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)   
  pdf.image('GUIDE.png', x = 0, y = 0, w = 210, h = 297, type = 'png', link = '')
  pdf.add_page('P', 'A4', False)
  


  pdf.output('ISSUE.pdf', 'F')


  #Send to dropbox
  from dropbox.files import WriteMode
  access_token = os.environ['A_TOKEN2']
  file_from = '/app/ISSUE.pdf'  
  file_to = '/JOURNAL FOR RAW VISUAL DATA/ISSUE.pdf'    
  def upload_file(file_from, file_to):
      dbx = dropbox.Dropbox(access_token)
      f = open(file_from, 'rb')
      dbx.files_upload(f.read(), file_to, mode=WriteMode('overwrite'))
  upload_file(file_from,file_to)
  '''def tweet_image():
    url = '%s' % random.choice(tuple(images_list))
    response = requests.get(url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        from PIL import Image, ImageDraw, ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        im = Image.open("img.jpg")
        font = aggdraw.Font((255, 255, 255), "/app/font.ttf", 48)
        d = aggdraw.Draw(im)
        p = aggdraw.Pen((255, 255, 255), 100)
        b = aggdraw.Brush((255, 255, 255))
        #d.ellipse((0, 0, 500, 500), p, b)
        #d.ellipse((0, 500, 500, 0), p, b)
        d.text((90, im.height / 2 - (im.height / 8)), "NEW ISSUE!", font)
        d.flush()
        del d

  # write to stdout
        im.save('/app/img.jpg')
        del response
    filename = 'img.jpg'
    text = "http://bit.ly/2FrONFY"
    return filename,text
  
  
  def tweet(file,text):
    # Twitter authentication
    auth = tweepy.OAuthHandler(os.environ['C_KEY'], os.environ['C_SECRET'])
    auth.set_access_token(os.environ['A_TOKEN'], os.environ['A_TOKEN_SECRET'])
    api = tweepy.API(auth)

    api.update_with_media(file,text)
    # you should read the img directory and delete file after posting
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
      log(e.message)
    else:
      log("Tweeted: " + text)
  logfile_path = '/app/log.log'
  def log(tweet):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_path), 'a+') as f:
      t = strftime("%d %b %Y %H:%M:%S", gmtime())
      f.write("\n" + t + " ")

  if __name__ == "__main__":
    image,text = tweet_image()
    tweet(image,text)'''
logging.info('Done!') 
print 'Done!'
