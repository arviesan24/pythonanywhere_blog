from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post

class PostForm(forms.ModelForm): #create the form structure that will be used which connects to db (this one has 2 fields)
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]