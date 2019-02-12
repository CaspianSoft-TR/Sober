
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
    This function returns proper drivers for given book
    IMPROPER DRIVER CONDITIONS 
        >> rejected driver
        >> working in different book
        >> book owner
"""
def findProperDrivers(bookId):

    # REJECTED USERS
    improperDriverIdList = []
    for bookDriver in BookDriver.objects.all().filter(book_id=bookId):
        improperDriverIdList.append(bookDriver.driver.id)

    # WORKING DRIVER 
    for book in Booking.objects.all().filter(status=1):
        improperDriverIdList.append(book.driver.id)    

    # BOOK OWNER
    improperDriverIdList.append(Booking.objects.get(id=bookId).customer.id)

    userProfileList = UserInfo.objects.all()
    driverList = userProfileList.filter(is_driver=True).exclude(user_id__in=improperDriverIdList)

    return driverList



"""
	This function searches nearest drivers by latitude & longitude
"""
def findNearestDriver(latitude , longitude , filterMaxDistance , driverList):

    # -1- GET ALL PROPER DRIVERS & PREPARE DESTINATION STRING
    gmaps = googlemaps.Client(key='AIzaSyA2b8Zh0rzAJQjwDn0_CZ_tHdPXm6G2Sjs')
    #userProfileList = UserInfo.objects.all()
    #driverList = userProfileList.filter(is_driver=True)

    driverObjectList = []
    destinations = ''
    for driver in driverList:
        if not(driver.longitude=='0' and driver.latitude=='0'):

            if destinations == '':
                destinations = driver.latitude + ',' + driver.longitude
            else:
                destinations = destinations + '|' + driver.latitude + ',' + driver.longitude

            driverObjectList.append(driver)


    # -2- CALL GOOGLEMAPS API TO FIND DISTANCE
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