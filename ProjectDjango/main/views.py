from django.shortcuts import render,redirect,reverse

from django.http import HttpResponse
from .models import Contacts,ProviderManager,Get_Contact
from models import ContactTable ,AddressTable


# Create your views here.
def contacts_home(request):
    return render(request,"main/contacts_home.html",{'message':'Hii All !'})



def add_contact_form(request):
    return render(request,'main/add_contact.html')



contacts = Contacts()



def add_contact11(request):

        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')

        try:
            c = ContactTable.objects.get(phone_no = phone_no)
            c.DoesNotExist()
        except :


            newcontact = ContactTable(name= name,phone_no=phone_no,email=email)
            newcontact.save()

            addr = AddressTable(phone_no= newcontact,street=street,city=city,state=state,pin_code=pin_code)

            addr.save()
            message = 'Contact successfully added!'

            return HttpResponse(message)
        else:
            message = 'Contact already exists!!'

            return HttpResponse(message)










def modify_contact_form(request):
    name = request.POST.get('name')

    phone_no = request.POST.get('phone_no')

    email = request.POST.get('email')

    street = request.POST.get('street')

    city = request.POST.get('city')

    state = request.POST.get('state')

    pin_code = request.POST.get('pin_code')

    return render(request, 'main/modify_contact.html',
                  {'name': name, 'phone_no': phone_no, 'email': email, 'street': street, 'city': city, 'state': state,
                   'pin_code': pin_code})


def modify_contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_no = request.POST['phone_no']
        email = request.POST['email']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pin_code']

        contact = ContactTable.objects.get(phone_no=phone_no)
        contact.name = name
        contact.email = email
        try:
            addr = AddressTable.objects.get(phone_no=phone_no)
            addr.DoesNotExist()
        except:
            addr = AddressTable(phone_no=phone_no,street= street,city= city,state=state,pin_code=pin_code)
            addr.save()

        else:

            addr.street = street
            addr.city = city
            addr.state = state
            addr.pin_code = pin_code
            addr.save()
            message = 'Contact successfully modified!'
            return HttpResponse(message)


def delete_contact_form(request):
    message = ''
    return render(request,'main/delete_contact.html',{'message': message})


def delete_contact(request):
    phone_no = request.POST.get('phone_no')

    try:
        c = ContactTable.objects.get(phone_no=phone_no)
        c.DoesNotExist()
    except:


        message = 'Contact Not  Exist!'

        return HttpResponse(message)
    else:
        c.delete()
        message = 'Contact deleted sussesfully!!'

        return HttpResponse(message)




def get_contact_form(request):
    message = ''
    return render(request,'main/get_contact.html', {'message':message})



def get_contact(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')



        try :
            c = ContactTable.objects.get(phone_no=phone_no)
            c.DoesNotExist()
        except :

            message = 'There is no contact with this phone number!'
            return render(request,'main/get_contact.html',{'message':message})
        else:

            contact = Get_Contact(c)



            return render(request, 'main/view_contact.html', {'contact': contact})


def get_provider_form(request):
    message = ''
    return render(request,'main/get_provider.html', {'message':message})



def get_provider11(request):

        phone_no = request.POST.get('phone_no')

        is_valid_phone_no = contacts.is_valid_phone_no(phone_no)
        if is_valid_phone_no:
            provider_name = ProviderManager.get_provider_name(phone_no)

            return HttpResponse(provider_name)
        else:
            message = 'Invalid phone number!!!!!'

            return HttpResponse(message)



def get_contacts_by_provider_form(request):
    return render(request,'main/get_contacts_by_provider.html')



def get_contacts_by_provider(request):
    if request.method == 'POST':
        provider_name = request.POST['provider']
        records = []

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
