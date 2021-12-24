# code from https://medium.com/geekculture/scrape-google-images-with-python-f9a20cda1355

import requests, lxml, re, json
from bs4 import BeautifulSoup
import urllib
import random
import time





def get_img(titleGame: str, index):
    agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102",
              "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 "
              "OPR/38.0.2220.41",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 "
              "Safari/537.36 Edg/91.0.864.59",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 "
              "Safari/601.3.9",
              "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
              ]

    random_agent = random.randint(0, 6)


    headers = {
        "User-Agent": agents[random_agent]
    }

    params = {
        "q": titleGame + ' game',
        "tbm": "isch",
        "ijn": "0",
    }

    timeout = random.randint(5, 30)
    print(timeout)
    time.sleep(timeout)
    html = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    all_script_tags = soup.select('script')

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ', '.join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(', ')


    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '', str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                                       removed_matched_google_images_thumbnails)


    # print('\nFull Resolution Images:')  # in order
    counter = 0

    for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
        counter +=1
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
        original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')

        if 'wikia' not in original_size_img:
            return original_size_img
        print(original_size_img)
        counter += 1

    print('\nFull Resolution Images:')  # in order
    for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
        original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')
        print(original_size_img)

        # ------------------------------------------------
        # Download original images

        # print(f'Downloading {index} image...')

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(original_size_img, f'pictures/{index}_{counter}.jpg')







def listUrls(data):
    result = []
    for x in data:
        result.append(get_img(x))

    return result

