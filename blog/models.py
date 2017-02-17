from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
	tag = models.CharField(max_length=50)
	create_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)

	class Meta:
		ordering = ['-create_time']

	def __str__(self):
		return self.tag	

	def get_articles(self):
		return Article.objects.filter(tags=self)

class Article(models.Model):
	PUBLISHED = 'P'
	DRAFT = 'D'
	STATUS = (
		(DRAFT,'Draft'),
		(PUBLISHED,'Published')
	)
	title = models.CharField(max_length=255)
	content = models.TextField(max_length=4000)
	markdown = models.TextField(max_length=4000,default='',null=True, blank=True)
	status = models.CharField(max_length=1,choices=STATUS)
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)


	user = models.ForeignKey(
		User,
		models.SET_NULL,
		blank=True,
		null=True
	)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-update_time']

	def create_tags(self, tags):
		tags_str = tags.strip()
		tags_list = tags_str.split(' ')
		for tag_str in tags_list:
			tag,created = Tag.objects.get_or_create(tag=tag_str.lower())
			self.tags.add(tag)

	def get_tags(self):
		return self.tags.all()
		
	def get_tags_str(self):
		tags = ''
		if self.get_tags:
			for tag in self.get_tags():
				tags = '{0} {1}'.format(tags, tag.tag)
			tags = tags.strip()
		return tags
	def get_comments(self):
		return Comment.objects.filter(article=self)



class Comment(models.Model):
	content = models.TextField(max_length=500)
	create_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User,models.SET_NULL,blank=True,null=True)
	article = models.ForeignKey(Article,models.SET_NULL,blank=True,null=True)

	class Meta:
		ordering = ['-create_time']

	def __str__(self):
		return self.content




class MyUser(User):
	class Meta:
		proxy = True

	def get_articles(self):
		return Article.objects.filter(user=self)
	def get_comments(self):
		return Comment.objects.filter(user=self)