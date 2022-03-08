from .models import Message, Profile, Skill
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name':'Name',
        }
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ 'name','username','email','profile_image','short_intro','bio', 'location',
                  'social_github','social_twitter','social_youtube','social_linkedin','social_website']
        
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
    
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text', 'placeholder':'Enter value'})

