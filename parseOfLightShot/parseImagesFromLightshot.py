import os
import time

import requests
from bs4 import BeautifulSoup

# headers
HEADERS = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}

# creating a folder to save our pictures there
try:
    os.mkdir('C:\\imageslight')
except FileExistsError:
    pass


# Geting page
def get_page(number):
    r1 = requests.get(f"https://prnt.sc/pt{number}", headers=HEADERS, params=None)
    return r1


# Geting images
def get_img(html, number):
    # First of all we parse a web page to get a link on the img
    soup = BeautifulSoup(html, 'html.parser')
    src = soup.find("div", class_='js-image-wrap').find_next("div", class_='js-image-pic').find_next("img",
                                                                                                     class_='screenshot-image').get(
        "src")
    # Some pictures have been already deleted and almost all of they are having img with this link
    # We will ignor it
    list_of_e_src = src.split('//')
    isNotImg = list_of_e_src[1].split('.')
    if src == '//st.prntscr.com/2022/09/11/1722/img/0_173a7b_211be8ff.png' or isNotImg[1] == "imageshack":
        pass
    else:
        # If we get a link of right picture
        # We will parse page of this picture
        r2 = requests.get(src, headers=HEADERS, params=None)

        # save picture in the folder which we created
        with open(f'C:\\imageslight\\{number}.png', 'wb') as file:
            file.write(r2.content)
            print(f"Image {number}.png has successfully parsed")


# The main func that starts parsing
def parse():
    # A score to know what page we are on
    # Also it is very important number because,
    # Link of images looks like this -> https://prnt.sc/pt{411}
    # And this number we need to change to get another picture

    # start position
    b = 430
    while b < 631:  # finish position
        html = get_page(b)
        if html.status_code == 200:
            get_img(html.text, number=b)
        b += 1


# Start parsing and measure  a time of this parse
t1 = time.time()
parse()
t2 = time.time()

print(f'Parsing time was approx {int(t2 - t1)}s')
