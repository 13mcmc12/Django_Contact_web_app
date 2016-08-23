"""ProjectDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.contacts_home,name='contacts_home'),
    url(r'^add_contact_form$',views.add_contact_form,name='add_contact_form'),
    url(r'^delete_contact_form$',views.delete_contact_form,name="delete_contact_form"),
    url(r'^get_contact$',views.get_contact_form,name = 'get_contact_form'),
    url(r'^get_provider$',views.get_provider_form,name = "get_provider_form"),
    url(r'^get_contacts_by_provider_form$',views.get_contacts_by_provider_form,name='get_contacts_by_provider_form'),
    url(r'^get_contacts_by_provider1$',views.get_contacts_by_provider,name='get_contacts_by_provider1'),
    url(r'^get_contacts_by_field_form$',views.get_contacts_by_field_form,name='get_contacts_by_field_form'),
    url(r'^get_contacts_by_field1$',views.get_contacts_by_field,name='get_contacts_by_field'),
    url(r'^delete_contact1$',views.delete_contact,name='delete_contact1'),
    url(r'^get_contact1$',views.get_contact,name='get_contact1'),
    url(r'^get_provider11$',views.get_provider11,name='get_provider11'),
    url(r'^add_contact11$',views.add_contact11,name='add_contact11'),
    url(r'^modify_contact_form$',views.modify_contact_form,name='modify_contact_form'),
    url(r'^modify_contact1$',views.modify_contact,name='modify_contact1')



]
