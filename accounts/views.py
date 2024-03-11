from django.shortcuts import render, redirect
from .forms import SignupForm, UserActivateForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail


# Create your views here.
def signup(request):
    '''
        - create new user
        - send email: code
        - redirect: activate
    '''
    if user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            user = form.save(commit=False)
            user.is_active = False

            form.save() # trigger signal --> create profile: code

            profile = Profile.objects.get(user__username=username)

            # Send email to user for activation
            send_mail(
                "Activate Your Account",
                f"Welcome {username}\nUse this code {profile.code} to activate your account.",
                "ismekbektop@gmail.com",
                [email],
                fail_silently=False,
            )
            return redirect('account_activate', username=username)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_activate(request, username):
    '''
        - code ----> activate
        - redirect: login
    '''
    profile = Profile.objects.get(user__username=username)
    if request.method == 'POST':
        form = UserActivateForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if code == profile.code:
                profile.code = ''
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
                profile.save()

                return redirect('account_login')
    else:
        form = UserActivateForm()
    return render(request, 'accounts/activate.html', {'form': form})
