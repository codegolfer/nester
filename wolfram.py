"""
wolframalpha apis
"""

import requests


def _url(path):
    return 'http://api.wolframalpha.com/v1' + path


def execute_spoken_query(appid='', query=''):
    """
    execute_spoken_query
    """
    payload = {}
    if appid:
        payload['appid'] = appid
    if query:
        payload['i'] = query
    # print (payload)
    resp = requests.get(_url('/spoken'), params=payload)
    return resp.text
