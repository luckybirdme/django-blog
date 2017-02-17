from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.conf import settings
from django.db.models import Count


import datetime
import uuid
import os

from form import ArticleForm,CommentForm
from models import Article,Tag,Comment,MyUser

# Create your views here.
def home(request):
	articles = Article.objects.filter(status=Article.PUBLISHED)
	title = 'Home'

	return base(request,articles,title)

def base(request,articles_list,title):
	paginator = Paginator(articles_list, 10) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		articles = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		articles = paginator.page(paginator.num_pages)
	tags = Tag.objects.all()
	return render(request, 'blog/home.html',{'articles':articles,'title':title,'tags':tags})

def show(request,id):
	article = get_object_or_404(Article,id=id)
	title = 'Show'
	form = CommentForm(initial={'article_id':article.id})

	return render(request, 'blog/show.html',{'article':article,'title':title,'form':form})

def user(request,username):
	user = User.objects.filter(username=username)
	articles = Article.objects.filter(status=Article.PUBLISHED,user=user)
	title = username
	return base(request,articles,title)

def tag(request,tag):
	tags = Tag.objects.filter(tag=tag)
	articles = Article.objects.filter(status=Article.PUBLISHED,tags=tags)
	title = tag
	return base(request,articles,title)

def search(request):
	q = request.GET.get('q')
	articles = Article.objects.filter(status=Article.PUBLISHED,title__contains=q)
	title = 'Search'
	return base(request,articles,title)


def alltag(request):
	tags = Tag.objects.annotate(num_articles=Count('article')).order_by('-create_time').order_by('-num_articles')
	title = 'Alltag'
	return render(request, 'blog/alltag.html',{'tags':tags,'title':title})

def alluser(request):
	users = MyUser.objects.annotate(num_articles=Count('article'),num_comments=Count('comment')).order_by('-num_comments').order_by('-num_articles')
	title = 'Alluser'
	return render(request, 'blog/alluser.html',{'users':users,'title':title})

@login_required
def draft(request):
	articles = Article.objects.filter(status=Article.DRAFT,user=request.user)
	title = 'Draft'
	return base(request,articles,title)

@login_required
def upload(request):
	files = request.FILES['upload']
	date = datetime.datetime.now().strftime("%Y%m%d")
	name = '%s%s' % (uuid.uuid1(),'.png')
	
	dirpath = '%s/%s/' % (settings.UPLOAD_PATH,date)
	fullname = '%s/%s' % (dirpath,name)
	fullurl = '/%s/%s/%s' % (settings.UPLOAD_URL,date,name)

	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

	with open(fullname, 'wb+') as destination:
		for chunk in files.chunks():
			destination.write(chunk)

	return HttpResponse(fullurl)

@login_required
def comment(request):
	form = CommentForm(request.POST)

	if form.is_valid():
		comment = Comment()
		comment.content = form.cleaned_data.get('content')
		comment.user = request.user
		id=form.cleaned_data.get('article_id')
		try:
			article = Article.objects.get(id=id)
			comment.article = article
			comment.save()
			article.save()
			rtn = {'status':True,'redirect':reverse('blog:show', args=[id])}
		except Article.DoesNotExist:
			rtn = {'status':False,'error':'Article is not exist'}
	else:
		rtn = {'status':False,'error':form.errors}

	return JsonResponse(rtn)

@login_required
def write(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			id = form.cleaned_data.get('id')
			try:
				article = Article.objects.get(id=id)
			except Article.DoesNotExist:
				article = Article()
			article.user = request.user
			article.title = form.cleaned_data.get('title')
			article.content = form.cleaned_data.get('content')
			article.status = form.cleaned_data.get('status')
			article.markdown = form.cleaned_data.get('markdown')
			article.save()
			tags = form.cleaned_data.get('tags')
			article.create_tags(tags)
			return redirect(reverse('blog:home'))
		else:
			return HttpResponse(form.errors.as_json());
			
	elif request.GET.get('id'):
		id = request.GET.get('id')
		article = Article.objects.get(id=id)
		tags = article.get_tags_str()
		form = ArticleForm(instance=article,initial={'tags': tags})

	else:
		form = ArticleForm()
	
	return render(request, 'blog/write.html', {'form':form})