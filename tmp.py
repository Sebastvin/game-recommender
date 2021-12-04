import requests, lxml, re, json
from bs4 import BeautifulSoup
import urllib
import requests
import time, random
import pandas as pd


def get_images_data(idx, game_name):
    agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 "
              "Safari/537.36 Edg/91.0.864.59",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 "
              "Safari/601.3.9",
              "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
              ]

    random_agent = random.randint(0, 5)

    headers = {
        "User-Agent": agents[random_agent],
        'referer': 'https://www.google.com/'
    }

    params = {
        "q": game_name + ' game',
        "tbm": "isch",
        "ijn": "0",
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    # print('\nGoogle Images Metadata:')
    # for google_image in soup.select('.isv-r.PNCib.MSM1fd.BUooTd'):
    #     title = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['title']
    #     source = google_image.select_one('.fxgdke').text
    #     link = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['href']
    #     print(f'{title}\n{source}\n{link}\n')

    # this steps could be refactored to a more compact
    all_script_tags = soup.select('script')
    #
    # # # https://regex101.com/r/48UZhY/4
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    #
    # # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # # if you try to json.loads() without json.dumps it will throw an error:
    # # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",',
                                           matched_images_data_json)

    # # https://regex101.com/r/NnRg27/1
    # matched_google_images_thumbnails = ', '.join(
    #     re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
    #                str(matched_google_image_data))).split(', ')

    # print('Google Image Thumbnails:')  # in order
    # for fixed_google_image_thumbnail in matched_google_images_thumbnails:
    #     # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
    #     google_image_thumbnail_not_fixed = bytes(fixed_google_image_thumbnail, 'ascii').decode('unicode-escape')
    #
    #     # after first decoding, Unicode characters are still present. After the second iteration, they were decoded.
    #     google_image_thumbnail = bytes(google_image_thumbnail_not_fixed, 'ascii').decode('unicode-escape')
    #     print(google_image_thumbnail)

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '', str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                                       removed_matched_google_images_thumbnails)

    counter = 0
    print('\nFull Resolution Images: ', idx)  # in order
    for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
        original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')
        print(original_size_img)

        # ------------------------------------------------
        # Download original images

        # print(f'Downloading {index} image...')

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', agents[random_agent])]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(original_size_img, f'pictures/{idx}_{counter}.jpg')
        if counter == 2:
            return None
        counter += 1


game_names = pd.read_csv("datasets/final_dataset.csv")

for index, row in game_names[:3].iterrows():
    get_images_data(index, row['name_game'])
    timeout = random.randint(5, 30)
    print("Next request: ", timeout)
    time.sleep(timeout)
