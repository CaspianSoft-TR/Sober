
import requests 
import googlemaps
from api.models import *

"""
	This function send notifications to given token devices
	Return "Response" type object

	* https://firebase.google.com/docs/cloud-messaging/http-server-ref
"""
def send_notification(token , messageTitle, messageBody):
	URL = "https://fcm.googleapis.com/fcm/send"
	fields = {
		'to':token,
		'notification':{
			'title':messageTitle,
			'body':messageBody
		}
	}

	headers = {
		'Content-Type':'application/json',
		'Authorization':'key = AIzaSyAYd8wWQYEJFBzdLJgSGaa1fpJO0OT4APA'
		}

	return requests.post(url=URL,json=fields,headers=headers) 



"""
	This function searches nearest drivers by latitude & longitude
"""
def findNearestDriver(latitude , longitude , filterMaxDistance):

    gmaps = googlemaps.Client(key='AIzaSyA2b8Zh0rzAJQjwDn0_CZ_tHdPXm6G2Sjs')
    # -1- GET ALL PROPER DRIVERS & LOCATION
    # -2- CALL GOOGLEMAPS API TO FIND DISTANCE
    # -3- IF DISTANCE <= 5000 
    userProfileList = UserInfo.objects.all()
    driverList = userProfileList.filter(is_driver=True)

    driverObjectList = []
    destinations = ''
    for driver in driverList:
        if not(driver.longitude=='0' and driver.latitude=='0'):

            if destinations == '':
                destinations = driver.latitude + ',' + driver.longitude
            else:
                destinations = destinations + '|' + driver.latitude + ',' + driver.longitude

            driverObjectList.append(driver)


    minDistanceIndex = -1
    minDistance = -1
    distanceResult = gmaps.distance_matrix(origins= latitude+','+longitude,destinations=destinations)
    for row in distanceResult['rows']:
        elementIndex = 0
        for element in row['elements']:
            distance = element['distance']
            if filterMaxDistance > distance['value']:
                if minDistance==-1 or distance['value'] < minDistance:
                    minDistance = distance['value']
                    minDistanceIndex = elementIndex

            elif distance['value'] >= minDistance:
                print("ERROR >> Distance filter error")
                        
            elementIndex=elementIndex+1
    return driverObjectList[minDistanceIndex]


"""
	This function return driver rate
"""
def getDriverPoint():
    return 3