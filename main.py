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
    # pprint(response.text.encode('utf8'))
    fly_lib = response.json()
    url_images = fly_lib[13]['links']['flickr']['original']
    #pprint(url_images)
    return url_images

def fetch_photo_hubble (url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    pprint(response.json())
    # pprint(response.text.encode('utf8'))
    fly_lib = response.json()
    name =  fly_lib[0]['id']
    print (name)
    collection_url = f'https://hubblesite.org/api/v3/image/{name}'
    print(collection_url)
    response = requests.request("GET", collection_url, headers=headers, data=payload)
    response.raise_for_status()
    image_url1 = fly_lib[0]['file_url']
    image_url2 = fly_lib[1]['file_url']
    pprint(response.json())
    # fly_lib = response.json()
    # url_images = fly_lib[0]['name']
    print(image_url1, image_url2)

if __name__ == '__main__':
    Path("images").mkdir(parents=True, exist_ok=True)
    #spacex_url = 'https://api.spacexdata.com/v4/launches/latest'
    spacex_url = 'https://api.spacexdata.com/v4/launches'
    hubble_url = 'https://hubblesite.org/api/v3/images/news'
    url_images = fetch_spacex_last_launch(spacex_url)
    download_imges(url_images)
    fetch_photo_hubble(hubble_url)





