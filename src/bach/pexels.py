from bs4 import BeautifulSoup
import requests
import os
from moviepy.editor import *
import argparse
import time

import sys
sys.path.insert(0, "../")
from model.model import *    # Replace "my_module" here with your module's name.
sys.path.pop(0)


GIF_DURATION = 4.0

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def download_video(url, category):
    print("downloading video @ " + url)
    page = requests.get(url, headers=HEADERS)

    wait_time = 2
    if page.status_code == 422:
        time.sleep(wait_time)
        wait_time *= 2
        page = requests.get(url, headers=HEADERS)

    tree = BeautifulSoup(page.content, 'html.parser')
    video = tree.find(lambda x: x.name == 'a' and x.has_attr('data-id'))
    filename = "data/videos/{}.mp4".format(video.get('data-id'))
    if not Video.exists(url):
        with open(filename, "wb") as f:
            vid = requests.get(video.get('href'), headers=HEADERS)
            f.write(vid.content)
        video_id = Video.create(url, category, filename)
        base_gif = "data/gifs/{}_".format(video.get('data-id'))
        clip = VideoFileClip(filename)
        start = 0.0
        i = 1
        while start < clip.duration:
            end = min(start + GIF_DURATION, clip.duration)
            subclip = clip.subclip(start, end).resize(height=100)
            gif_filename = base_gif + str(i) + ".gif"
            subclip.write_gif(gif_filename)
            Gif.create(video_id, i, gif_filename)
            i += 1
            start += GIF_DURATION


def compose_video_url(sub, page):
    if page != 1:
        sub = sub.split('"')[1][:-1]
    return "https://videos.pexels.com" + sub


def compose_path(category, page):
    path = "https://videos.pexels.com/search/{}".format(category)
    if page != 1:
        path += "?page={}&format=js".format(page)
    return path


def get_atags(tree, page):
    if page != 1:
        return tree.find_all('a')
    return tree.find_all(lambda x: x.name == 'a' and x.has_attr('data-duration'))


def download_list(category, page):
    path = compose_path(category, page)
    print("Page {} --- Downloading: ".format(page) + path)
    p = requests.get(path, headers=HEADERS)

    wait_time = 2
    if page.status_code == 422:
        time.sleep(wait_time)
        wait_time *= 2
        page = requests.get(url, headers=HEADERS)

    html = p.content.decode("UTF8")
    if page != 1:
        html = html.split("'")[5]
    tree = BeautifulSoup(html, 'html.parser')
    atags = get_atags(tree, page)
    for tag in atags:
        download_video(compose_video_url(tag.get('href'), page), category)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--category', '-c', type=str)
    parser.add_argument('--pages', '-p', type=int, default=1)

    args = parser.parse_args()
    for i in range(1, args.pages+1):
        download_list(args.category, i)
