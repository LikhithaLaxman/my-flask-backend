
import http.client, ssl, certifi

context = ssl.create_default_context(cafile=certifi.where())


def device_swapped_check(mobile_number):
    conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com",context=context)

    payload = "{\"phoneNumber\":\""+mobile_number+"\",\"maxAge\":120}"

    headers = {
        'x-rapidapi-key': "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/passthrough/camara/v1/device-swap/device-swap/v1/check", payload, headers)

    res = conn.getresponse()
    data = res.read()
    if res.status != 200:
        print("Error occurred:")
        return 0
    elif  res.status == 200:
        print("Sim swappped status retrieved successfully")
        return 1

# import http.client
# import ssl
# import certifi
# import json


# def device_swapped_check(mobile_number):
#     """
#     Checks whether a device was recently swapped using the Network as Code API.
#     Uses certifi-based SSL context for consistent and secure certificate verification.
#     """

#     # ✅ Create a secure SSL context with certifi’s trusted CA bundle
#     ssl_context = ssl.create_default_context(cafile=certifi.where())

#     # ✅ Use the SSL context for HTTPS connection
#     conn = http.client.HTTPSConnection(
#         "network-as-code.p-eu.rapidapi.com",
#         context=ssl_context
#     )

#     # ✅ Build JSON payload safely using Python dict
#     payload_data = {
#         "phoneNumber": mobile_number,
#         "maxAge": 120
#     }

#     # Convert dict to JSON string and encode to bytes
#     payload = json.dumps(payload_data).encode('utf-8')

#     headers = {
#         "x-rapidapi-key": "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
#         "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
#         "Content-Type": "application/json"
#     }

#     try:
#         # ✅ Make the POST request securely
#         conn.request("POST", "/passthrough/camara/v1/device-swap/device-swap/v1/check", payload, headers)
#         res = conn.getresponse()
#         data = res.read()

#         if res.status != 200:
#             print(f"[ERROR] Device swap check failed: HTTP {res.status} {res.reason}")
#             return 0
#         else:
#             print("[INFO] Device swap status retrieved successfully")
#             return 1

#     except Exception as e:
#         print(f"[ERROR] Device swap check failed: {e}")
#         return 0
