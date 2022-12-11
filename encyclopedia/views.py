from django.shortcuts import render
import markdown

from . import util





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    allEntries = util.list_entries()
    response = entry
    for x in allEntries:
        if x.lower() == entry.lower():
            response = x
            break    
    temp = markdown.Markdown()
    name = util.get_entry(response)
    if name is None:
        return render(request, "encyclopedia/error.html", {
            "name": entry,
            "error": "The requested page doesn't exist"
        })
    else:       
        return render(request, "encyclopedia/entry.html", {    
            "entry":temp.convert(name),
            "name": entry
        })

def bar(request):
    if request.method == "POST":
        search = request.POST["entry"]
        if util.get_entry(search) == None:
            all = util.list_entries()
            similar = [k for k in all if search.lower() in k.lower()]
            return render(request, "encyclopedia/results.html", {
            "name": entry,
            "similar": similar
            })
        else:
            return entry(request, search)

def page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["page"]
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/error.html", {
            "name": title,
            "error": "The page already exist, please use the edit function"
        })
        else:
            util.save_entry(title, content)            
            return entry(request, title)

    else:

        return render(request, "encyclopedia/page.html")