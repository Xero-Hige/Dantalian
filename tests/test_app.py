import requests
import unittest
import hashlib
from uuid import uuid4

unittest.defaultTestLoader.sortTestMethodsUsing = None

BASE_URI = lambda x: "http://localhost:8000/api/0.1/" + x


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app_name = str(uuid4())
        origin = cls.app_name
        res = requests.post(BASE_URI("users"), json={'username': origin})
        cls.api_key = res.json()['api_key']

    def test_create_user(self):
        self.assertTrue(self.__class__.api_key is not None)

    def test_get_video(self):
        with open('../src/bach/data/videos/853789.mp4', 'rb') as f:
            video_checksum = hashlib.md5(f.read()).hexdigest()
        res = requests.get(BASE_URI("video/1"),
                            headers={'api_key': self.__class__.api_key,
                                  'origin': self.__class__.app_name})
        res_checksum = hashlib.md5(res.content).hexdigest()
        self.assertEqual(video_checksum, res_checksum)

    def test_get_gif(self):
        with open('../src/bach/data/gifs/853789_1.gif', 'rb') as f:
            gif_checksum = hashlib.md5(f.read()).hexdigest()
        res = requests.get(BASE_URI("gif/1"),
                            headers={'api_key': self.__class__.api_key,
                                  'origin': self.__class__.app_name})
        res_checksum = hashlib.md5(res.content).hexdigest()
        self.assertEqual(gif_checksum, res_checksum)


if __name__ == '__main__':
    unittest.main()
