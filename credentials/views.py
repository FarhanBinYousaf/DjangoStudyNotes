from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate,login,logout
from datetime import date
from .models import Notes, Profile
from .form import CustomCreationForm,ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'credentials/home.html')
def register(request):
    msg = ""
    error_msg = ""
    pass_error = ""
    subject = 'Welcome to the Notes Sharing Site.'
    message = 'We are glad you are here'

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uemail = request.POST['email']
        ucontact = request.POST['contact']
        upassword = request.POST['password']
        uCPass = request.POST['cpass']
        ubranch = request.POST['branch']
        urole = request.POST['role']
        if upassword == uCPass:
            try:
                user = User.objects.create_user(username=uemail,password=upassword,first_name=fname,last_name=lname)
                Profile.objects.create(user=user,contact=ucontact,branch=ubranch,role=urole)
                msg = "Account Created Successfully"
                send_mail(subject,message,settings.EMAIL_HOST_USER,[uemail],
                    fail_silently=False)
                return redirect('login')
                
            except:
                error_msg = "something went wrong"
        else:
            pass_error = "Password do not match"

    context = {'msg':msg,'error_msg':error_msg,'pass_error':pass_error}
    return render(request,'credentials/register.html',context)

def UserLogin(request):
    msg = ""
    error_msg = ""
    if request.method == "POST":
        uemail = request.POST['email']
        upass = request.POST['pwd']
        try:
            user = User.objects.get(username=uemail)
        except:
            msg = "Username does not exist"

        user = authenticate(request,username=uemail,password= upass)

        if user is not None and user.is_superuser==False:
            login(request,user)
            return redirect('home')
        else:
            error_msg = "Invalid Credentials"
    context = {'msg':msg,'error_msg':error_msg}
    return render(request,'credentials/login.html',context)

def userLogout(request):
    logout(request)
    return redirect('login')
def adminHome(request):

    pendingNotes = Notes.objects.filter(status="pending").count()
    acceptedNotes = Notes.objects.filter(status="Accept").count()
    rejectedNotes = Notes.objects.filter(status="Reject").count()
    allNotes = Notes.objects.all().count()
    context = {'pendingNotes':pendingNotes,'acceptedNotes':acceptedNotes,'rejectedNotes':rejectedNotes,'allNotes':allNotes}
    return render(request,'credentials/admin_index.html',context)
def adminLogin(request):
    error_msg =""
    if request.method == "POST":
        admin_name = request.POST['adminName']
        admin_pwd = request.POST['adminPwd']
        admin = authenticate(request,username=admin_name,password= admin_pwd)
        if admin.is_staff:
            login(request,admin)
            return redirect('admin_home')
        else:
            error_msg = "Invalid Credentials"
    context = {'error_msg':error_msg}
    return render(request,'credentials/admin_login.html',context)

@login_required(login_url='login')
def userProfile(request):
    
    if request.user.is_superuser==True:
        print("No")
    else:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
    context = {'user':user,'profile':profile}
    return render(request,'credentials/user_profile.html',context)

@login_required(login_url='login')
def editProfile(request):
    msg = ""
    msg1 = ""
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        new_f_name = request.POST['new_f_name']
        new_l_name = request.POST['new_l_name']
        new_mail = request.POST['new_mail']
        new_contact = request.POST['new_contact']
        new_branch = request.POST['new_branch']

        user.first_name = new_f_name
        user.last_name = new_l_name
        user.email = new_mail
        profile.contact = new_contact
        profile.branch = new_branch
        user.save()
        profile.save()
        msg  = True
        if msg!=True:
            msg1 = False
    context = {'user':user,'profile':profile,'msg':msg}
    return render(request,'credentials/edit_profile.html',context)

def change_pass(request):
    error_msg = ""
    if request.method == "POST":
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confim_pass']
        if new_pass == confirm_pass:
            user = User.objects.get(username__exact=request.user.username)
            user.set_password(new_pass)
            user.save()
            return redirect('login')
        else:
            error_msg = "Invalid Credentials"
    context = {'error_msg':error_msg}
    return render(request,'credentials/change_password.html',context)

@login_required(login_url='login')
def uploadNotes(request):
    msg = ""
    error_msg = ""
    if request.method == "POST":
        branch = request.POST['branch']
        subject = request.POST['subject']
        notesFile = request.FILES['notesfile']
        fileType = request.POST['filetype']
        desc = request.POST['description']
        current_user = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=current_user,uploadingDate=date.today(),branch=branch,subject=subject,notesFile=notesFile,fileType=fileType,description=desc,status="pending")
            msg = True
            return redirect('view_my_notes')
        except:
            error_msg = False
    context = {'msg':msg,'error_msg':error_msg}
    return render(request,'credentials/upload_notes.html',context)

@login_required(login_url='login')
def viewMyNotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Notes.objects.filter(user=user)
    context = {'data':data}
    return render(request,'credentials/view_my_notes.html',context)

def deleteNotes(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pk)
    notes.delete()
    return redirect('view_my_notes')
    return render(request,'credentials/delete_notes.html')

@login_required(login_url='login')
def viewAllNotes(request):
    data = Notes.objects.all()
    context = {'data':data}
    return render(request,'credentials/view_all_notes.html',context)


# Admin Section Starts Here
@login_required(login_url='adminLogin')
def view_users(request):
    users = Profile.objects.all()
    context = {'users':users}
    return render(request,'credentials/view_users.html',context)

def deleteUsers(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('view_users')
    return render(request,'credentials/delete_user.html')

def pendingNotes(request):
    data = Notes.objects.filter(status="pending")
    context = {'data':data}
    return render(request,'credentials/pending_notes.html',context)

def acceptedNotes(request):
    data = Notes.objects.filter(status="Accept")
    context = {'data':data}
    return render(request,'credentials/accepted_notes.html',context)

def rejectedNotes(request):
    data = Notes.objects.filter(status="Reject")
    context = {'data':data}
    return render(request,'credentials/rejected_notes.html',context)

def assignStatus(request,pk):
    msg = ""
    error_msg = ""
    notes = Notes.objects.get(id=pk)
    if request.method == "POST":
        status = request.POST['status']
        try:
            notes.status = status
            notes.save()
            msg = "Updated Successfully"
            return redirect('all_notes')
        except:
            error_msg = "something went wrong "
    context = {'notes':notes,'msg':msg,'error_msg':error_msg}
    return render(request,'credentials/assign_status.html',context)


def allNotes(request):
    data = Notes.objects.all()
    context = {'data':data}
    return render(request,'credentials/all_notes.html',context)