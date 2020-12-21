import requests
from time import time
import json
import urllib.parse

class Splunk:
    __session = requests.Session()
    __cvalCookie = None

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    def login(self):
        url = "https://splunkitops.conductor.com.br/en-US/account/login"
        r = self.__session.get(url, verify=False)
        pay = {
            "username": self.__username,
            "password": self.__password,
            "cval": r.cookies.get("cval"),
        }
        r = self.__session.post(url, data=pay, verify=False)
        print(r.status_code)
        if r.status_code == 200:
            self.__cvalCookie = r.cookies.get("splunkweb_csrf_token_443")

    def search(self):
        payload = {
            "adhoc_search_level": "smart",
            "auto_cancel": "30",
            "check_risky_command": "false",
            "custom.search": 'index="heimdall" trace.resultStatus=200',
            "earliest_time": "-24h@h",
            "indexedRealtime": "",
            "latest_time": "now",
            "output_mode": "json",
            "preview": "1",
            "provenance": "UI:Search",
            "rf": "*",
            "sample_ratio": "1",
            "search": 'search index="heimdall" trace.resultStatus=200',
            "status_buckets": "300",
            "ui_dispatch_app": "conductor",
        }

        h = {
            "X-Splunk-Form-Key": self.__session.cookies.get("splunkweb_csrf_token_443"),
            "X-Requested-With": "XMLHttpRequest"
        }
        url = "https://splunkitops.conductor.com.br/en-US/splunkd/__raw/servicesNS/%s/conductor/search/jobs" %self.__username
        r = self.__session.post(url, headers=h, data=payload)
        print(r.status_code)
        if r.status_code == 201:
            sid = r.json()["sid"]
            print(sid)
            self.getResults(sid)

    def getResults(self, sid):
        url = "https://splunkitops.conductor.com.br/en-US/splunkd/__raw/servicesNS/%s/conductor/search/jobs/%s/events?" %(self.__username, sid)
        tm = str(time()).replace(".", "")[:13]
        query = {
            "output_mode": "json",
            "offset": "0",
            "count": "20",
            "segmentation": "full",
            "max_lines": "5",
            "field_list": "host,source,sourcetype,_raw,_time,_audit,_decoration,eventtype,_eventtype_color,linecount,_fulllinecount,_icon,tag*",
            "truncation_mode": "abstract",
            "_": "1608514972334"
        }

        url += urllib.parse.urlencode(query)
        # url = f"https://splunkitops.conductor.com.br/en-GB/api/search/jobs/{sid}/event?isDownload=true&timeFormat=%25FT%25T.%25Q%25%3Az&maxLines=0&count=20&offset=0&filename=&outputMode=csv"
        # url2 = f"https://splunkitops.conductor.com.br/en-GB/api/search/jobs/{sid}/event?isDownload=true&timeFormat=%25FT%25T.%25Q%25%3Az&maxLines=0&count=20&offset=20&filename=&outputMode=csv"
        r = self.__session.get(url, verify=False, headers={"X-Requested-With": "XMLHttpRequest"})
        # r = self.__session.get(url, verify=False)
        # r2 = self.__session.get(url2, verify=False)
        print(r.url)
        print(r.status_code)
        print(r.content)
        if r.status_code == 200:
            print(r.headers)
            
            with open("results.csv", "wb") as f:
                f.write(r.content)
            # with open("results2.csv", "wb") as f:
            #     f.write(r2.content)
        else:
            print(r.text)

if __name__ == "__main__":
    splunk = Splunk(
        username="username",
        password="password",
    )
    splunk.login()
    splunk.search()