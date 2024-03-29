from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
from .models import RecommendedBuddies, InviteBuddy, BuddyBoard, ContentID
from users.models import Practice
import pandas as pd


user = get_user_model()


class Item:
    def __init__(self, title, url, topics, text, images, id):
        self.title = title
        self.url = url
        self.topics = topics
        self.text = text
        self.images = images
        self.id = id


def recommended_buddies_view(request):
    board = BuddyBoard.objects.filter(
        Q(buddy_1=request.user) | Q(buddy_2=request.user)
    )
    if board.exists():
        return redirect("buddy-board")

    p = RecommendedBuddies.objects.filter(user=request.user).first()
    users = user.objects.exclude(username=request.user.username)
    u = request.user
    sent_invites = InviteBuddy.objects.filter(from_user=request.user)
    rec_invites = InviteBuddy.objects.filter(to_user=request.user)
    # is this user our friend
    button_status = "not_friend"

    context = {
        "u": u,
        "button_status": button_status,
        "rec_buddy_list": users,
        "sent_friend_requests": sent_invites,
        "rec_friend_requests": rec_invites,
    }

    return render(request, "buddy/home.html", context)


def send_buddy_request(request):
    if request.GET:
        username = request.GET["username"]

    user = get_object_or_404(User, username=username)
    frequest, created = InviteBuddy.objects.get_or_create(
        from_user=request.user, to_user=user
    )

    return redirect("buddy-home")


def delete_buddy_request(request):
    if request.GET:
        username = request.GET["username"]

    from_user = get_object_or_404(User, username=request.user)
    to_user = get_object_or_404(User, username=username)
    frequest = InviteBuddy.objects.filter(
        from_user=from_user, to_user=to_user
    ).first()
    frequest.delete()
    return redirect("buddy-home")


def ignore_buddy_request(request):
    if request.GET:
        username = request.GET["username"]

    from_user = get_object_or_404(User, username=username)
    to_user = get_object_or_404(User, username=request.user)
    frequest = InviteBuddy.objects.filter(
        from_user=from_user, to_user=to_user
    ).first()
    frequest.delete()
    return redirect("buddy-home")


def accept_buddy_request(request):
    # accepts the buddy username
    # creates a new board object pairing the new users
    # redirects to the board page
    # shows the content from the board
    # board parses and shows content from both users just like before
    if request.GET:
        username = request.GET["username"]

    other_user = get_object_or_404(User, username=username)
    current_user = request.user
    buddy_board, created = BuddyBoard.objects.get_or_create(
        buddy_1=current_user, buddy_2=other_user
    )
    sent_invites_other = InviteBuddy.objects.filter(from_user=other_user)
    sent_invites_current = InviteBuddy.objects.filter(from_user=current_user)
    sent_invites_other.delete()
    sent_invites_current.delete()

    return redirect("buddy-board")


def buddy_board_view(request):
    # parse the content of the buddy board and display it like previously
    # we'll need to get the IDs from the csv

    board = BuddyBoard.objects.filter(
        Q(buddy_1=request.user) | Q(buddy_2=request.user)
    ).first()

    content = []
    for ids in board.buddy_content.all():
        content.append(ids.value)
    practice_buddy1 = Practice.objects.get(user=board.buddy_1)
    practice_buddy2 = Practice.objects.get(user=board.buddy_2)
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

    df = data.iloc[content]
    df["images"] = df["images"].replace(
        "[]",
        "['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-KQcs5WCy2Y5ZVeOuI1fcQnQBdhkuv4DrRKOSklirJ0pX7_vQ&s']",
    )
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

    context = {"Items": items}

    return render(request, "buddy/board.html", context)
