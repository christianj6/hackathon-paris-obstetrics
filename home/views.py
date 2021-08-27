from django.shortcuts import render
from django.http import HttpResponse
from .models import Content
import pandas as pd


class Item:
    def __init__(self, title, url, topics, text, images):
        self.title = title
        self.url = url
        self.topics = topics
        self.text = text
        self.images = images


data = pd.read_csv("res/data_home.csv")
items = []
for index, row in data.iterrows():
    items.append(
        Item(
            title=row["Source Title"],
            url=row["Source URL"],
            topics=[k for k, v in eval(row["Features"]).items() if v > 0.1],
            text=[paragraph for paragraph in row["Text"].split("\n")],
            images=[
                image
                for image in row["Images"]
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
                .split(",")
                if image != "None"
            ][:1],
        )
    )

c = {"Items": items}


def home(request):
    context = c
    return render(request, "home/home.html", context)


def about(request):
    return render(request, "home/about.html")
