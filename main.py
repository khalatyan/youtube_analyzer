
import requests
import csv

import pandas as pd
import re

from local_file import *

playlist_list = []
data = []


def get_seconds_by_str(string: str):
    my_str = 'PT'
    if ("H" in string):
        my_str += '(\d+)H'
    if ("M" in string):
        my_str += '(\d+)M'
    if ("S" in string):
        my_str += '(\d+)S'

    H = re.findall(my_str,string)[0]

    total_secs = 0
    for i in range(len(H) - 1):
        total_secs += int(H[i]) * 60
    total_secs += int(H[-1])
    return total_secs

def get_playlist_from_chanel():
    API_URL = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet' + '&channelId=UCSaVoRErW4kqKsDqExs2MXA' + '&maxResults=500' + '&key=' + API_KEY
    response = requests.get(API_URL)

    json_response = response.json()
    items = json_response["items"]

    for i in items:
        playlist_id = i["id"]
        playlist_name = i["snippet"]["title"]

        playlist_list.append({"id": playlist_id, "title": playlist_name})



def get_videos_from_playlist(id, name, i):
    API_URL = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet' + '&playlistId=' + id + '&maxResults=500' + '&key=' + API_KEY

    response = requests.get(API_URL)

    json_response = response.json()
    items = json_response["items"]



    for item in items:
        list = get_information_to_video(item["snippet"]["resourceId"]["videoId"])
        if (list):
            list["title"] = item["snippet"]["title"]
            list["publishedAt"] = item["snippet"]["publishedAt"]
            list["playlist_anme"] = playlist_list[i]["title"]

            data.append(list)


def get_information_to_video(id):
    API_URL = 'https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails' + '&id=' + id + '&key=' + API_KEY
    response = requests.get(API_URL)

    json_response = response.json()
    if (json_response["items"]):
        item = json_response["items"][0]
        statistics = item["statistics"]
        duration = get_seconds_by_str(item["contentDetails"]["duration"])

        try:
            list = {
                "viewCount": statistics["viewCount"],
                "likeCount": statistics["likeCount"],
                "dislikeCount": statistics["dislikeCount"],
                "favoriteCount": statistics["favoriteCount"],
                "commentCount": statistics["commentCount"],
                "duration": duration
            }
        except Exception:
            list = {
                "viewCount": 0,
                "likeCount": statistics["likeCount"],
                "dislikeCount": statistics["dislikeCount"],
                "favoriteCount": statistics["favoriteCount"],
                "commentCount": statistics["commentCount"],
                "duration": duration
            }
    else:
        return ({})


    return (list)



get_playlist_from_chanel()


j = 0
for i in playlist_list:
    get_videos_from_playlist(i["id"], i["title"], j)
    j += 1



keys = data[0].keys()
with open('outputfile.csv', 'w', newline='', encoding='utf-8')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(data)
