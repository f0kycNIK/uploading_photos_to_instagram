import os
import glob
import sys
import time
import requests
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

load_dotenv()

login_instagram = os.getenv('LOGIN_INSTAGRAM')
password_instagram = os.getenv('PASSWORD_INSTAGRAM')

def download_spacex_imges(images):
    for number_image, image in enumerate(images):
        filename = f'spacex_images/spacex{number_image}.jpg'
        response = requests.get(image)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)


def fetch_spacex_last_launch(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    fly_lib = response.json()
    url_images = fly_lib[13]['links']['flickr']['original']
    return url_images


def fetch_photo_hubble(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    fly_lib = response.json()
    image_id = fly_lib[0]['id']
    return image_id


def creating_hubbl_list_url_image(image_id):
    payload = {}
    headers = {}
    collection_url = f' http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.request("GET", collection_url, headers=headers, data=payload)
    response.raise_for_status()
    fly_lib2 = response.json()
    images = fly_lib2['image_files']
    lst = []
    for image in images:
        lst.append(image['file_url'])
    return (lst)


def save_picture_any_format(list_images_url, image_id):
    payload = {}
    headers = {}
    for image_url in list_images_url:
        lst = image_url.split('.')
        image_format = lst[-1]
        filename = f'hubble_images/{image_id}.{image_format}'
        modify_image_url = 'https:' + image_url
        response = requests.get(modify_image_url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)

def resiz_picture(folder_list):
    number_image = 1
    for path in folder_list:
        for dir,folder,files in os.walk(path):
            for image in files:
                lst = image.split('.')
                image_format = lst[-1]
                if image_format == 'jpg':
                    new_image = Image.open(f'{dir}/{image}')
                    new_image = new_image.resize((1080, 1080))
                    new_image.save(f'instagram_images/{number_image}-{lst[0]}-resize.jpg', format='JPEG')
                    number_image += 1


def publication_photo_instagram (login_instagram, password_instagram):
    try:
        with open("pics.txt", "r", encoding="utf8") as f:
            posted_pic_list = f.read().splitlines()
    except Exception:
        posted_pic_list = []

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

                pic_name = pic[:-4].split("-")
                pic_name = "-".join(pic_name[1:])

                print("upload: " + pic_name)

                description_file = folder_path + "/" + pic_name + ".txt"

                if os.path.isfile(description_file):
                    with open(description_file, "r") as file:
                        caption = file.read()
                else:
                    caption = pic_name.replace("-", " ")

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
    spacex_url = 'https://api.spacexdata.com/v4/launches'
    # spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    Path("spacex_images").mkdir(parents=True, exist_ok=True)
    url_images = fetch_spacex_last_launch(spacex_url)
    download_spacex_imges(url_images)

    hubble_url = 'https://hubblesite.org/api/v3/images/?page=all&collection_name=spacecraft'
    Path("hubble_images").mkdir(parents=True, exist_ok=True)
    hubble_image_id = fetch_photo_hubble(hubble_url)

    lst = creating_hubbl_list_url_image(hubble_image_id)
    save_picture_any_format(lst, hubble_image_id)

    Path("instagram_images").mkdir(parents=True, exist_ok=True)
    folder_list = ['hubble_images', 'spacex_images']
    resiz_picture(folder_list)
    publication_photo_instagram(login_instagram, password_instagram)