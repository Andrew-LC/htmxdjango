from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Contact

def index(request):
   query = request.GET.get("q")
   if query is not None:
      contacts = Contact.objects.filter(first__icontains=query)
   else:
      contacts = Contact.objects.all() 
      
   template = loader.get_template("contacts/index.html")
   context = {
         "contacts": contacts
   }
   return HttpResponse(template.render(context, request))
    
