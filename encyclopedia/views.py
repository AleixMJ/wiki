from django.shortcuts import render
import markdown

from . import util





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Function that checks if an entry exist
def entry(request, entry):
    # Check that the entry exists regardless of the capitalisation used
    allEntries = util.list_entries()
    response = entry
    for x in allEntries:
        if x.lower() == entry.lower():
            response = x
            break    
    # Convert to Markdown if entry exists and error if it doens't
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

# Function that allows the Search Bar to check for an entry in the wiki and show recommendations if it does not exist.
def bar(request):
    if request.method == "POST":
        allEntries = util.list_entries()
        # Check that the entry exists regardless of the capitalisation used
        search = request.POST["entry"]
        for x in allEntries:
            if x.lower() == search.lower():
                search = x
                # process the entry function to return the data with Markdown
                return entry(request, search)  
        # Return recommendations to the search if the entry does not exist
        similar = [k for k in allEntries if search.lower() in k.lower()]
        print(similar)
        if similar != []:
            return render(request, "encyclopedia/results.html", {
            "name": search,
            "similar": similar
            })
        # Return an error if there are no recommendations to show
        else:
            return render(request, "encyclopedia/error.html", {
            "name": search,
            "error": "The requested page doesn't exist"
        })

# Function used to create new pages for the wiki
def page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["page"]
        # Check that the entry exists regardless of the capitalisation used
        allEntries = util.list_entries()
        for x in allEntries:
            if x.lower() == title.lower():
                title = x
                return render(request, "encyclopedia/error.html", {
                "name": title,
                "error": "The page already exist, please use the edit function"
                })
        # If the entry does not exist, then save the entry and render the new page by calling entry function.           
        util.save_entry(title, content)            
        return entry(request, title)
    else:
        return render(request, "encyclopedia/page.html")
