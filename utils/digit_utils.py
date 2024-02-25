import requests
import json

def get_auth_token(data):
    url = 'https://staging.digit.org/user/oauth/token'
    headers = {
        'Authorization': 'Basic ZWdvdi11c2VyLWNsaWVudDo=',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data.update({
        'grant_type': 'password',
        'scope': 'read',
        'tenantId': 'pg',
        'userType': 'citizen'
    })
    response = requests.post(url, headers=headers, data=data, verify=False)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response
        return response.json()['access_token']
    else:
        return None
    
def validate_locality(data):
    complaint_data = {
        "RequestInfo": {
            "apiId": "Rainmaker",
            "authToken": data.get("auth_token", ""),
            "userInfo": {
                "id": 2079,
                "uuid": "7e2b023a-2f7f-444c-a48e-78d75911387a",
                "userName": "7878787878",
                "name": data.get("name", ""),
                "mobileNumber": data.get("mobile_number", ""),
                "emailId": "",
                "locale": None,
                "type": "CITIZEN",
                "roles": [
                    {
                        "name": "Citizen",
                        "code": "CITIZEN",
                        "tenantId": "pg"
                    }
                ],
                "active": True,
                "tenantId": "pg",
                "permanentCity": "pg.citya"
            },
            "msgId": "1706156400076|en_IN",
            "plainAccessRequest": {}
        }
    }

    city_code = "pg.cityb"
    headers = {'Content-Type': 'application/json'}
    url = f"https://staging.digit.org/egov-location/location/v11/boundarys/_search?hierarchyTypeCode=ADMIN&boundaryType=Locality&tenantId={city_code}"

    response = requests.post(url, headers=headers, data=json.dumps(complaint_data), verify=False)

    if response.status_code == 200:
        response_data = response.json()
        localities = {}
        for locality in response_data["TenantBoundary"][0]["boundary"]:
            localities[locality["name"].lower()] = locality["code"]
        source_locality = data.get("locality", "").lower()
        locality_code = localities.get(source_locality, None)
        return locality_code
    else:
        return None
    

def file_complaint(data):
    locality_code = validate_locality(data)
    print(f"locality code is {locality_code}")
    headers = {'Content-Type': 'application/json'}
    data = {
    "service": {
        "tenantId": "pg.cityb",
        "serviceCode": data.get("service_code"),
        "description": "",
        "additionalDetail": {},
        "source": "web",
        "address": {
            "city": data.get("city", ""),
            "district": data.get("district", ""),
            "region": data.get("region", ""),
            "state": data.get("state", ""),
            "locality": {
                "code": locality_code,
                "name": data.get("locality", "")
            },
            "geoLocation": {}
        }
    },
    "workflow": {
        "action": "APPLY"
    },
    "RequestInfo": {
        "apiId": "Rainmaker",
        "authToken": data["auth_token"],
        "userInfo": {
            "id": 2079,
            "uuid": "7e2b023a-2f7f-444c-a48e-78d75911387a",
            "userName": data["username"],
            "name": data["name"],
            "mobileNumber": data["username"],
            "emailId": "",
            "locale": None,
            "type": "CITIZEN",
            "roles": [
                {
                    "name": "Citizen",
                    "code": "CITIZEN",
                    "tenantId": "pg"
                }
            ],
            "active": True,
            "tenantId": "pg",
            "permanentCity": "pg.citya"
        },
        "msgId": "1703653602370|en_IN",
        "plainAccessRequest": {}
    }
}
    url = "https://staging.digit.org/pgr-services/v2/request/_create"

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        error_code = response.json()["Errors"][0]["code"]
        if error_code == "NotNull.serviceRequest.service.address.locality.code":
            return {
                "error": "Given locality is not valid"
            }
        else:
            return {
                "error": "UNKNOWN_ERROR"
            }
    
def search_complaint(data):
    headers = {'Content-Type': 'application/json'}
    mobile_number = data["username"]
    url = f"https://staging.digit.org/pgr-services/v2/request/_search?tenantId=pg.cityb&mobileNumber={mobile_number}&_=1704443852959"

    data = {
        "RequestInfo":{
            "apiId":"Rainmaker",
            "authToken":data["auth_token"],
            "userInfo":{
                "id":2079,
                "uuid":"7e2b023a-2f7f-444c-a48e-78d75911387a",
                "userName":data["username"],
                "name":data["name"],
                "mobileNumber":data["mobile_number"],
                "emailId":"",
                "locale":None,
                "type":"CITIZEN",
                "roles":[
                    {
                        "name":"Citizen",
                        "code":"CITIZEN",
                        "tenantId":"pg"
                    }
                ],
                "active":True,
                "tenantId":"pg",
                "permanentCity":"pg.cityb"
            },
            "msgId":"1704443852959|en_IN",
            "plainAccessRequest":{}
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
        return response_data
    else:
        return None

    

