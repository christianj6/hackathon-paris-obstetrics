from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import RecommendedBuddies, InviteBuddy
# from django.views.generic import CreateView



user = get_user_model()

def create_recommended_buddies(request):
	pass

def send_buddy_request(request):
	# group = Group.objects.get(pk=pk)
 #    group.status = Status.approved
 #    group.save()
	if request.GET:
		username = request.GET['username']

	# if request.user.is_authenticated():
	user = get_object_or_404(User, username=username)
	frequest, created = InviteBuddy.objects.get_or_create(
		from_user=request.user,
		to_user=user)

	return redirect('buddy-home')






	# return HttpResponseRedirect(request, 'buddy/home.html')


def delete_buddy_request(request, username):
	from_user = get_object_or_404(User, username=username)
	frequest = InviteBuddy.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

def accept_buddy_request(request, username):
	from_user = get_object_or_404(User, username=username)
	frequest = InviteBuddy.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.RecommendedBuddies.suggested_buddies.add(user2.RecommendedBuddies)
	user2.RecommendedBuddies.suggested_buddies.add(user1.RecommendedBuddies)
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.RecommendedBuddies.slug))



def recommended_buddies_view(request):
	# p, created = RecommendedBuddies.objects.get_or_create(user=request.user)

	p = RecommendedBuddies.objects.filter(user=request.user).first()

	users = user.objects.exclude(username=request.user.username)
	# TODO: Add more logic to filter users based on current user's skills.

	u = request.user
	# u = p.user
	sent_invites = InviteBuddy.objects.filter(from_user=request.user)
	rec_invites = InviteBuddy.objects.filter(to_user=request.user)

	# users = p.suggested_buddies.all()

	# is this user our friend
	button_status = 'not_friend'
	# if p not in request.user.RecommendedBuddies.suggested_buddies.all():
	# 	button_status = 'not_friend'

	# 	# if we have sent him a friend request
	# 	if len(FriendRequest.objects.filter(
	# 		from_user=request.user).filter(to_user=p.user)) == 1:
	# 			button_status = 'friend_request_sent'

	context = {
		'u': u,
		'button_status': button_status,
		'rec_buddy_list': users,
		'sent_friend_requests': sent_invites,
		'rec_friend_requests': rec_invites
	}

	return render(request, 'buddy/home.html', context)

# def get_recommended_buddies(request):
# 	users = User.objects.exclude(request.user)




# def board(request)
	# we need to create this object upon pairing with a user
	

# 	# this parses the content from the board model
# 	return render(request, 'buddy/board.html', )