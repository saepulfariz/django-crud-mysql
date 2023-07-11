from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm
from django.views.generic import ListView, DetailView
# from pyodbc import pyodbc
# from MySQLdb import _mysql
from MySQLdb.connections import _mysql


# db=_mysql.connect(host="localhost",user="root", password="",database="mydb")
# db.query("SELECT * FROM crudapp_contact")
# r=db.store_result()

class IndexView(ListView):
    template_name = 'crudapp/index.html'
    context_object_name = 'contact_list'

    def get_queryset(self):
        return Contact.objects.all()

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'crudapp/contact-detail.html'

def detail(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    try:
        res = Contact.objects.get(pk = pk)
        res_limit = Contact.objects.raw("SELECT * FROM crudapp_contact ORDER BY createdAt DESC LIMIT 1")[0]
        dataku = Contact.objects.raw("SELECT * FROM dataku")
        print(res_limit)
        context["data"] = res 
        context["res_limit"] = res_limit
        context["dataku"] = dataku
    except:
        return redirect('index')
         
    return render(request, "crudapp/contact-detail.html", context)

def create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = ContactForm()

    return render(request,'crudapp/create.html',{'form': form})

def edit(request, pk, template_name='crudapp/edit.html'):
    contact = get_object_or_404(Contact, pk=pk)
    # form = ContactForm(request.POST)
    # form = ContactForm(request.POST or None, instance=post)
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')
    # form = ContactForm()
    return render(request, template_name, {'form':form})

def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method=='POST':
        contact.delete()
        return redirect('index')
    return render(request, template_name, {'object':contact})