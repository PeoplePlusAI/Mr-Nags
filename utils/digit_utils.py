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
    
def validate_city(data):
    headers = {'Content-Type': 'application/json'}
    source_city = data.get("city", "")
    print(data)
    data = {
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
        },
        "MdmsCriteria": {
            "tenantId": "pg",
            "moduleDetails": [
                {
                    "moduleName": "tenant",
                    "masterDetails": [
                        {
                            "name": "tenants"
                        }
                    ]
                }
            ]
        }
    }

    url = "https://staging.digit.org/egov-mdms-service/v1/_search"

    response = requests.post(
        url, 
        headers=headers, 
        data=json.dumps(data), 
        verify=False
    )

    if response.status_code == 200:
        response_data = response.json()
        cities = {}
        for city in response_data["MdmsRes"]["tenant"]["tenants"]:
            city_name = city["name"].lower().replace(" ", "")
            cities[city_name] = city["code"]
        source_city = source_city.lower().replace(" ", "")
        code = cities.get(source_city.lower(), None)
    else:
        code = None
    if code:
        return {
                "city_code": code
            }
    else:
        cities_str = "\n".join(
            [city["name"] for city in response_data["MdmsRes"]["tenant"]["tenants"]]
        )
        return {
            "error": f"Service is unavailable in this city. Choose another city from this list\n  {cities_str}"
        }
    
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

    city_code = data.get("city_code", "")
    headers = {'Content-Type': 'application/json'}
    url = f"https://staging.digit.org/egov-location/location/v11/boundarys/_search?hierarchyTypeCode=ADMIN&boundaryType=Locality&tenantId={city_code}"

    response = requests.post(url, headers=headers, data=json.dumps(complaint_data), verify=False)

    if response.status_code == 200:
        response_data = response.json()
        localities = {}
        for locality in response_data["TenantBoundary"][0]["boundary"]:
            locality_name = locality["name"].lower().replace(" ", "")
            localities[locality_name] = locality["code"]
        source_locality = data.get("locality", "").lower()
        source_locality = source_locality.replace(" ", "").lower()
        locality_code = localities.get(source_locality, None)
    else:
        locality_code = None
    if locality_code:
        return {
            "locality_code": locality_code
        }
    else:
        localities_str = "\n".join(
            [locality["name"] for locality in response_data["TenantBoundary"][0]["boundary"]]
        )
        return {
            "error": f"Service is unavailable in this locality. Choose another locality from this list {localities_str}"
        }
    

def file_complaint(data):
    city_code = validate_city(data)
    if "error" in city_code:
        return city_code
    data["city_code"] = city_code.get("city_code")
    locality_code = validate_locality(data)
    if "error" in locality_code:
        return locality_code
    data["locality_code"] = locality_code.get("locality_code")
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
                "code": data.get("locality_code", ""),
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
        return {
            "error": "Something went wrong please try again later"
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

    

