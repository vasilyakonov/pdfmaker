import dropbox
import os
import fpdf
import uuid
import json
import requests
import shutil
import time
import sys
import random
from urllib2 import urlopen
import urllib






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
        self.ln(20)'''

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

# Instantiation of inherited class
pdf = PDF()
#Get a nice font
pdf.add_font('font', '', 'font.ttf', uni=True)

#Make it work oooh yea
pdf.add_font('sysfont', '', r"/app/font.ttf", uni=True)
pdf.alias_nb_pages()
pages = 5
for page in range(pages):
  if page % 2:
     pdf.add_page()
     pdf.set_font('font', '', 12)
     pdf.cell(0, 10, 'A Quick One Before The Eternal Worm Devours Connecticut', 0, 1, 'C')
     for i in range(1, 41):
         pdf.cell(0, 10, 'Printing line %s ' % uuid.uuid4() + str(i) , 0, 1)
  else:
  
     pdf.add_page('P', 'A4', False)
     pdf.set_font('font', '', 12)
     pdf.cell(0, 10, 'King of Carrot Flowers', 0, 1)
     
     dbx = dropbox.Dropbox(os.environ['A_TOKEN2'])
     dbx.users_get_current_account()
     dbx.files_download_to_file('/app/cool.json', '/cavs vs warriors/urls.json')
  
     
     images_response = open('cool.json').read()
     the_images = json.loads(images_response)
     images_list = []


     for f in the_images:
      #for k, v in f.iteritems():
         images_list.append(f)

     n = random.randint(0,len(images_list))
     the_image = images_list[n]

     url = '%s' % (the_image)
     response = requests.get(url, stream=True)
     #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
     with open('finalImage.jpg', 'wb') as out_file:
       shutil.copyfileobj(response.raw, out_file)   
     pdf.image('finalImage.jpg', x = random.randint(10, 100), y = random.randint(10, 100), w = 0, h = 0, type = 'jpg', link = '')
pdf.output('tuto3.pdf', 'F')


#Send to dropbox
from dropbox.files import WriteMode
access_token = os.environ['A_TOKEN2']
file_from = '/app/tuto3.pdf'  
file_to = '/King of Carrot Flowers/tuto3.pdf'    
def upload_file(file_from, file_to):
    dbx = dropbox.Dropbox(access_token)
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(), file_to, mode=WriteMode('overwrite'))
upload_file(file_from,file_to,)