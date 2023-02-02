import requests

def get_address_from_lat_long(data):
        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+ str(data['location_latitude'])+','+str(data['location_longitude'])+'&key=AIzaSyDsEBmD4Cu7yiavI2acEzpdMh-Om_oohhU'
            r = requests.get(url=url)
            # print("ererr")
            # print("ererr=====================================>>>>>>>>>>>>>")
            r = r.json()
            # print(r.keys())
            # print(r['results'][0]['formatted_address'])
            return r['results'][0]['formatted_address']
            # print(r['results'][0]['address_components']['formatted_address'])
        except Exception as e:
            return ''