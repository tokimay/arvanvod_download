import json
from selenium import webdriver


def get(url):
    jsonLink = []

    # Initialize Chrome WebDriver with performance logging enabled
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the target website
    driver.get(url)

    # Capture network log entries
    log_entries = driver.get_log("performance")

    # Initialize dictionaries to store request and response headers
    request_headers_data = []
    response_headers_data = []
    last_known_url = None  # To keep track of the URL associated with the latest entry

    for entry in log_entries:
        try:
            obj_serialized = entry.get("message")
            obj = json.loads(obj_serialized)
            message = obj.get("message")
            method = message.get("method")
            url = message.get("params", {}).get("documentURL")

            if method == 'Network.requestWillBeSentExtraInfo' or method == 'Network.requestWillBeSent':
                try:
                    request_payload = message['params'].get('request', {})
                    request_headers = request_payload.get('headers', {})
                    # Store request headers and last known URL in request_headers_data
                    request_headers_data.append({"url": url, "headers": request_headers})
                    last_known_url = url
                except KeyError:
                    pass

            if method == 'Network.responseReceivedExtraInfo' or method == 'Network.responseReceived':
                try:
                    response_payload = message['params'].get('response', {})
                    response_headers = response_payload.get('headers', {})
                    # Store response headers and last known URL in response_headers_data
                    response_headers_data.append({"url": url, "headers": response_headers})
                    last_known_url = url
                except KeyError:
                    pass

        except Exception as e:
            raise e from None

    # Iterate through the headers sequentially
    for request_headers, response_headers in zip(request_headers_data, response_headers_data):
        # print("Request URL:", request_headers["url"])
        # print("Request Headers:", request_headers["headers"])
        # print("Response URL:", response_headers["url"])
        # print("Response Headers:", response_headers["headers"])
        # print('--------------------------------------')
        if str(request_headers["url"]).find("player.arvancloud.ir") == -1:
            pass
        else:
            jsonLink.append(request_headers["url"])

    # Close the WebDriver
    driver.quit()
    # print(jsonLink)
    return jsonLink