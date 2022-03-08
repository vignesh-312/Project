from email import message
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    userobj = instance
    if created:
        profile = Profile.objects.create(
            user = userobj,
            name = userobj.username,
            username = userobj.username,
            email = userobj.email
        )
        print('Profile also created for this user')
        
        subject = "welcome to Developer's Web Application"
        message = "We are glad you are here"
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

@receiver(post_delete,sender=Profile)
def deleteUser(sender,instance,**kwargs):
    profile = instance
    userobj = profile.user
    userobj.delete()
    print('User also deleted')

def updateUser(sender,instance, created, **kwargs):
    if created == False:
        profile = instance
        user = profile.user.profile
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()
        print('User record updated')

post_save.connect(updateUser, sender=Profile)
post_save.connect(createProfile, sender=User)
#post_delete.connect(deleteUser, sender=Profile)