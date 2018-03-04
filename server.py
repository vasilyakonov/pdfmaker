# -*- coding: utf-8 -*-

import requests
import os
import tweepy
import shutil
import PIL
import pip
import aggdraw
import urllib
import json
import random
import dropbox
import fpdf


url2 = 'https://vignette.wikia.nocookie.net/logopedia/images/e/ee/Burger_King_Logo.svg.png/revision/latest?cb=20121104001421'
response = requests.get(url2, stream=True)
     #you shold be able to specify a path, check glitch support for writing to ASSETS or to .tmp folder
with open('logo_pb.png', 'wb') as out_file:
  shutil.copyfileobj(response.raw, out_file)


from fpdf import FPDF

class PDF(FPDF):
    def header(self):
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
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# Instantiation of inherited class
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)
for i in range(1, 41):
    pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
pdf.output('tuto2.pdf', 'F')