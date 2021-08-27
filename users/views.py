from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import Practice
from django.contrib.auth.models import User
import json
import io
import decimal
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
import matplotlib

from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Bar
from django.db.models import Q
from buddy.models import BuddyBoard, ContentID

from django import forms


class AssessmentForm(forms.Form):

    proficiency_choices = (
        ("NONE", "No Knowledge"),
        ("BEGINNER", "Some Knowledge"),
        ("INTERMEDIATE", "Intermediate Knowledge"),
        ("ADEPT", "Very Good Knowledge"),
        ("EXPERT", "Expert Knowledge"),
    )

    Psychological_Distress_Management = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Providing_Ante_Natal_Care = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Research_Knowledge = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Treating_Retained_Placenta = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Administering_Medication = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Handling_Fetal_Risks = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Appropriate_Communication = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Risk_Assessment = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Advising_New_Mothers_About_Breastfeeding = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Treating_Post_Natal_Complications = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )
    Using_Specialized_Tools = forms.ChoiceField(
        choices=proficiency_choices, widget=forms.Select
    )


class Item:
    def __init__(
        self, title, url, topics, text, images, id, text_es="", title_es=""
    ):
        self.title = title
        self.url = url
        self.topics = topics
        self.text = text
        self.images = images
        self.id = id
        self.text_es = text_es
        self.title_es = title_es


