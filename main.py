
import requests
import csv

import pandas as pd

from local_file import *

playlist_list = []
data = []


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
        list["title"] = item["snippet"]["title"]
        list["publishedAt"] = item["snippet"]["publishedAt"]
        list["playlist_anme"] = playlist_list[i]["title"]

        data.append(list)


def get_information_to_video(id):
    API_URL = 'https://www.googleapis.com/youtube/v3/videos?part=statistics' + '&id=' + id + '&key=' + API_KEY
    response = requests.get(API_URL)

    json_response = response.json()
    if (json_response["items"]):
        item = json_response["items"][0]
        statistics = item["statistics"]

        try:
            list = {
                "viewCount": statistics["viewCount"],
                "likeCount": statistics["likeCount"],
                "dislikeCount": statistics["dislikeCount"],
                "favoriteCount": statistics["favoriteCount"],
                "commentCount": statistics["commentCount"]
            }
        except Exception:
            list = {
                "viewCount": 0,
                "likeCount": statistics["likeCount"],
                "dislikeCount": statistics["dislikeCount"],
                "favoriteCount": statistics["favoriteCount"],
                "commentCount": statistics["commentCount"]
            }
    else:
        return ({})


    return (list)



get_playlist_from_chanel()


j = 0
for i in playlist_list:
    get_videos_from_playlist(i["id"], i["title"], j)
    j += 1


data_file = open('outputfile.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(data_file)

count = 0

for emp in data:
    if count == 0:
        # Writing headers of CSV file
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(emp.values())


data_file.close()
