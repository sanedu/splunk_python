import requests
s = requests.Session()

def getToken():
    global s
    url = "https://splunkitops.conductor.com.br/en-US/account/login"
    r = s.get(url, verify=False)
    pay = {
        "username": "username",
        "password": "password",
        "cval": r.cookies.get("cval"),
    }
    r = s.post(url, data=pay, verify=False)
    print(r.status_code)
    c = r.cookies.get_dict()
    cookie = ""
    for k in c:
        cookie += k
        cookie += "="
        cookie += c[k]
        cookie += ";"

    return r.cookies.get("splunkweb_csrf_token_443"), cookie

URL = "https://splunkitops.conductor.com.br/en-US/splunkd/__raw/servicesNS/eduardo.santos/conductor/search/jobs"

PAYLOAD = {
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
    # "custom.dispatch.earliest_time": "-24h@h",
    # "custom.dispatch.latest_time": "now",
    # "custom.dispatch.sample_ratio": "1",
    # "custom.display.page.search.mode": "smart",
}

cval, cookie = getToken()

HEADERS = {
    "Cookie": cookie,
    "X-Splunk-Form-Key": cval,
    "X-Requested-With": "XMLHttpRequest"
}

print(HEADERS)

r = s.post(URL, headers=HEADERS, data=PAYLOAD, verify=False)
print(r.status_code)
print(r.text)


