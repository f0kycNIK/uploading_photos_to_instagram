import requests
from pathlib import Path
from pprint import pprint

def download_imges (images):
    #firs_part_name = 'spacex'
    for image_number, image in enumerate(images):
        #image_name = 'spacex'+image_number
        #print(image_name)
        filename = f'images/spacex{image_number}.jpeg'
        response = requests.get(image)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        #print(book_number, book)

def fetch_spacex_last_launch(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    fly_lib = response.json()
    url_images = fly_lib[13]['links']['flickr']['original']
    return url_images

def fetch_photo_hubble (url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    fly_lib = response.json()
    image_id =  fly_lib[0]['id']
    return image_id


def creating_list_url_image (image_id):
    payload = {}
    headers = {}
    collection_url = f' http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.request("GET", collection_url, headers=headers, data=payload)
    response.raise_for_status()
    pprint(response.json())
    fly_lib2 = response.json()
    images = fly_lib2['image_files']
    lst = []
    for image in images:
        lst.append(image['file_url'])
    print(lst)
    return(lst)

def save_picture_any_format (list_images_url, image_id):
    payload = {}
    headers = {}
    for image_url in list_images_url:
        lst = image_url.split('.')
        image_format = lst[-1]
        filename = f'hubble_images/{image_id}.{image_format}'
        response = requests.get('https:' + image_url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)

if __name__ == '__main__':
    Path("images").mkdir(parents=True, exist_ok=True)
    #spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    spacex_url = 'https://api.spacexdata.com/v4/launches'
    hubble_url = 'https://hubblesite.org/api/v3/images/news'
    url_images = fetch_spacex_last_launch(spacex_url)
    download_imges(url_images)
    image_id = fetch_photo_hubble(hubble_url)
    Path("hubble_images").mkdir(parents=True, exist_ok=True)
    lst = creating_list_url_image(image_id)
    save_picture_any_format(lst, image_id)





