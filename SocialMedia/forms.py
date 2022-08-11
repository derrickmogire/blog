from SocialMedia.models import *
from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm




class SocialForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': ' textarea border-muted rounded  ', 'cols': 50, 'rows': 5, 'autocomplete': 'off'}),

        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dob', 'dp')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image', )


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': ' textarea border-muted rounded  ', 'cols': 50, 'rows': 5, 'autocomplete': 'off'}),

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {

            'comment': Textarea(attrs={'class': 'form-control textarea border-muted rounded  ', 'cols': 50, 'rows': 3, 'autocomplete': 'off'}),

        }

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username",'password1','password2',)

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)        
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].help_text=''
        
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].help_text=''
        
        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].help_text=''