from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from markdown2 import markdown
import random

from . import util


def entry(request, title):

    content = util.get_entry(title)
    if not content: 
        return render(request, "encyclopedia/error.html", {
            "error_title": "404 Not Found", 
            "error_details": "The page you have requested was not found."
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content)
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    query = request.GET.get("q")

    matches = query.lower() in (title.lower() for title in util.list_entries()) 
    if matches:
        return HttpResponseRedirect(reverse('entry', args=[query]))
    
    titles = []
    for title in util.list_entries():
        if query.lower() in title.lower():
            titles.append(title)

    return render(request, "encyclopedia/search.html", {
        "entries": titles
    })
        


def new(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("desc")
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error_title": "Already exists", 
                "error_details": "The page you are trying to create already exists"
            })
        
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=[title]))

    return render(request, "encyclopedia/new.html")


def edit(request, title):

    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, 
            "content": content
        }) 

    elif request.method == "POST":
        
        util.delete_entry(title)

        new_title = request.POST.get("title")
        new_content = request.POST.get("desc")
        
        if new_title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error_title": "Title already exists", 
                "error_details": "The tilte of the page you are trying to create already exists"
            })

        
        util.save_entry(new_title, new_content)
        return HttpResponseRedirect(reverse('entry', args=[new_title]))

       
def random_page(request):
    titles = util.list_entries()
    random_title = random.choice(titles)
    return HttpResponseRedirect(reverse('entry', args=[random_title]))