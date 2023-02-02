import requests
from requests.exceptions import HTTPError

REPLACE_STR = '{#var#}'

TEMP_REGISTRATION_SUCCESSFUL = {
"message_title" : "Company Registration",
"purpose": "TXN",
"sender_id":"ZENYLG",
"template_id":1107165709151830898,
"content":"Thank you {#var#} {#var#} {#var#} for registering with Quantagt. You will be notified shortly upon approval."
}

TEMP_REGISTRATION_OTP = {
"message_title" : "Quantagt Register OTP",
"purpose": "OTP",
"sender_id":"ZENYLG",
"template_id":1107165709050778516,
"content":"Your Verification OTP for Quantagt Registration is {#var#}"
}

TEMP_LOGIN_OTP = {
"message_title" :"Quantagt Login Otp",
"purpose": "OTP",
"sender_id":"ZENYLG",
"template_id":1107165709004657343,
"content":"Your Login OTP for Quantagt is {#var#}"
}

TEMP_EMPLOYEE_ADDED = {
"message_title" :"User added successfully",
"purpose": "TXN",
"sender_id":"ZENYLG",
"template_id":1107165832412060587,
"content":"You have been successfully registered with Quantagt by {#var#}. Download the Quantagt App in Play store/App store to login."
}


COUNTRY_PREFIX_IN = '+91'

def prepare_request(template, mobile):
    url = 'https://api.kaleyra.io/v1/HXIN1737577934IN/messages'
    payload = {"to":mobile, 'type':template['purpose'], 'sender':template['sender_id'], 'template_id':template['template_id'], 'body':template['content']}
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Accept-Charset': '*/*', 'api-key': 'A80c7e683c48ebc21dd7cdd49384caa29'}
    return {'url':url, 'headers':headers, 'payload':payload}

def send_company_registration_successful(name, mobile_number):
    data = prepare_request(TEMP_REGISTRATION_SUCCESSFUL, COUNTRY_PREFIX_IN+mobile_number)
    content = data['payload']['body']
    content = content.replace(REPLACE_STR, name) 
    data['payload']['body'] = content
    try:
        print(data['payload'])
        print(data['headers'])
        r = requests.post(url=data['url'], data=data['payload'], headers=data['headers'])
        print("ererr")
        print(r)
    except HTTPError as e:
        print("ererr44")
        print(e.response.text)

def send_company_registration_OTP(name, mobile_number, otp):
    data = prepare_request(TEMP_REGISTRATION_OTP, COUNTRY_PREFIX_IN+mobile_number)
    content = data['payload']['body']
    content = content.replace(REPLACE_STR, str(otp)) 
    data['payload']['body'] = content

    try:
        print(data['payload'])
        print(data['headers'])
        r = requests.post(url=data['url'], data=data['payload'], headers=data['headers'])
        print("ererr")
        print(r)
    except HTTPError as e:
        print("ererr44")
        print(e.response.text)

def send_employee_registration(company_name, mobile_number):
    # "content":"You have been successfully registered with Quantagt by {#var#}. Download the Quantagt App in Play store/App store to login."
    data = prepare_request(TEMP_EMPLOYEE_ADDED, COUNTRY_PREFIX_IN+mobile_number)
    content = data['payload']['body']
    content = content.replace(REPLACE_STR, company_name) 
    data['payload']['body'] = content

    try:
        print(data['payload'])
        print(data['headers'])
        r = requests.post(url=data['url'], data=data['payload'], headers=data['headers'])
        print("ererr")
        print(r)
    except HTTPError as e:
        print("ererr44")
        print(e.response.text)


def send_company_login_OTP(name, mobile_number, otp):
    data = prepare_request(TEMP_LOGIN_OTP, COUNTRY_PREFIX_IN+mobile_number)
    content = data['payload']['body']
    content = content.replace(REPLACE_STR, str(otp)) 
    data['payload']['body'] = content

    try:
        print(data['payload'])
        print(data['headers'])
        r = requests.post(url=data['url'], data=data['payload'], headers=data['headers'])
        print("ererr")
        print(r)
    except HTTPError as e:
        print("ererr44")
        print(e.response.text)

# def send_registration_otp(name, mobile_number):

