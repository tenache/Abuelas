
# API_KEY = "da5e05401bcd92452801bca30452cf5234dfb08a4181524c52a6d7d4493dc2f4"
import argparse
import os, requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import socket
from dotenv import load_dotenv

load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument('queries')
parser.add_argument('folder_name', type=str)
args = parser.parse_args()

def serpapi_get_google_images(queries, folder_name='GoogleImgs'):
    print(os.getenv('API_KEY'))
    if type(queries)==str:
        queries = [queries]

    image_results = []

    for query in queries:

        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            #"api_key": API_KEY
            "api_key": os.getenv("API_KEY")   # your serpapi api key
            # other query parameters: hl (lang), gl (country), etc  
        }

        
        
        search = GoogleSearch(params)         # where data extraction happens

        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary

            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if image["original"] not in image_results:
                        image_results.append(image["original"])
                images_is_present = False

                # update to the next page
                params["ijn"] += 1
            else:
                images_is_present = False
                print(results["error"])

    # -----------------------
    # Downloading images
    print('afterGoogleSearch')
    for index, image in enumerate(image_results, start=1):
        print(f"Downloading {index} image...")

        opener=urllib.request.build_opener()
        opener.addheaders=[("User-Agent","Mozilla/5.0")]
        urllib.request.install_opener(opener)
        socket.setdefaulttimeout(15)
        try:
            urllib.request.urlretrieve(image, f"{folder_name}/{queries[0]}_{index}.jpg")
        except Exception as e:
            print('Downloading gave the following error: ')
            print(e)

    print(json.dumps(image_results, indent=2))
    print(len(image_results))
if __name__ == '__main__':
    serpapi_get_google_images(args.queries, args.folder_name)
