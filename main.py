import os
import time
from glob import glob
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from instabot import Bot
from PIL import Image


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    fly_lib = response.json()
    image_urls = []

    # search last run with photo
    flight_number = -1
    while not bool(image_urls):
        image_urls = fly_lib[flight_number]['links']['flickr']['original']
        flight_number -= 1
    return image_urls


def fetch_news_id_hubble(url):
    response = requests.get(url)
    response.raise_for_status()
    fly_lib = response.json()
    news_id = fly_lib[1]['id']
    return news_id


def get_hubble_image_urls(news_id):
    collection_url = f' http://hubblesite.org/api/v3/image/{news_id}'
    response = requests.get(collection_url)
    response.raise_for_status()
    fly_lib = response.json()
    image_urls = fly_lib['image_files'][0]['file_url']
    return image_urls


def add_protocol_to_url(image_url, protocol):
    if protocol == 'https':
        return image_url
    new_image_url = f'https:{image_url}'
    return new_image_url


def save_image(image_url, folder, image_name, image_number):
    parts_url = urlparse(image_url)
    protocol = parts_url.scheme
    image_url = add_protocol_to_url(image_url, protocol)
    url_path = parts_url.path
    root_url, image_format = os.path.splitext(url_path)
    file_name = f'{folder}/{image_name}-{image_number}{image_format}'
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    with open(file_name, 'wb') as file:
        file.write(response.content)


def download_images(image_urls, folder, image_name):
    if type(image_urls) == str:
        image_number = 0
        return save_image(image_urls, folder, image_name, image_number)
    for image_number, image_url in enumerate(image_urls):
        save_image(image_url, folder, image_name, image_number)


def resize_images(paths, folder_name):
    image_number = 1
    image_size = (1080, 1080)
    for path in paths:
        for directory, folder, files in os.walk(path):
            for image in files:
                image_name, image_format = os.path.splitext(image)
                new_image = Image.open(f'{directory}/{image}')
                new_image.thumbnail(image_size)
                new_image.save(
                    f'{folder_name}/{image_number}-{image_name}.jpg',
                    format='JPEG')
                image_number += 1


def open_pics_list():
    try:
        with open('pics.txt', 'r', encoding='utf8') as f:
            posted_pics = f.read().splitlines()
    except FileNotFoundError:
        posted_pics = []
    return posted_pics


def get_caption(description_file, pic_name):
    if os.path.isfile(description_file):
        with open(description_file, 'r') as file:
            caption = file.read()
    else:
        caption = pic_name.replace('-', ' ')
    return caption


def create_pic_name(pic, folder_path):
    pic_name = pic[:-4].split('-')
    pic_name = '-'.join(pic_name[1:])
    description_file = f'{folder_path}/{pic_name}.txt'
    return description_file, pic_name


def upload_photo_instagram(instagram_login, instagram_password,
                           folder_name):
    posted_pics = open_pics_list()

    # timeout = 24 * 60 * 60  # pics will be posted every 24 hours
    timeout = 5

    bot = Bot()
    bot.login(username=instagram_login, password=instagram_password,
              use_cookie=False)
    while True:
        folder_path = folder_name
        pics = glob(f'{folder_path}/*.jpg')
        pics = sorted(pics)
        try:
            for pic in pics:
                if pic in posted_pics:
                    continue
                description_file, pic_name = create_pic_name(pic, folder_path)
                caption = get_caption(description_file, pic_name)

                bot.upload_photo(pic, caption=caption)

                if bot.api.last_response.status_code != 200:
                    raise requests.HTTPError('нет доступа к Instagram')
                posted_pics.append(pic)
                with open('pics.txt', 'a', encoding='utf8') as f:
                    f.write(f'{pic}\n')

                time.sleep(timeout)

        except requests.HTTPError as exception:
            print(exception)
        time.sleep(60)


if __name__ == '__main__':
    load_dotenv()

    instagram_login = os.getenv('LOGIN_INSTAGRAM')
    instagram_password = os.getenv('PASSWORD_INSTAGRAM')

    spacex_url = 'https://api.spacexdata.com/v4/launches'
    hubble_url = 'https://hubblesite.org/api/v3/images'
    hubble_folder = 'hubble_images'
    spacex_folder = 'spacex_images'
    instagram_folder = 'instagram_images'
    hubble_image_name = 'hubble'
    spacex_image_name = 'spacex'

    Path(spacex_folder).mkdir(parents=True, exist_ok=True)
    spacex_image_urls = fetch_spacex_last_launch(spacex_url)
    download_images(spacex_image_urls, spacex_folder, spacex_image_name)

    Path(hubble_folder).mkdir(parents=True, exist_ok=True)
    hubble_news_id = fetch_news_id_hubble(hubble_url)
    hubble_image_urls = get_hubble_image_urls(hubble_news_id)
    download_images(hubble_image_urls, hubble_folder, hubble_image_name)

    Path(instagram_folder).mkdir(parents=True, exist_ok=True)
    folders = [spacex_folder, hubble_folder]
    resize_images(folders, instagram_folder)

    upload_photo_instagram(instagram_login, instagram_password,
                           instagram_folder)
