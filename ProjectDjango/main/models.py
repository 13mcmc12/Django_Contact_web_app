from __future__ import unicode_literals

from django.db import models


# Create your models here.


#tables
class ContactTable(models.Model):
    name = models.CharField(max_length=30,blank=True)
    phone_no = models.CharField(max_length=30 ,primary_key=True)
    email = models.EmailField(max_length=100, blank=True )


class AddressTable(models.Model):
    c = ContactTable()
    phone_no = models.ForeignKey(c,on_delete=models.CASCADE)
    street = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    pin_code = models.CharField(max_length=6, blank=True)

class ProviderTable(models.Model):

    provider_name = models.CharField(max_length=20, blank=True)
    list = models.CharField(max_length=4,blank=True)


    def __str__(self):  # __unicode__ on Python 2
        return (self.provider_name,self.list)
#end tables

class Address:
    def __init__(self, street, city, state, pin_code):
        self.street = street
        self.city = city
        self.state = state
        self.pin_code = pin_code

    def get_json(self):
        json = {}
        json["street"] = self.street
        json["city"] = self.city
        json["state"] = self.city
        json["pin_code"] = self.pin_code
        return json

    def set_street(self, street):
        self.street = street

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state

    def set_pin_code(self, pin_code):
        self.pin_code = pin_code

    def get_street(self):
        return self.street

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_pin_code(self):
        return self.pin_code


class Contact:
    def __init__(self, name, phone_no, email, street, city, state, pin_code):
        self.name = name
        self.phone_no = phone_no
        self.email = email
        self.address = Address(street, city, state, pin_code)

    def get_json(self):
        json = {}
        json["name"] = self.name
        json["phone_no"] = self.phone_no
        json["email"] = self.email
        json["address"] = self.address.get_json()
        return json

    def set_name(self, name):
        self.name = name

    def set_phone_no(self, phone_no):
        self.phone_no = phone_no

    def set_email(self, email):
        self.email = email

    def set_address(self, address):
        self.address = address

    def get_name(self):
        return self.name

    def get_phone_no(self):
        return self.phone_no

    def get_email(self):
        return self.email

    def get_address(self):
        return self.address

class Get_Contact():
    def __init__(self,c):
        self.name = c.name
        self.phone_no = c.phone_no
        self.email = c.email
        try:
            a = AddressTable.objects.get(phone_no= c.phone_no)
            a.DoesNotExist()
        except:

            self.street = ''
            self.city = ''
            self.state = ''
            self.pin_code = 0
        else:
            self.street = a.street
            self.city = a.city
            self.state = a.state
            self.pin_code = a.pin_code



class ContactDetails:
    NAME = 'name'
    PHONE_NO = 'phone_no'
    EMAIL = 'email'
    ADDRESS = 'address'
    STREET = 'street'
    CITY = 'city'
    STATE = 'state'
    PIN_CODE = 'pin_code'


class Provider:
    def __init__(self, provider_name):
        self.provider_name = provider_name


    def add_series(self, series):
        try :
            p = ProviderTable.objects.get(list=series)
            p.DoesNotExist()
        except:
            pr = ProviderTable(provider_name= self.provider_name,list= series)
            pr.save()
        else:
            pass

class ProviderManager:

    @staticmethod
    def get_provider_name(phone_no):
        try:
            p = ProviderTable.objects.get(list=phone_no[0:4])
            p.DoesNotExist()
        except:
            return 'Others'
        else:
            return p.provider_name




class Contacts:
    def __init__(self, contact_list = None):
        self.contact_list = contact_list

    def is_contact_exist(self, phone_no):
        try:
            c = ContactTable.objects.get(phone_no=phone_no)
            c.DoesNotExist()
        except:
            return False
        else:
            return True

    @staticmethod
    def is_valid_phone_no(phone_no):
        if len(phone_no) == 10 and phone_no[0] != '0':
            return True
        else:
            return False



    def add_contact(self, contact):
        self.contact_list[contact.phone_no] = contact

    def modify_contact(self, phone_no, fields):
        for field in fields.keys():
            if field == ContactDetails.NAME:
                self.contact_list[phone_no].name = fields[field]
            elif field == ContactDetails.PHONE_NO:
                self.contact_list[phone_no].phone_no = fields[field]
            elif field == ContactDetails.EMAIL:
                self.contact_list[phone_no].email = fields[field]
            elif field == ContactDetails.STREET:
                self.contact_list[phone_no].address.street = fields[field]
            elif field == ContactDetails.CITY:
                self.contact_list[phone_no].address.city = fields[field]
            elif field == ContactDetails.STATE:
                self.contact_list[phone_no].address.state = fields[field]
            elif field == ContactDetails.PIN_CODE:
                self.contact_list[phone_no].address.pin_code = fields[field]

    def delete_contact(self, phone_no):
        del self.contact_list[phone_no]

    def get_contact(self, phone_no):
        return self.contact_list[phone_no]

    @staticmethod
    def get_provider(phone_no):
        return ProviderManager.get_provider_name(phone_no[0:4])

    def get_contacts_by_provider(self, provider_name):
        li = []
        provider = ContactTable.objects.all()
        for lis in provider :

            if self.get_provider(lis.phone_no) == provider_name:
                contact = Get_Contact(lis)
                li.append(contact)
        return li






    def get_contacts_by_field(self, st, field):
        li = []
        addr = AddressTable.objects.all()
        for contact in  ContactTable.objects.all():
            if field == ContactDetails.NAME and st in contact.name:
                li.append(Get_Contact(contact))

            elif field == ContactDetails.PHONE_NO and st in contact.phone_no:
                li.append(Get_Contact(contact))
            elif field == ContactDetails.EMAIL and st in contact.email:
                li.append(Get_Contact(contact))

        for ad in addr:
            if field == ContactDetails.STREET and st in ad.street:
                li.append(Get_Contact(contact))
            elif field == ContactDetails.CITY and st in ad.city:
                li.append(Get_Contact(contact))
            elif field == ContactDetails.STATE and st in ad.state:
                li.append(Get_Contact(contact))
            elif field == ContactDetails.PIN_CODE and st in ad.pin_code:
                li.append(Get_Contact(contact))

        return li


