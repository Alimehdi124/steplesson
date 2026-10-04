"""Dərs 8: hər səhifə məlumatı template-ə render() ilə ötürür."""

from django.http import Http404
from django.shortcuts import render

from .data import CATEGORIES, POSTS


def posts_list(request):
    return render(request, "posts.html", {"posts": POSTS})


def post_detail(request, post_id):
    for post in POSTS:
        if post["id"] == post_id:
            return render(request, "post_detail.html", {"post": post})
    raise Http404("Post tapılmadı")


def category_list(request):
    return render(request, "categories.html", {"categories": CATEGORIES})


def category_detail(request, category_slug):
    for category in CATEGORIES:
        if category["slug"] == category_slug:
            category_posts = []
            for post in POSTS:
                if post["category"] == category_slug:
                    category_posts.append(post)
            return render(request, "category_detail.html", {
                "category": category, "posts": category_posts,
            })
    raise Http404("Kateqoriya tapılmadı")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def author_posts(request, name):
    author_post_list = []
    for post in POSTS:
        if post["author"] == name:
            author_post_list.append(post)
    return render(request, "author_posts.html", {
        "author": name, "posts": author_post_list,
    })


def latest(request):
    return render(request, "latest.html", {"posts": POSTS[-3:]})


def stats(request):
    return render(request, "stats.html", {"posts": POSTS, "categories": CATEGORIES})
