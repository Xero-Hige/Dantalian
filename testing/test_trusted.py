import requests
from constants import BASE_HEADER, BASE_URL
from printing_functions import print_code_test, print_success


def no_json(test_name):
    url = BASE_URL + "users/trust"
    header = BASE_HEADER.copy()

    req = requests.post(url, headers=header)

    print_code_test(test_name, req.status_code, 400)
    print_success(test_name)


if __name__ == '__main__':
    no_json("No Json")
