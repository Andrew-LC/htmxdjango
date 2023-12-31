from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse
from django.template import loader
from .models import Contact
from .forms import NewContact
from .archiver import Archiver
from wsgiref.util import FileWrapper
from urllib.parse import quote as urlquote


def index(request):
    query = request.GET.get("q")
    
    if query:
        contacts = Contact.objects.filter(
            first__icontains=query
        )

        if request.headers.get("HX-Trigger") == "search":
            return render(request, "contacts/row.html", {"contacts": contacts, "archiver": Archiver.get() })
    else:
        contacts = Contact.objects.all()

    context = {
        "contacts": contacts,
        "archiver": Archiver.get(),
    }

    # Bulk delete
    if request.method == "POST":
        contact_ids = list(map(int, request.POST.getlist("selected_contact_ids")))
        print(request.POST.getlist("selected_contact_ids"))
        Contact.objects.filter(pk__in=contact_ids).delete()
        messages.success(request, "Deleted Contacts!")

    return render(request, "contacts/index.html", context)

    
def new(request):
    if request.method == "POST":
        form = NewContact(request.POST)
        if form.is_valid():
            new_contact = Contact(
                email=form.cleaned_data['email'],
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
        if request.headers.get("HX-Trigger") == "delete":
            return redirect("/contacts", 303)
        else:
            return HttpResponse("")
    else:
        messages.error(request, "Invalid request method for contact deletion")
        print("didnt work mate")
        return redirect("/contacts")


def count(request):
    count = Contact.objects.count()
    value = f"({count} total Contacts)" 
    return HttpResponse(value)

def archive(request):
    archiver = Archiver.get()
    print(archiver)
    archiver.run()
    return render(request, "contacts/archive.html", {"archiver": archiver})

def archive_content(request):
    manager = Archiver.get()
    file_path = manager.archive_file()

    with open(file_path, 'rb') as file:
        response = FileResponse(FileWrapper(file), as_attachment=True, filename="contacts.json")
        response['Content-Disposition'] = f'attachment; filename={urlquote("contacts.json")}'
        return response
