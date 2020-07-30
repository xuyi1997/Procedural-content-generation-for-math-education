import requests
import json
import shutil
import re


api_key = "wg62dhqm2bfuuxzygvt5r5wz"
api_secret = "AYqEEFoWrNw4haX79WgW"
username = "info@squla.nl"
password = "W3lk0m01"
refreshtokendata = 'sl/LQ6zr9hM51/VCuNttmbx2Exs/tYITcvt5VqWmyxgPrbAUTyycVbiWq42vhQTyM4z0Nrth+/yF0o91oCOK5hgDzgVDpiHJrfzQKk1IkuR7jnCWr72qohoXMIoQ3/uqqiq7qXPcvVRZAwldsz6fhaNesOROuw7XpEvC5QTqI08=|77u/YVZVQjlTZGtXckgyRVRlQUFCU1YKMTAwNzI0CjczMTU4MjkKM2JUV0VRPT0KNWJ2V0VRPT0KMQp3ZzYyZGhxbTJiZnV1eHp5Z3Z0NXI1d3oKODAuMTEyLjE3OC4yMDgKMAoKS1RxNEV3PT0KNDQxCjAKCgo=|3|4|1'


def get_resource_owner_token(key, secret, user, passwd):
    """Get an access token using resource owner grant"""
    url = "https://api.gettyimages.com/oauth2/token"
    payload = f"grant_type=password&client_id={key}&client_secret={secret}&username={user}&password={passwd}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    auth = json.loads(response.content)
    # print(auth)
    return auth

def search_image(phrase, auth):
        """Search for creative images given a search phrase and some filters"""
        url = "https://api.gettyimages.com/v3/search/images"
        query_params = {"phrase": phrase, "collection_codes": ["essentials"],"collections_filter_type": 'exclude'}
        headers = {
            "Api-Key": auth["api_key"]
        }
        response = requests.get(url, params=query_params, headers=headers)
        return response


def get_download_url(id, auth):
    """Get a download image url given an image id and oauth token"""
    url = f"https://api.gettyimages.com/v3/downloads/images/{id}?auto_download=false&product_type=royaltyfreesubscription"
    headers = {
        "Api-Key": auth["api_key"],
        "Authorization": "Bearer " + auth["access_token"]
    }
    response = requests.request("POST", url, headers=headers)
    return response

def download_image(url):
    """Download an image given the url"""

    response = requests.get(url, stream=True)
    content_disposition = response.headers["content-disposition"]
    match = re.search(".*filename=?(\S*)", content_disposition)
    if match:
        filename = match.group(1)
    else:
        filename = "image.jpg"
    filename = "retrieved_image" + "\\" + filename
    with open(filename, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return filename

def get_metadata(id, auth):
    """Get metadata for a single image by supplying one image id"""
    url = f"https://api.gettyimages.com//v3/images/{id}"
    headers = {
        "Api-Key": auth["api_key"],
        "Authorization": "Bearer " + auth["access_token"]
    }
    response = requests.request("POST", url, headers=headers)
    # print(response.content)
    return response

def get_client_credentials_token(key, secret):
    """Get an access token using client credentials grant"""
    url = "https://api.gettyimages.com/oauth2/token"
    payload = f"grant_type=client_credentials&client_id={key}&client_secret={secret}"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    oauth = json.loads(response.content)
    return oauth

def image_retrieve(search_phrase):

    image_id_list = []
    image_dir_list = []
    url_list = []
    auth = get_resource_owner_token(api_key, api_secret, username, password)
    auth["api_key"] = api_key
    search_response = search_image(search_phrase, auth)
    # print(search_response.json())

    for i in range(min(len(search_response.json()["images"]), 4)):
        img = search_response.json()["images"][i]
        rough_img_url = img['display_sizes'][0]['uri']
        img_dir = download_image(rough_img_url)
        image_dir_list.append(img_dir)
        id = img["id"]
        download_response = get_download_url(id, auth)
        image_dir_list.append(download_response.json()["uri"])
    # download_response = get_download_url(image_id, auth)
    print(url_list)
    return image_dir_list
    # from PIL import Image
    # image_eps = filename
    # im = Image.open(image_eps)
    # fig = im.convert('RGBA')
    # image_png= search_phrase  + '.png'
    # fig.save(image_png, lossless = True)

# image_retrieve("brownies cafe")