from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader
from .models import Contact
from .forms import NewContact

def index(request):
    query = request.GET.get("q")
    page_number = request.GET.get("page", 1)

    if query:
        contacts = Contact.objects.filter(first__icontains=query)
    else:
        contacts = Contact.objects.all()

    # Paginate the contacts with 10 contacts per page
    paginator = Paginator(contacts, 10)
    page = paginator.get_page(page_number)

    context = {
        "contacts": page,
        "query": query,
    }
    return render(request, "contacts/index.html", context)

def new(request):
    if request.method == "POST":
        form = NewContact(request.POST)
        if form.is_valid():
            new_contact = Contact(
                first=form.cleaned_data['first_name'],
                last=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone']
            )
            new_contact.save()
            messages.success(request, "Successfully created a new contact")
            return redirect("/contacts")
        else:
            messages.error(request, "Form validation error")
    else:
        form = NewContact()

    template = loader.get_template("contacts/new.html")
    return HttpResponse(template.render({"form": form}, request))


def view(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(contact)
    template = loader.get_template("contacts/view.html")
    return HttpResponse(template.render({"contact": contact}, request))


def edit(request, contact_id):
    contact = Contact.objects.get(id=contact_id)

    if request.method == "POST":
       form = NewContact(request.POST)
       if form.is_valid():
          contact.first = form.cleaned_data['first_name']
          contact.last = form.cleaned_data['last_name']
          contact.phone = form.cleaned_data['phone']
          contact.save()
          messages.success(request, "Successfully updated contact")
          return redirect("/contacts")
       else:
          messages.error(request, "Form validation error")
    else:
       form = NewContact()

    template = loader.get_template("contacts/edit.html")
    return HttpResponse(template.render({"form": form, "contact": contact}, request))


def delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "DELETE":
        contact.delete()
        messages.success(request, "Successfully deleted contact")
        return redirect("/contacts", 303)
    else:
        messages.error(request, "Invalid request method for contact deletion")
        print("didnt work mate")
        return redirect("/contacts")
