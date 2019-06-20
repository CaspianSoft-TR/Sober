import requests
import googlemaps
from api.models import *
import uuid

from api.serializers import UserSerializer

"""
	This function send notifications to given token devices
	Return "Response" type object

	* https://firebase.google.com/docs/cloud-messaging/http-server-ref
"""


def send_notification(token, messageTitle, messageBody):
    URL = "https://fcm.googleapis.com/fcm/send"
    fields = {
        'to': token,
        'notification': {
            'title': messageTitle,
            'body': messageBody
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key = AIzaSyAYd8wWQYEJFBzdLJgSGaa1fpJO0OT4APA'
    }

    return requests.post(url=URL, json=fields, headers=headers)


# Send message by firebase
def send_message(token, messageType, messageBody):
    URL = "https://fcm.googleapis.com/fcm/send"
    fields = {
        'to': token,
        'data': {
            'messageType': messageType,
            'body': messageBody
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key = AIzaSyAYd8wWQYEJFBzdLJgSGaa1fpJO0OT4APA'
    }

    return requests.post(url=URL, json=fields, headers=headers)


"""
    This function returns proper drivers for given book
    IMPROPER DRIVER CONDITIONS 
        >> rejected driver
        >> working in different book
        >> book owner
"""


def findProperDrivers(bookId):
    from django.db.models import Q

    # REJECTED & CANCELLED USERS
    improperDriverIdList = []
    for bookDriver in BookDriver.objects.all().filter(book_id=bookId):
        improperDriverIdList.append(bookDriver.driver.id)

    # Find Working Drivers
    for book in Booking.objects.all().filter(Q(status=1) | Q(status=20)):
        improperDriverIdList.append(book.driver.id)

    # BOOK OWNER
    improperDriverIdList.append(Booking.objects.get(id=bookId).customer.id)

    userProfileList = UserInfo.objects.all()
    driverList = userProfileList.filter(~Q(latitude='0'), ~Q(longitude='0'), is_driver=True).exclude(
        user_id__in=improperDriverIdList)

    return driverList


"""
	This function searches nearest drivers by latitude & longitude
"""


def findNearestDriver(latitude, longitude, filterMaxDistance, driverList):
    # -1- GET ALL PROPER DRIVERS & PREPARE DESTINATION STRING
    gmaps = googlemaps.Client(key='AIzaSyCePDBwi9tD1JrHm-qNvac8ScYq7roBUCI')
    # userProfileList = UserInfo.objects.all()
    # driverList = userProfileList.filter(is_driver=True)

    driverObjectList = []
    destinations = ''
    for driver in driverList:
        if not (driver.longitude == '0' and driver.latitude == '0'):

            if destinations == '':
                destinations = driver.latitude + ',' + driver.longitude
            else:
                destinations = destinations + '|' + driver.latitude + ',' + driver.longitude

            driverObjectList.append(driver)

    #  -2- CALL GOOGLEMAPS API TO FIND DISTANCE
    minDistanceIndex = -1
    minDistance = -1
    distanceResult = gmaps.distance_matrix(origins=latitude + ',' + longitude, destinations=destinations)
    print('distanceResult', distanceResult)
    for row in distanceResult['rows']:
        elementIndex = 0
        for element in row['elements']:
            distance = element['distance']
            if filterMaxDistance > distance['value']:
                if minDistance == -1 or distance['value'] < minDistance:
                    minDistance = distance['value']
                    minDistanceIndex = elementIndex

            elif distance['value'] >= minDistance:
                print("ERROR >> Distance filter error")

            elementIndex = elementIndex + 1
    return driverObjectList[minDistanceIndex]


def make_uuid():
    return uuid.uuid4().hex[:6].upper()


"""
	This function return driver rate
"""


def getDriverPoint():
    return 3


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'access_token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
