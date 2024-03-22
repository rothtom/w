from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.middleware import csrf
import markdown2
import requests
import os

from . import util


def index(request):
    entrie_names = util.list_entries()
    entrie_paths = []
    for name in entrie_names:
        entrie_paths.append(f"/wiki/{name}")
    entries = []
    for i in range(len(entrie_names)):
        entries.append({"name": entrie_names[i],
                        "path": entrie_paths[i]})

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def title(request, title):
    if entry := util.get_entry(title):
        if os.path.exists(f"templates/encyclopedia/{title}.html") != True:
            create_template(title, entry)
        return render(request, f"templates/encyclopedia/{title}.html")
    return render(request, "encyclopedia/entry_not_found.html")

def search(request, keyword):
    if request.method != "GET":
        return HttpResponseRedirect("")
    
    if util.get_entry(keyword) != None:
        return HttpResponseRedirect(f"wiki/{keyword}")
    
    entries = util.list_entries()
    matches = []
    for entry in entries:
        if keyword in entry:
            matches.append(entry)
    
    return render(request, "encyclopedia/search_results.html", {
        "results": matches
    })
    


def create_template(title, entry):
    path = os.path.join("templates/encyclopedia/", f"{title}.html")
    with open(path, "w") as f:
        print("Hello")
        f.write(entry)

