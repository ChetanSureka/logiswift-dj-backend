import requests

try:
    url = 'https://chetansureka.pythonanywhere.com/utils/tatupdate/'
    response = requests.get(url)
    if response.status_code != 200:
        print("Can't update...", response.status_code)
    else:
        print(response.content)
except Exception as e:
    print("Could not get response...", e)