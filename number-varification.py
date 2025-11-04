import http.client, ssl, certifi

context = ssl.create_default_context(cafile=certifi.where())

def number_verification_check(mobile_number):
    conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com",context=context)

    payload = "{\"phoneNumber\":\""+mobile_number+"\"}"

    headers = {
        'x-rapidapi-key': "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/passthrough/camara/v1/number-verification/number-verification/v0/verify", payload, headers)

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


# def number_verification_check(mobile_number):
#     """
#     Verifies a mobile number using the Network as Code API via RapidAPI.
#     Uses certifi-based SSL context to ensure cross-platform SSL reliability.
#     """

#     # ✅ Create SSL context using certifi’s trusted CA bundle
#     ssl_context = ssl.create_default_context(cafile=certifi.where())

#     # ✅ Use the SSL context for the HTTPS connection
#     conn = http.client.HTTPSConnection(
#         "network-as-code.p-eu.rapidapi.com",
#         context=ssl_context
#     )

#     # ✅ Build safe JSON payload
#     payload_data = {
#         "phoneNumber": mobile_number
#     }

#     # Convert dict to JSON string and encode to bytes
#     payload = json.dumps(payload_data).encode("utf-8")

#     headers = {
#         "x-rapidapi-key": "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
#         "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
#         "Content-Type": "application/json"
#     }

#     try:
#         # ✅ Make secure POST request
#         conn.request("POST", "/passthrough/camara/v1/number-verification/number-verification/v0/verify", payload, headers)
#         res = conn.getresponse()
#         data = res.read()

#         if res.status != 200:
#             print(f"[ERROR] Number verification failed: HTTP {res.status} {res.reason}")
#             return 0
#         else:
#             print("[INFO] Number verification succeeded")
#             return 1

#     except Exception as e:
#         print(f"[ERROR] Number verification check failed: {e}")
#         return 0
