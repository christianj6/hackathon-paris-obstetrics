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


# import plotly.graph_objs as go


class Item:
	def __init__(self, title, url, topics, text, images, id):
		self.title = title
		self.url = url
		self.topics = topics
		self.text = text
		self.images = images
		self.id = id

class Skill:
	def __init__(self, skill, value):
		self.skill = skill
		self.value = value


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, f'Welcome {username}. You are now able to log in.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})


# the lowest n skills of the user
def get_lowest_skills(skill_set, lowestn=2):
    return {k: v for k, v in sorted(skill_set.items(), key=lambda item: item[1])[:lowestn]}.keys()


# for each article compute the average of the n features relevant to the user (lowest_n)
def article_rating(features, skills):
    for skill in skills:
        vals = + eval(features)[skill]
    return vals / len(skills)

def best_article_rating(features, skills):
    return max([eval(features)[skill] for skill in skills])

def get_most_relevant(data, skills, topn=20):
    # based on the n lowest skills of the user, create a new column in the dataframe titled relevance
    data['relevance'] = data.apply(lambda x: best_article_rating(x['features'], get_lowest_skills(skills)), axis=1)
    # return the n most relevant articles
    data.iloc[0, data.columns.get_loc('relevance')] = 111

    return data.sort_values(by=['relevance']).nlargest(topn, 'relevance')

def recommend_articles(data, skills, topn=3):
    return get_most_relevant(data, skills).sample(n=topn) 

@login_required
def save_to_board(request):
	if request.GET:
		id = request.GET['resource_id']
	board = BuddyBoard.objects.filter(Q(buddy_1 = request.user) | Q(buddy_2 = request.user)).first()
	content_id, created = ContentID.objects.get_or_create(value = id)
	board.buddy_content.add(content_id)

	return redirect('practice')


@login_required
def update_proficiency(request):
	if request.GET:
		topics = eval(request.GET['topics'])

	user=request.user
	for topic in topics:
		if topic == 'Psychological Distress':
			user.practice.f_psychology += decimal.Decimal(0.1)
		elif topic == 'Pre-Pregnancy':
			user.practice.f_prepregnancy += decimal.Decimal(0.1)
		elif topic == 'Research':
			user.practice.f_research += decimal.Decimal(0.1)
		elif topic == 'Retained Placenta':
			user.practice.f_placenta += decimal.Decimal(0.1)
		elif topic == 'Administer Medication':
			user.practice.f_medication += decimal.Decimal(0.1)
		elif topic == 'Fetal':
			user.practice.f_fetus += decimal.Decimal(0.1)
		elif topic == 'Communication':
			user.practice.f_communication += decimal.Decimal(0.1)
		elif topic == 'Assess Risks':
			user.practice.f_risks += decimal.Decimal(0.1)
		elif topic == 'Breastfeeding':
			user.practice.f_breastfeed += decimal.Decimal(0.1)
		elif topic == 'Post-Natal Complications: Bleeding':
			user.practice.f_bleeding += decimal.Decimal(0.1)
		elif topic == 'Tool Knowledge':
			user.practice.f_tools += decimal.Decimal(0.1)

		
		user.practice.save()

	return redirect('practice')

		
@login_required
def practice(request):

	Practice.objects.get_or_create(user=request.user)

	current_user = request.user
	practice = Practice.objects.filter(user=current_user)[0]
	skills = {

		'Psychological Distress': practice.f_psychology,
		'Pre-Pregnancy': practice.f_prepregnancy,
		'Research': practice.f_research,
		'Retained Placenta': practice.f_placenta,
		'Administer Medication': practice.f_medication,
		'Fetal': practice.f_fetus,
		'Communication': practice.f_communication,
		'Breastfeeding': practice.f_risks,
		'Assess Risks': practice.f_breastfeed,
		'Post-Natal Complications: Bleeding': practice.f_bleeding,
		'Tool Knowledge': practice.f_tools,

	}

	# items = [k for k, v in skills.items()]

	data = pd.read_csv('data_04.csv')
	data.columns = ['title', 'url', 'topics', 'text', 'features', 'images'] # rename the columns for easier access
	data.dropna()  # ignore rows that contain NaN values
	# data['id'] = pd.factorize(data.url)[0]  # add a column with a unique id for each url
	
	df = get_most_relevant(data, skills)
	df['images'] = df['images'].replace('[]', '[\'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-KQcs5WCy2Y5ZVeOuI1fcQnQBdhkuv4DrRKOSklirJ0pX7_vQ&s\']')
	endpoint = "https://ttp.mllp.upv.es/X5gon/lib/online_mt.php"

	items = []
	for index, row in df.iterrows():
		items.append(Item(

			title=row['title'],
			url=row['url'],
			topics=[k for k, v in eval(row['features']).items() if v > 0.1],
			text=[paragraph for paragraph in row['text'].split('\n')],
			images=[image for image in row['images'].replace('[', '').replace(']', '').replace("'", "").split(',') if image != 'None'][:1],
			id=index
			))



	skills_new = [

		('Psychological Distress Management', practice.f_psychology),
		('Providing Ante-Natal Care', practice.f_prepregnancy),
		('Research Knowledge', practice.f_research),
		('Treating Retained Placenta', practice.f_placenta),
		('Administering Medication', practice.f_medication),
		('Handling Fetal Risks', practice.f_fetus),
		('Appropriate Communication', practice.f_communication),
		('Risk Assessment', practice.f_risks),
		('Advising New Mothers About Breastfeeding', practice.f_breastfeed),
		('Treating Post-Natal Complications', practice.f_bleeding),
		('Using Specialized Tools', practice.f_tools),

	]

	skills_sorted = sorted(skills_new, key=lambda item: item[1])[:2]
	skills_worst = [Skill(skill[0], skill[1]) for skill in skills_sorted]


# Bar(x=['food','service','environment'],y=[3.4,4.2,4.3])

	# layout = go.Layout(
	#     autosize=False,
	#     width=500,
	#     height=500,
	#     )

	x_data = [key for key, value in skills_new]
	y_data = [value for key, value in skills_new]
	plot_div = plot([Bar(y=x_data, x=y_data,
	                    # mode='lines',
	                    # width=800, 
	                    # height=400,
	                    # layout=layout,
	                    orientation='h',
	                    name='test',
	                    opacity=0.8, 
	                    marker_color='pink')],
	           output_type='div')


	context = {'Items': items, 'Skills': skills_worst, 'Image': plot_div}

	return render(request, 'users/practice.html', context)