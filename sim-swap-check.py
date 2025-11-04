import http.client, ssl, certifi

context = ssl.create_default_context(cafile=certifi.where())

def sim_swap_check(mobile_number):
    conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com",context=context)

    payload = "{\"phoneNumber\":\""+mobile_number+"\",\"maxAge\":240}"

    headers = {
        'x-rapidapi-key': "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/passthrough/camara/v1/sim-swap/sim-swap/v0/check", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    print(res.status, res.reason)
    
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


# def sim_swap_check(mobile_number):
#     """
#     Performs a SIM swap check via the Network as Code API (RapidAPI).
#     Uses certifi-based SSL context for proper HTTPS verification across systems.
#     """

#     # ✅ Create SSL context using certifi (trusted CA bundle)
#     ssl_context = ssl.create_default_context(cafile=certifi.where())

#     # ✅ Use this SSL context in the HTTPS connection
#     conn = http.client.HTTPSConnection(
#         "network-as-code.p-eu.rapidapi.com",
#         context=ssl_context
#     )

#     # ✅ Build JSON payload safely
#     payload_data = {
#         "phoneNumber": mobile_number,
#         "maxAge": 240
#     }

#     # Convert to JSON string and encode to bytes
#     payload = json.dumps(payload_data).encode("utf-8")

#     headers = {
#         "x-rapidapi-key": "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
#         "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
#         "Content-Type": "application/json"
#     }

#     try:
#         # ✅ Send POST request securely
#         conn.request("POST", "/passthrough/camara/v1/sim-swap/sim-swap/v0/check", payload, headers)
#         res = conn.getresponse()
#         data = res.read()

#         print(data.decode("utf-8"))  # optional: inspect API response
#         print(res.status, res.reason)

#         if res.status != 200:
#             print(f"[ERROR] SIM swap check failed: HTTP {res.status} {res.reason}")
#             return 0
#         else:
#             print("[INFO] SIM swap status retrieved successfully")
#             return 1

#     except Exception as e:
#         print(f"[ERROR] SIM swap check failed: {e}")
#         return 0
