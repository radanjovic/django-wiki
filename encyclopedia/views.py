from django.shortcuts import render
from markdown2 import Markdown
import random
from django.http import HttpResponseRedirect
from . import util
from django.urls import reverse


def index(request):
    # POST: SEARCH
    if request.method == "POST":
        q = request.POST['q']
        entries = util.list_entries()
        match = []
        for entry in entries:
            if q == entry:
                return HttpResponseRedirect(f"wiki/{entry}")
            elif q in entry:
                match.append(entry)
        if len(match) != 0:
            return render(request, "encyclopedia/search.html", {"entries":match})
        return render(request, 'encyclopedia/no_entry.html')

    # GET: Displays index with all the entries and links to each of the entries. 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_entry(request, entry):
    # Entry - displays an entry when wiki/ENTRY typed.
    markdowner = Markdown()
    entries = util.list_entries()
    if entry in entries:
        i = entries.index(entry)
        entry = markdowner.convert(util.get_entry(entry))
        title = entries[i]
        return render(request, "encyclopedia/wiki_entry.html", {"entry": entry, "title": title})

    else:
        return render(request, "encyclopedia/no_entry.html")

def random_entry(request):
    # Random page - coded to just redirect to random page
    entries = util.list_entries()
    i = random.randrange(len(entries))
    entry = entries[i]
    return HttpResponseRedirect(f'wiki/{entry}')


    # Random page - coded as a separate page that gets random entry 
    # instead of just redirecting to some of the entries.

    #markdowner = Markdown()
    #entries = util.list_entries()
    #i = random.randrange(len(entries))
    #entry = util.get_entry(entries[i])
    #entry = markdowner.convert(entry)
    #return render(request, "encyclopedia/random.html", {"entry": entry})

def create(request):
    # Creating new page
    if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']
            entries = util.list_entries()
            for entry in entries:
                # if already exists - error
                if title == entry:
                    return render(request, "encyclopedia/no_create.html", {"entry":title})
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")

    # GET  
    return render(request, 'encyclopedia/create.html')


def edit(request, entry):
    # POST
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        # save_entry automatically replaces old with new
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/wiki/{title}")

    # GET
    content = util.get_entry(entry)
    title = entry
    return render(request, 'encyclopedia/edit.html', {"content": content, "title":title})
          