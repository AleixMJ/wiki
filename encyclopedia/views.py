from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html", {
            "name": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {     
            "name": entry,       
            "entry":util.get_entry(entry)
        })

def bar(request):
    if request.method == "POST":
        search = request.POST["entry"]
        if util.get_entry(search) == None:
            all = util.list_entries()
            print(all)
            similar = [k for k in all if search in k]
            print(similar)
            return render(request, "encyclopedia/results.html", {
            "name": entry,
            "similar": similar
            })
        else:
            return entry(request, search)