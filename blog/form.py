from django import forms

from models import Article,Comment


class ArticleForm(forms.ModelForm):
	title = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		max_length=255,
		required=True)
	tags = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		max_length=255, 
		required=False,
		help_text='Use spaces to separate the tags, such as "java php c"')

	status = forms.ChoiceField(
		widget=forms.Select(attrs={'class': 'form-control'}),
		choices = Article.STATUS, 
		initial=Article.DRAFT,
		required=True)
	id = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	markdown = forms.CharField(
		widget=forms.Textarea(attrs={'class': 'form-control'}),
		max_length=4000,
		required=True,
		label='Content')
	content = forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model = Article
		fields = ['id','title','tags','status', 'markdown','content']

class CommentForm(forms.Form):
	content = forms.CharField(
		label='Comment',
		widget=forms.Textarea(attrs={'class': 'form-control','rows':3}),
		max_length=500,
		required=True
		)
	article_id = forms.IntegerField(widget=forms.HiddenInput(),required=True)










