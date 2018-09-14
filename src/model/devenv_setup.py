from model import *

tagtext1 = TagText.create("personas")
print("tagtext1 id is {}".format(tagtext1))
tagtext2 = TagText.create("perros")
print("tagtext2 id is {}".format(tagtext2))

video1_id = Video.create('https://videos.pexels.com/videos/blurry-video-of-people-working-853789', 'people', '/images/videos/853789.mp4')
print("video id is {}".format(video1_id))

gif1 = Gif.create(video1_id, 1, '/images/gifs/853789_1.gif')
gif2 = Gif.create(video1_id, 2, '/images/gifs/853789_2.gif')
gif3 = Gif.create(video1_id, 3, '/images/gifs/853789_3.gif')
gif4 = Gif.create(video1_id, 4, '/images/gifs/853789_4.gif')

token1 = Users.create("app1")

Tag.create(tagtext1, gif1, token1, True)
Tag.create(tagtext2, gif1, token1, False)
