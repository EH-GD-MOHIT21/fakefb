from typing import MutableSequence
from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect, render,HttpResponse
from hksfbclone.models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
from datetime import timezone
import smtplib
import datetime
from email.message import EmailMessage
from random import choice
from django.conf import settings


# Create your views here.
def hlo(request):
    if request.user.is_authenticated:
        posts=reversed(item.objects.all())
        dsd=comment.objects.all()
        return render(request,'comm.html',{'psts':posts,'co':dsd})
    else:
        hk=0
        return render(request,'Signup.html',{'hkss':hk})


def generate_random_unicode():
        # logic to generate code
        varsptoken = ''
        alphas = ['-', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(26):
            alphas.append(chr(65+i))
            alphas.append(chr(97+i))
        for i in range(89):
            varsptoken += choice(alphas)

        return varsptoken

def send_mail(to, personalcode):
        # logic to send mail to user
    sender_mail = f"{settings.MAIL_SENDER}"
    password_sender = f"{settings.PASS_MAIL}"
    message = EmailMessage()
    message['To'] = to
    message['From'] = sender_mail
    message['Subject'] = "Welcome to Fb Clone"
    message.set_content(
        f"Hello User welcome to FbClone.com Your one time login link is\n {settings.SITE_URL}/verify/{personalcode} \nvalid for next 15 minutes.")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_mail, password_sender)
        server.send_message(message)
        return True         # success 
    except:
        return False   



def signup(request):
    if request.method=='POST':
        first_name=request.POST['f_name']
        last_name=request.POST['l_name']
        username=request.POST['u_name']
        email=request.POST['mmail']
        passw=request.POST['pass']
        passw1=request.POST['pass1']

        if passw==passw1:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exist')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already exist')
                return redirect('/signup')
            else:
                personalcode = generate_random_unicode()
                mytimecalculator = 0
                while(len(profile_details.objects.filter(unicode=personalcode))):
                    personalcode = generate_random_unicode()
                    mytimecalculator += 1
                    if mytimecalculator > 10000:
                # render(request,'logshower.html',{'formid': 'sorry but we are unable to process your request'})
                        pass 

                status = send_mail(email, personalcode)
                user=User.objects.create_user(username=username, password=passw, email=email, first_name=first_name,last_name=last_name)
                user.save();
                hkk=1
                upes = profile_details(user=user, terimail=email,u_nm= username,fstname=first_name,secname=last_name,
                            unicode=personalcode, timestamp=datetime.datetime.now(timezone.utc))
                upes.save()
                messages.info(request,'Confirmation link sent to your mail')
                return render(request,'Signup.html',{'hkss':hkk})
        else:
            messages.info(request,'Password not matching')
            return redirect('/signup')
    else:
        return render(request,'Signup.html')


def login(request):
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['upss'] 

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            datas = profile_details.objects.filter(user=user)
            for data in datas:
                if not data.verified:
                    messages.error(request,'User Not Verified Yet...')
                    return render(request, 'Signup.html')
            auth.login(request,user)
            posts=reversed(item.objects.all()) 
            return redirect('/')
        else:
            hksss=1
            messages.info(request,'invalid credentials')
            return render(request,'Signup.html',{'hkss':hksss})
    else:
        return render(request,'Signup.html')




def cmm(request):
    posts=reversed(item.objects.all())
    dsd=comment.objects.all()
    return render(request,'comm.html',{'psts':posts,'co':dsd})

def shsgn(request):
    hk=0
    return render(request,'Signup.html', {'hkss':hk})

def shlgn(request):
    hk=1
    return render(request,'Signup.html', {'hkss':hk})

def createpost(request):
    if request.user.is_authenticated:
        tm=datetime.datetime.now().strftime('%Y-%m-%d ,%H:%M')
        return render(request,'createpost.html',{'times':tm})
    hk=0
    return redirect('/',{'hkss':hk})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        hk=0
        return redirect('/',{'hkss':hk})
    messages.info(request,'Need to login first')
    return render(request,'Signup.html')


