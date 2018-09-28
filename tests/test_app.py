import requests
import unittest
import hashlib


unittest.defaultTestLoader.sortTestMethodsUsing = None

BASE_URI = "http://localhost:8000/api/0.1/"
APP_NAME = "test_app1"
API_KEY = None 

class TestApp(unittest.TestCase):
    def test_create_user(self):
        origin = APP_NAME
        res = requests.post(BASE_URI + "users", json={'username': origin})
        self.assertTrue(res.ok)
        print(res.json())
        API_KEY = res.json()

    def test_get_video(self):
        with open('../src/bach/data/videos/853789.mp4', 'rb') as f:
            video_checksum = hashlib.md5(f.read()).hexdigest()
        res = requests.post(BASE_URI + "users", json={'api_key': API_KEY, 'origin': APP_NAME})
        res_checksum = hashlib.md5(res.content).hexdigest()
        self.assertEqual(video_checksum, res_checksum)


if __name__ == '__main__':
    unittest.main()
