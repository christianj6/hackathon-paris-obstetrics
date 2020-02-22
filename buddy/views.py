from django.shortcuts import render
from django.http import HttpResponse


def buddy(request):
	# return HttpResponse('<h1>Buddy Page</h1>')
	return render(request, 'buddy/home.html')