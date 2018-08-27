from bs4 import BeautifulSoup
import requests
import os
from moviepy.editor import *

GIF_DURATION = 4.0

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def download_video(url):
    print("downloading video @ "+url)
    page = requests.get(url, headers=HEADERS)
    tree = BeautifulSoup(page.content, 'html.parser')
    video = tree.find(lambda x: x.name == 'a' and x.has_attr('data-id'))
    filename = "data/videos/{}.mp4".format(video.get('data-id'))
    if not os.path.exists(filename):
        with open(filename, "wb") as f:
            vid = requests.get(video.get('href'), headers=HEADERS)
            f.write(vid.content)
        base_gif = "data/gifs/{}_".format(video.get('data-id'))
        clip = VideoFileClip(filename)
        start = 0.0
        i = 1
        while start < clip.duration:
            end = min(start + GIF_DURATION, clip.duration)
            subclip = clip.subclip(start, end).resize(height=100)
            subclip.write_gif(base_gif + str(i) + ".gif")
            i += 1
            start += GIF_DURATION


def compose_video_url(sub):
    return "https://videos.pexels.com" + sub


def download_list_(category, page):
    path = "https://videos.pexels.com/search/{}?page={}&format=js".format(category, page)
    print("Downloading: "+path)
    p = requests.get(path, headers=HEADERS)
    if p.status_code != 200:
        raise Exception("Error code {}".format(p.status_code))
    html = p.content.decode("UTF8").split("'")[5]
    tree = BeautifulSoup(html, 'html.parser')
    atags = tree.find_all('a')
    for tag in atags:
        download_video(compose_video_url(tag.get('href').split('"')[1][:-1]))
        with open("tags.csv", "a") as f:
            f.write("{},{}\n".format(category, tag.get('href').split("-")[-1]))
    

def download_list(category, page):
    if page != 1:
        download_list_(category, page)
    path = "https://videos.pexels.com/search/{}".format(category)
    print("Downloading: "+path)
    p = requests.get(path, headers=HEADERS)
    if p.status_code != 200:
        raise Exception("Error code {}".format(p.status_code))
    html = p.content.decode("UTF8")
    tree = BeautifulSoup(html, 'html.parser')
    atags = tree.find_all(lambda x: x.name == 'a' and x.has_attr('data-duration'))
    for tag in atags:
        download_video(compose_video_url(tag.get('href')))
        with open("tags.csv", "a") as f:
            f.write("{},{}\n".format(category, tag.get('href').split("-")[-1]))
    


if __name__ == "__main__":
    #download_list("people", 1)
    download_list("people", 2)
    download_list("cat", 1)
    download_list("cat", 2)
    download_list("dog", 1)
    download_list("dog", 2)