class Skill:
    def __init__(self, skill, value):
        self.skill = skill
        self.value = value


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")

            messages.success(
                request, f"Welcome {username}. You are now able to log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def assessment(request):

    proficiency_mapping = {
        "NONE": 0.0,
        "BEGINNER": 0.2,
        "INTERMEDIATE": 0.4,
        "ADEPT": 0.7,
        "EXPERT": 0.9,
    }

    if request.method == "POST":
        form = AssessmentForm(request.POST)
        if form.is_valid():
            prof_f_psychology = form.cleaned_data.get(
                "Psychological_Distress_Management"
            )
            prof_f_prepregnancy = form.cleaned_data.get(
                "Providing_Ante_Natal_Care"
            )
            prof_f_research = form.cleaned_data.get("Research_Knowledge")
            prof_f_placenta = form.cleaned_data.get(
                "Treating_Retained_Placenta"
            )
            prof_f_medication = form.cleaned_data.get(
                "Administering_Medication"
            )
            prof_f_fetus = form.cleaned_data.get("Handling_Fetal_Risks")
            prof_f_communication = form.cleaned_data.get(
                "Appropriate_Communication"
            )
            prof_f_risks = form.cleaned_data.get("Risk_Assessment")
            prof_f_breastfeed = form.cleaned_data.get(
                "Advising_New_Mothers_About_Breastfeeding"
            )
            prof_f_bleeding = form.cleaned_data.get(
                "Treating_Post_Natal_Complications"
            )
            prof_f_tools = form.cleaned_data.get("Using_Specialized_Tools")

            Practice.objects.create(
                user=request.user,
                f_psychology=proficiency_mapping.get(prof_f_psychology),
                f_prepregnancy=proficiency_mapping.get(prof_f_prepregnancy),
                f_research=proficiency_mapping.get(prof_f_research),
                f_placenta=proficiency_mapping.get(prof_f_placenta),
                f_medication=proficiency_mapping.get(prof_f_medication),
                f_fetus=proficiency_mapping.get(prof_f_fetus),
                f_communication=proficiency_mapping.get(prof_f_communication),
                f_risks=proficiency_mapping.get(prof_f_risks),
                f_breastfeed=proficiency_mapping.get(prof_f_breastfeed),
                f_bleeding=proficiency_mapping.get(prof_f_bleeding),
                f_tools=proficiency_mapping.get(prof_f_tools),
            )

            messages.success(
                request, f"You are now able to access the content page."
            )
            return redirect("practice")

    else:
        form = AssessmentForm()

    return render(request, "users/assessment.html", {"form": form})

    # redirected here from practice if not Practice object
    # otherwise they just go to the content page
    # logic to process the html form to create a new practice object for the user


# the lowest n skills of the user
def get_lowest_skills(skill_set, lowestn=2):
    return {
        k: v
        for k, v in sorted(skill_set.items(), key=lambda item: item[1])[
            :lowestn
        ]
    }.keys()


# for each article compute the average of the n features relevant to the user (lowest_n)
def article_rating(features, skills):
    for skill in skills:
        vals = +eval(features)[skill]
    return vals / len(skills)


def best_article_rating(features, skills):
    return max([eval(features)[skill] for skill in skills])


def get_most_relevant(data, skills, topn=20):
    # based on the n lowest skills of the user, create a new column in the dataframe titled relevance
    data["relevance"] = data.apply(
        lambda x: best_article_rating(
            x["features"], get_lowest_skills(skills)
        ),
        axis=1,
    )
    # return the n most relevant articles
    data.iloc[0, data.columns.get_loc("relevance")] = 111

    return data.sort_values(by=["relevance"]).nlargest(topn, "relevance")


def recommend_articles(data, skills, topn=3):
    return get_most_relevant(data, skills).sample(n=topn)


@login_required
def save_to_board(request):
    if request.GET:
        id = request.GET["resource_id"]
    board = BuddyBoard.objects.filter(
        Q(buddy_1=request.user) | Q(buddy_2=request.user)
    ).first()
    content_id, created = ContentID.objects.get_or_create(value=id)
    board.buddy_content.add(content_id)

    return redirect("practice")


@login_required
def update_proficiency(request):
    if request.GET:
        topics = eval(request.GET["topics"])

    user = request.user
    for topic in topics:
        if topic == "Psychological Distress":
            user.practice.f_psychology += decimal.Decimal(0.1)
        elif topic == "Pre-Pregnancy":
            user.practice.f_prepregnancy += decimal.Decimal(0.1)
        elif topic == "Research":
            user.practice.f_research += decimal.Decimal(0.1)
        elif topic == "Retained Placenta":
            user.practice.f_placenta += decimal.Decimal(0.1)
        elif topic == "Administer Medication":
            user.practice.f_medication += decimal.Decimal(0.1)
        elif topic == "Fetal":
            user.practice.f_fetus += decimal.Decimal(0.1)
        elif topic == "Communication":
            user.practice.f_communication += decimal.Decimal(0.1)
        elif topic == "Assess Risks":
            user.practice.f_risks += decimal.Decimal(0.1)
        elif topic == "Breastfeeding":
            user.practice.f_breastfeed += decimal.Decimal(0.1)
        elif topic == "Post-Natal Complications: Bleeding":
            user.practice.f_bleeding += decimal.Decimal(0.1)
        elif topic == "Tool Knowledge":
            user.practice.f_tools += decimal.Decimal(0.1)

        user.practice.save()

    return redirect("practice")


@login_required
def practice(request):

    if not Practice.objects.filter(user=request.user).exists():
        return redirect("assessment")

    current_user = request.user
    practice = Practice.objects.filter(user=current_user)[0]
    skills = {
        "Psychological Distress": practice.f_psychology,
        "Pre-Pregnancy": practice.f_prepregnancy,
        "Research": practice.f_research,
        "Retained Placenta": practice.f_placenta,
        "Administer Medication": practice.f_medication,
        "Fetal": practice.f_fetus,
        "Communication": practice.f_communication,
        "Breastfeeding": practice.f_risks,
        "Assess Risks": practice.f_breastfeed,
        "Post-Natal Complications: Bleeding": practice.f_bleeding,
        "Tool Knowledge": practice.f_tools,
    }
    data = pd.read_csv("res/data.csv")
    data.columns = [
        "title",
        "url",
        "topics",
        "text",
        "features",
        "images",
    ]  # rename the columns for easier access
    data.dropna()  # ignore rows that contain NaN values
    df = get_most_relevant(data, skills)
    df["images"] = df["images"].replace(
        "[]",
        "['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-KQcs5WCy2Y5ZVeOuI1fcQnQBdhkuv4DrRKOSklirJ0pX7_vQ&s']",
    )
    endpoint = "https://ttp.mllp.upv.es/X5gon/lib/online_mt.php"
    items = []
    for index, row in df.iterrows():
        items.append(
            Item(
                title=row["title"],
                url=row["url"],
                topics=[
                    k for k, v in eval(row["features"]).items() if v > 0.1
                ],
                text=[paragraph for paragraph in row["text"].split("\n")],
                images=[
                    image
                    for image in row["images"]
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                    .split(",")
                    if image != "None"
                ][:1],
                id=index,
            )
        )

    skills_new = [
        ("Psychological Distress Management", practice.f_psychology),
        ("Providing Ante-Natal Care", practice.f_prepregnancy),
        ("Research Knowledge", practice.f_research),
        ("Treating Retained Placenta", practice.f_placenta),
        ("Administering Medication", practice.f_medication),
        ("Handling Fetal Risks", practice.f_fetus),
        ("Appropriate Communication", practice.f_communication),
        ("Risk Assessment", practice.f_risks),
        ("Advising New Mothers About Breastfeeding", practice.f_breastfeed),
        ("Treating Post-Natal Complications", practice.f_bleeding),
        ("Using Specialized Tools", practice.f_tools),
    ]

    skills_sorted = sorted(skills_new, key=lambda item: item[1])[:2]
    skills_worst = [Skill(skill[0], skill[1]) for skill in skills_sorted]

    x_data = [key for key, value in skills_new]
    y_data = [value for key, value in skills_new]
    plot_div = plot(
        [
            Bar(
                y=x_data,
                x=y_data,
                orientation="h",
                name="test",
                opacity=0.8,
                marker_color="pink",
            )
        ],
        output_type="div",
    )

    context = {"Items": items, "Skills": skills_worst, "Image": plot_div}

    return render(request, "users/practice.html", context)
