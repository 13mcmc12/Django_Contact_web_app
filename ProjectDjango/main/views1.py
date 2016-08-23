from django.shortcuts import render,redirect,reverse

from django.http import HttpResponse
from .models import Contacts,Contact,ContactDetails ,Provider,ProviderManager,Loaddata


# Create your views here.
def contacts_home(request):
    return render(request,"main/contacts_home.html",{'message':'Hii All !'})



def add_contact_form(request):
    return render(request,'main/add_contact.html')

data = Loaddata()
contact_list = data.get_data_from_jsonfile()
contacts = Contacts(contact_list)



def add_contact11(request):

        name = request.POST.get('name')
        print name

        phone_no = request.POST.get('phone_no')
        email = request.GET.get('email')

        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        is_contact_exist = contacts.is_contact_exist(phone_no)
        is_valid_phone_no = contacts.is_valid_phone_no(phone_no)
        if (not is_contact_exist) and is_valid_phone_no:
            contact = Contact(name, phone_no, email, street, city, state, pin_code)
            contacts.add_contact(contact)
            contacts.save_contacts_to_file()
            message = 'Contact successfully added!'


            return HttpResponse( message)
        elif is_contact_exist:
            message = 'Contact already exists!'

            return HttpResponse(message)
        else:
            message = 'Invalid phone number!'

            return HttpResponse(message)



def modify_contact_form(request):
    message = ''
    return render(request,'main/modify_contact.html', {'message':message})



def modify_contact(request):
    if request.method == 'POST':
        phone_no = request.form['phone_no']
        is_contact_exist = contacts.is_contact_exist(phone_no)
        if is_contact_exist:
            fields = request.form
            contacts.modify_contact(phone_no, fields)
            contacts.save_contacts_to_file()
            message = 'Contact successfully modified!'
            return render(request,'main/modify_contact.html', {'message':message})
        else:
            message = 'There is no contact with this phone number!'
            return render(request, 'main/modify_contact.html', {'message': message})



def delete_contact_form(request):
    message = ''
    return render(request,'main/delete_contact.html',{'message': message})


def delete_contact(request):

        phone_no = request.POST.get('phone_no')
        print phone_no
        is_contact_exist = contacts.is_contact_exist(phone_no)
        if is_contact_exist:
            contacts.delete_contact(phone_no)
            contacts.save_contacts_to_file()
            message = 'Contact deleted successfully!'
            return HttpResponse( message)
        else:
            message = 'There is no contact with this phone number!'
            return HttpResponse (message)



def get_contact_form(request):
    message = ''
    return render(request,'main/get_contact.html', {'message':message})



def get_contact(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        is_contact_exist = contacts.is_contact_exist(phone_no)
        if is_contact_exist:
            records = []
            records.append(contacts.get_contact(phone_no))
            return render(request,'main/view_contacts.html', {'records':records})
        else:
            message = 'There is no contact with this phone number!'
            return render(request,'main/get_contact.html',{'message':message})


def get_provider_form(request):
    message = ''
    return render(request,'main/get_provider.html', {'message':message})



def get_provider11(request):

        phone_no = request.POST.get('phone_no')
        print phone_no

        is_valid_phone_no = contacts.is_valid_phone_no(phone_no)
        if is_valid_phone_no:
            provider_name = contacts.get_provider(phone_no[0:4])

            return HttpResponse(provider_name)
        else:
            message = 'Invalid phone number!!!!!'

            return HttpResponse(message)



def get_contacts_by_provider_form(request):
    return render(request,'main/get_contacts_by_provider.html')



def get_contacts_by_provider(request):
    if request.method == 'POST':
        provider_name = request.POST['provider']
        print provider_name
        records = contacts.get_contacts_by_provider(provider_name)
        return render(request,'main/view_contacts.html', {'records':records})



def get_contacts_by_field_form(request):
    return render(request,'main/get_contacts_by_field.html')



def get_contacts_by_field(request):
    if request.method == 'POST':
        string = request.POST.get('string')
        field = request.POST.get('field')
        records = contacts.get_contacts_by_field(string, field)
        return render(request, 'main/view_contacts.html', {'records': records})
