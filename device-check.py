# import http.client
import http.client, ssl, certifi

context = ssl.create_default_context(cafile=certifi.where())


#+36719991000
def get_device_status(mobile_number):
    conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com",context = context)

    payload = f'{{"subscriptionDetail":{{"device":{{"phoneNumber":"{mobile_number}"}},"type":"org.camaraproject.device-status.v0.roaming-status"}},"subscriptionExpireTime":"2026-01-17T13:18:23.682Z","webhook":{{"notificationUrl":"https://application-server.com","notificationAuthToken":"c8974e592c2fa383d4a3960714"}}}}'

    headers = {
        'x-rapidapi-key': "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/device-status/v0/subscriptions", payload, headers)

    res = conn.getresponse()
    if res.status != 201:
        print("Error occurred:")
        return 0
    elif  res.status == 201:
        print("Subscription created successfully")
        return 1



# print(res.status, res.reason)
# data = res.read()
# print(data.decode("utf-8"))




# import http.client
# import ssl
# import certifi
# import json


# def get_device_status(mobile_number):
#     """
#     Creates a device status subscription via the Network as Code API (RapidAPI).
#     Uses a certifi-based SSL context for reliable certificate verification.
#     """

#     # ✅ Create SSL context using certifi’s trusted CA bundle
#     ssl_context = ssl.create_default_context(cafile=certifi.where())

#     # ✅ Use secure context in HTTPS connection
#     conn = http.client.HTTPSConnection(
#         "network-as-code.p-eu.rapidapi.com",
#         context=ssl_context
#     )

#     # ✅ Build JSON payload safely using Python dict
#     payload_data = {
#         "subscriptionDetail": {
#             "device": {"phoneNumber": mobile_number},
#             "type": "org.camaraproject.device-status.v0.roaming-status"
#         },
#         "subscriptionExpireTime": "2026-01-17T13:18:23.682Z",
#         "webhook": {
#             "notificationUrl": "https://application-server.com",
#             "notificationAuthToken": "c8974e592c2fa383d4a3960714"
#         }
#     }

#     # Convert dict to JSON and encode to bytes
#     payload = json.dumps(payload_data).encode("utf-8")

#     headers = {
#         "x-rapidapi-key": "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
#         "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
#         "Content-Type": "application/json"
#     }

#     try:
#         # ✅ Send POST request with secure SSL context
#         conn.request("POST", "/device-status/v0/subscriptions", payload, headers)
#         res = conn.getresponse()

#         if res.status != 201:
#             print(f"[ERROR] Device status subscription failed: HTTP {res.status} {res.reason}")
#             return 0
#         else:
#             print("[INFO] Subscription created successfully")
#             return 1

#     except Exception as e:
#         print(f"[ERROR] Connection failed: {e}")
#         return 0