def addpost(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            pos=item()
            pos.username=request.user.username
            pos.time_creat=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            pos.about=request.POST.get('aboutde')
            if len(request.FILES)!=0:
                pos.img=request.FILES['imgle']
            
            dkc=profile_details.objects.get(u_nm=request.user.username)
            pos.author=request.user
            dff=dkc.id
            pos.profile=dkc
            pos.save();
            posts=reversed(item.objects.all())
            return render(request,'comm.html',{'psts':posts})

        return render(request,'createpost.html')
    return render(request,'Signup.html') 


def addcomment(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            dd=request.POST.get('idele')
            ac=comment()
            ac.pst=item.objects.filter(id=dd)[0]
            ac.nam=request.user.username
            ac.body=request.POST.get('hereis')
            ac.save();
            posts=reversed(item.objects.all())
            return render(request,'comm.html',{'psts':posts})
    messages.info(request,'Need to login First')
    return render(request,'Signup.html')  


def uposts(request):
    if request.user.is_authenticated:
        posts=reversed(item.objects.filter(username=request.user.username))
        l=len(item.objects.filter(username=request.user.username))
        dxx=1
        return render(request,'comm.html',{'psts':posts, 'le':dxx, 'lnt':l}) 
    return render(request,'Signup.html')


def delepost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            dde=request.POST.get('idele')
            item.objects.filter(id=dde).delete()
            comment.objects.filter(pst=dde).delete()
            posts=reversed(item.objects.filter(username=request.user.username))
            l=len(item.objects.filter(username=request.user.username))
            dxx=1
            return render(request,'comm.html',{'psts':posts, 'le':dxx, 'lnt':l})
    return render(request,'Signup.html') 


def delecomm(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            ddex=request.POST.get('idele') 
            comment.objects.filter(id=ddex).delete()
            posts=reversed(item.objects.all()) 
            return render(request,'comm.html',{'psts':posts})
    return render(request,'Signup.html')
            

def verify(request, pid):
    return render(request, 'verify.html', {'pid': pid})  


def updateuser(request,pid):
    if request.method == 'POST':
        username = request.POST['unamm']
        me = profile_details.objects.filter(unicode=pid)
        puser = User.objects.filter(username=username)
        if len(me) != 1 or len(puser) != 1:
            return HttpResponse({'user not exists'})
        for person in me:
            if person.verified == 0:
                # match timestamp code here
                cur_time = datetime.datetime.now(timezone.utc)
                pre_time = person.timestamp
                del_time = str(cur_time-pre_time)
                del_time = del_time.split(':')
                if del_time[0] != '0':
                    # delete entry from database
                    profile_details.objects.filter(
                        unicode=pid).delete()
                    User.objects.filter(username=username).delete()
                    return HttpResponse({'Time Limit Exceed'})
                elif int(del_time[1]) > 14:     # 15 minutes time
                    # delete entry from database
                    profile_details.objects.filter(
                        unicode=pid).delete()
                    User.objects.filter(username=username).delete()
                    return HttpResponse({'Time limit Excced'})
                person.verified = 1
                person.unicode = None
                person.save()
                return HttpResponse({'success'})
            else:
                return HttpResponse({'Already Verified.'})
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        return HttpResponse({'user is not authenticated.'})


def likechange(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            dd=request.POST.get('idele')
            post=item.objects.get(id=dd)
            user=request.user
            if user in post.liked.all():
                post.liked.remove(user)
            else:
                post.liked.add(user)

            like,created=likes.objects.get_or_create(user=user,post=post)
            if not created:
                if like.value=='Like':
                    like.value=='Unlike'
                else:
                    like.value=='Like'

            like.save()
            return redirect('/')
    messages.info(request,'Need to login first')
    return render(request,'Signup.html')
            
def yourprofile(request):
    if request.user.is_authenticated:
        psd=profile_details.objects.filter(u_nm=request.user.username)
        return render(request,'profile.html',{'prfde':psd})
    return render(request,'Signup.html')

def saveupdate(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            dsdd=profile_details.objects.get(u_nm=request.user.username)
            if len(request.FILES)!=0:
                if len(dsdd.imgp)>0:
                    os.remove(dsdd.imgp.path)
                dsdd.imgp=request.FILES['imgle']
            dsdd.fstname=request.POST.get('f_name')
            dsdd.secname=request.POST.get('l_name')
            dsdd.fbacc=request.POST.get('mmail')
            dsdd.save()
            return redirect('/showprofile')
    return redirect('/')


