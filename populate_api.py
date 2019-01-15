import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sober.settings')

import django
django.setup()

## FAKE POP SCRIPT
import random
from api.models import MyStore
from faker import Faker

fakegen = Faker()
stores = ['Caspiansoft','Guppy','XYZ']

def add_store():
    s = MyStore.objects.get_or_create(storeName=random.choice(stores))[0]
    s.save()
    return s 

def populate(N=10):
    for entry in range(N):

        # Create fake data
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        mystore = MyStore.objects.get_or_create(storeName=fake_name,storeId=fake_name)

        # Burada test amaçlı sadece tek bir model populate edilmiştir
        # Daha fazlası edilebilir

if __name__ == '__main__':
    print("Populating Script!")
    populate(40)
    print("Populating Complete!")

