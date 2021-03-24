import os
import glob
import sys
import time
import requests
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
from io import open


sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    fly_lib = response.json()
    images_url = []

    #search last run with photo
    flight_number = -1
    while bool(images_url) != True:
        images_url = fly_lib[flight_number]['links']['flickr']['original']
        flight_number -= 1
    return images_url


def fetch_news_id_hubble(url):
    response = requests.get(url)
    response.raise_for_status()
    fly_lib = response.json()
    news_id = fly_lib[1]['id']
    return news_id


def get_url_image_hubble(news_id):
    collection_url = f' http://hubblesite.org/api/v3/image/{news_id}'
    response = requests.get(collection_url)
    response.raise_for_status()
    fly_lib = response.json()
    url_image = fly_lib['image_files'][0]['file_url']
    return (url_image)


def change_url(url_image, protocol):
    if protocol != 'https:':
        new_url_image = 'https:' + url_image
    else:
        new_url_image = url_image
    return new_url_image


def safe_image (url_image, folder, name_image, number_image):
    protocol_lst = url_image.split('//')
    protocol = protocol_lst[0]
    url_image = change_url(url_image, protocol)
    lst = url_image.split('.')
    image_format = lst[-1]
    filename = f'{folder}/{name_image}-{number_image}.{image_format}'
    response = requests.get(url_image, verify=False)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def download_image(urls_image, folder, name_image):
    if type (urls_image) == str:
        number_image = 0
        safe_image(urls_image, folder, name_image, number_image)
    else:
        for number_image, url_image in enumerate(urls_image):
            safe_image(url_image, folder, name_image, number_image)


def resiz_image(folder_list):
    image_number = 1
    for path in folder_list:
        for dir,folder,files in os.walk(path):
            for image in files:
                lst = image.split('.')
                new_image = Image.open(f'{dir}/{image}')
                new_image = new_image.resize((1080, 1080))
                new_image.save(f'instagram_images/{image_number}-{lst[0]}.jpg',
                               format='JPEG')
                image_number += 1


def check_pic_list():
    posted_pic_list = []
    try:
        with open("pics.txt", "r", encoding="utf8") as f:
            posted_pic_list = f.read().splitlines()
    except Exception:
        posted_pic_list = []
    return posted_pic_list


def check_file_name(description_file, pic_name):
    if os.path.isfile(description_file):
        with open(description_file, "r") as file:
            caption = file.read()
    else:
        caption = pic_name.replace("-", " ")
    return caption


def create_pic_name(pic,  folder_path):
    pic_name = pic[:-4].split("-")
    pic_name = "-".join(pic_name[1:])

    print("upload: " + pic_name)

    description_file = folder_path + "/" + pic_name + ".txt"
    return description_file, pic_name


def publication_photo_instagram (login_instagram, password_instagram):
    posted_pic_list = check_pic_list()

    # timeout = 24 * 60 * 60  # pics will be posted every 24 hours
    timeout = 5

    bot = Bot()
    bot.login(username=login_instagram, password=password_instagram)
    while True:
        folder_path = "./instagram_images"
        pics = glob.glob(folder_path + "/*.jpg")
        pics = sorted(pics)
        try:
            for pic in pics:
                if pic in posted_pic_list:
                    continue

                [description_file, pic_name] = create_pic_name(pic, folder_path)
                caption = check_file_name(description_file, pic_name)

                bot.upload_photo(pic, caption=caption)

                if bot.api.last_response.status_code != 200:
                    print(bot.api.last_response)
                    break

                if pic not in posted_pic_list:
                    posted_pic_list.append(pic)
                    with open("pics.txt", "a", encoding="utf8") as f:
                        f.write(pic + "\n")

                time.sleep(timeout)

        except Exception as e:
            print(str(e))
        time.sleep(60)


if __name__ == '__main__':
    load_dotenv()

    login_instagram = os.getenv('LOGIN_INSTAGRAM')
    password_instagram = os.getenv('PASSWORD_INSTAGRAM')

    spacex_url = 'https://api.spacexdata.com/v4/launches'
    hubble_url = 'https://hubblesite.org/api/v3/images'
    folder_list = ['hubble_images', 'spacex_images']
    image_name_list = ['hubble', 'spacex']

    Path("spacex_images").mkdir(parents=True, exist_ok=True)
    url_images_spacex = fetch_spacex_last_launch(spacex_url)
    download_image(url_images_spacex, folder_list[1], image_name_list[1])


    Path("hubble_images").mkdir(parents=True, exist_ok=True)
    news_id_hubble = fetch_news_id_hubble(hubble_url)
    url_image_hubble = get_url_image_hubble(news_id_hubble)
    download_image(url_image_hubble, folder_list[0], image_name_list[0])

    Path("instagram_images").mkdir(parents=True, exist_ok=True)
    resiz_image(folder_list)

    publication_photo_instagram(login_instagram, password_instagram)