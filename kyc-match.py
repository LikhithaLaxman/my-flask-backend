import http.client, ssl, certifi

context = ssl.create_default_context(cafile=certifi.where())
import json

def kyc_match_check(mobile_number):
    

    conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com",context=context)

    payload_data = {
        "phoneNumber": mobile_number,
        "idDocument": "66666666q",
        "name": "Federica Sanchez Arjona",
        "givenName": "Federica",
        "familyName": "Sanchez Arjona",
        "nameKanaHankaku": "federica",
        "nameKanaZenkaku": "Ｆｅｄｅｒｉｃａ",
        "middleNames": "Sanchez",
        "familyNameAtBirth": "YYYY",
        "address": "Tokyo-to Chiyoda-ku Iidabashi 3-10-10",
        "streetName": "Nicolas Salmeron",
        "streetNumber": "4",
        "postalCode": "1028460",
        "region": "Tokyo",
        "locality": "ZZZZ",
        "country": "JP",
        "houseNumberExtension": "VVVV",
        "birthdate": "1978-08-22",
        "email": "abc@example.com",
        "gender": "OTHER"
    }

    payload = json.dumps(payload_data).encode('utf-8')

    headers = {
        'x-rapidapi-key': "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json",
        'x-correlator': "b4333c46-49c0-4f62-80d7-f0ef930f1c46"
    }

    conn.request("POST", "/passthrough/camara/v1/kyc-match/kyc-match/v0.3/match", payload, headers)

    res = conn.getresponse()
    # data = res.read()
    # print(data.decode("utf-8"))
    #print(res.status, res.reason)
    if res.status != 200:
        print("Error occurred:")
        return 0
    elif  res.status == 200:
        print("Sim swappped status retrieved successfully")
        return 1


# import http.client
# import json
# import ssl
# import certifi

# def kyc_match_check(mobile_number):
#     """
#     Performs KYC match verification via RapidAPI (Network as Code API).
#     Uses certifi-based SSL context for cross-platform compatibility.
#     """

#     # ✅ Create SSL context using certifi (trusted CA bundle)
#     ssl_context = ssl.create_default_context(cafile=certifi.where())

#     # ✅ Use that SSL context for HTTPS connection
#     conn = http.client.HTTPSConnection(
#         "network-as-code.p-eu.rapidapi.com",
#         context=ssl_context
#     )

#     # Request payload
#     payload_data = {
#         "phoneNumber": mobile_number,
#         "idDocument": "66666666q",
#         "name": "Federica Sanchez Arjona",
#         "givenName": "Federica",
#         "familyName": "Sanchez Arjona",
#         "nameKanaHankaku": "federica",
#         "nameKanaZenkaku": "Ｆｅｄｅｒｉｃａ",
#         "middleNames": "Sanchez",
#         "familyNameAtBirth": "YYYY",
#         "address": "Tokyo-to Chiyoda-ku Iidabashi 3-10-10",
#         "streetName": "Nicolas Salmeron",
#         "streetNumber": "4",
#         "postalCode": "1028460",
#         "region": "Tokyo",
#         "locality": "ZZZZ",
#         "country": "JP",
#         "houseNumberExtension": "VVVV",
#         "birthdate": "1978-08-22",
#         "email": "abc@example.com",
#         "gender": "OTHER"
#     }

#     payload = json.dumps(payload_data).encode('utf-8')

#     headers = {
#         'x-rapidapi-key': "a2aea3ab6dmsh3da63ce0400adcdp1a45cajsn4d1a823c6475",
#         'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
#         'Content-Type': "application/json",
#         'x-correlator': "b4333c46-49c0-4f62-80d7-f0ef930f1c46"
#     }

#     # ✅ Make the HTTPS request using the secure context
#     conn.request(
#         "POST",
#         "/passthrough/camara/v1/kyc-match/kyc-match/v0.3/match",
#         payload,
#         headers
#     )

#     res = conn.getresponse()

#     if res.status != 200:
#         print(f"[ERROR] KYC check failed: HTTP {res.status} {res.reason}")
#         return 0
#     else:
#         print("[INFO] KYC Match retrieved successfully")
#         return 1
