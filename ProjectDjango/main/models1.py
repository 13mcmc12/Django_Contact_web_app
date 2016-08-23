from __future__ import unicode_literals

from django.db import models


# Create your models here.
import json
import os
#tables





































class ContactTable(models.Model):
    name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=30 ,primary_key=True)
    email = models.CharField(max_length=30)


class AddressTable(models.Model):
    phone_no = models.ForeignKey(ContactTable)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pin_code = models.IntegerField()

class ProviderTable(models.Model):
    phone_no = models.ForeignKey(ContactTable)
    provider_name = models.CharField(max_length=20)
    list = models.CommaSeparatedIntegerField
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
        self.series_list = []

    def add_series(self, series):
        self.series_list.append(series)


class ProviderManager:
    provider_list = []
    provider = Provider("Airtel")
    provider.add_series("9900")
    provider.add_series("9800")
    provider.add_series("9811")
    provider_list.append(provider)
    provider = Provider("BSNL")
    provider.add_series("9440")
    provider.add_series("9822")
    provider_list.append(provider)
    provider = Provider("Reliance")
    provider.add_series("9300")
    provider.add_series("9812")
    provider_list.append(provider)

    @staticmethod
    def get_provider_name(phone_no):
        for provider in ProviderManager.provider_list:
            if phone_no[0:4] in provider.series_list:
                return provider.provider_name
        return "Other"


class Contacts:
    def __init__(self, contact_list):
        self.contact_list = contact_list

    def is_contact_exist(self, phone_no):
        if phone_no not in self.contact_list.keys():
            return False
        else:
            return True

    @staticmethod
    def is_valid_phone_no(phone_no):
        if len(phone_no) == 10 and phone_no[0] != '0':
            return True
        else:
            return False

    def save_contacts_to_file(self):
        final_contact_list = {}
        for key, value in self.contact_list.items():
            final_contact_list[key] = value.get_json()
        with open('contacts_data.json', 'w') as data_file:
            json.dump(final_contact_list, data_file, indent=2)

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
        for phone, contact in self.contact_list.items():
            if self.get_provider(phone) == provider_name:
                li.append(contact)
        return li

    def get_contacts_by_field(self, st, field):
        li = []
        for phone, contact in self.contact_list.items():
            if field == ContactDetails.NAME and st in contact.name:
                li.append(contact)
            elif field == ContactDetails.PHONE_NO and st in contact.phone_no:
                li.append(contact)
            elif field == ContactDetails.EMAIL and st in contact.email:
                li.append(contact)
            elif field == ContactDetails.STREET and st in contact.address.street:
                li.append(contact)
            elif field == ContactDetails.CITY and st in contact.address.city:
                li.append(contact)
            elif field == ContactDetails.STATE and st in contact.address.state:
                li.append(contact)
            elif field == ContactDetails.PIN_CODE and st in contact.address.pin_code:
                li.append(contact)
        return li


class Loaddata():
    def get_data_from_jsonfile(self):
        contact_list = {}
        if os.path.isfile('contacts_data.json') and os.path.getsize('contacts_data.json') > 0:
            with open('contacts_data.json') as data_file:
                json_data = json.load(data_file)
            for key, value in json_data.items():
                ct = Contact(value[ContactDetails.NAME], value[ContactDetails.PHONE_NO], value[ContactDetails.EMAIL],
                             value[ContactDetails.ADDRESS][ContactDetails.STREET],
                             value[ContactDetails.ADDRESS][ContactDetails.CITY],
                             value[ContactDetails.ADDRESS][ContactDetails.STATE],
                             value[ContactDetails.ADDRESS][ContactDetails.PIN_CODE])
                contact_list[key] = ct
            return contact_list

