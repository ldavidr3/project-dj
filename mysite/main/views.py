from django.shortcuts import HttpResponseRedirect, render

from django.http import HttpResponse

from .models import ToDoList, Item
from .forms import CreateNewList

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    print(response.POST)
    if response.method == "POST":
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
    
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")
 
    return render(response, "main/list.html", {"ls":ls})

    #return HttpResponse("<h1>%s </h1> <br></br> <p>%s</p>" %(ls.name, str(item.text)))

def home(request):
    return render(request, 'main/home.html', {})


def create(request):
    if request.method == 'POST':
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data['name']
            t = ToDoList(name=n)
            t.save()
        
        return HttpResponseRedirect('/%i' %t.id)
    else:
        form = CreateNewList()
    return render(request, 'main/create.html', {'form':form})

