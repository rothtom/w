from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.middleware import csrf
import markdown2
import os
import requests
from random import choice

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
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry)
        })
    return render(request, "encyclopedia/entry_not_found.html")


def search(request):
    if request.method != "GET":
        return HttpResponseRedirect("../")
    
    keyword = request.GET["q"].lower()
    
    if util.get_entry(keyword) != None:
        return HttpResponseRedirect(f"../wiki/{keyword}")
    
    entries = util.list_entries()
    matches = []
    for entry in entries:
        print(entry)
        if keyword in entry.lower():
            matches.append(entry)

    if matches == []:
        return HttpResponseRedirect("../")
    
    print("results")
    return render(request, "encyclopedia/search_results.html", {
        "keyword": keyword,
        "results": matches
    })


def new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    
    title = request.POST.get("title")
    content = request.POST.get("content")

    if title in util.list_entries():
        return render(request, "encyclopedia/entry_already_exists_error.html", {
            "title": title
        })
    
    util.save_entry(title, content)
    
    return HttpResponseRedirect(f"../wiki/{title}")


def random(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{entry}")

def edit(request):
    if request.method == "GET":
        title = request.GET.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "content": content
        })
    
    title = request.POST.get("title")
    content = request.POST.get("content")

    util.save_entry(title, content)
    return HttpResponseRedirect(f"../wiki/{title}")

    