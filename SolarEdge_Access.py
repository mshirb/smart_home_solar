import requests
import json

api_key = '4VJK000831ZQJKMAWLGOF5ML6X6TL9I5'
site_id = '635862'
url_head = 'https://monitoringapi.solaredge.com/'


def url_builder(location, param):
    url = url_head + location + '.json?api_key=' + api_key
    for para in param:
        url += '&' + para
    return url


newurl = url_builder('overview', [])
print(newurl)