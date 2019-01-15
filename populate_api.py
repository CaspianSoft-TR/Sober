import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sober.settings')

import django
django.setup()

## FAKE POP SCRIPT
import random
from api.models import Driver
from faker import Faker

fakegen = Faker()
stores = ['Caspiansoft','Guppy','XYZ']

def add_car():
    fake_company_name = fakegen.company()
    fake_plate_number =fake.ean8()
    car = Car.objects.get_or_create(car_brand=fake_company_name,number_plate=fake_plate_number)[0]
    car.save()
    return car 

def add_driver():
    fake_driver_name = fakegen.name()
    fake_driver_email = fake.email()
    driver = Driver.objects.get_or_create(name=fake_driver_name,email=fake_driver_email)[0]
    driver.save()
    return driver 


def populate(N=10):
    for entry in range(N):

    	car = add_car()

        # Create fake data
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        #mystore = MyStore.objects.get_or_create(storeName=fake_name,storeId=fake_name)

        # Burada test amaçlı sadece tek bir model populate edilmiştir
        # Daha fazlası edilebilir

if __name__ == '__main__':
    print("Populating Script!")
    populate(40)
    print("Populating Complete!")