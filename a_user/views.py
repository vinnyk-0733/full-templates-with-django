from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import logout
from .form import *

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    try:
        profile = request.user.profile
    except:
        return redirect('account_login')
    return render(request,'a_user/profile.html',{'profile':profile})

@login_required
def profile_edit_view(request):
    form  = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile_onboarding'):
        onboarding = True
    else:
        onboarding  = False
    return render(request,'a_user/profile_edit.html',{'form':form,'onboarding':onboarding})

@login_required
def profile_setting_view(request):
    return render(request,'a_user/profile_setting.html')


@login_required
def profile_emailchange(request):

    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            email = form.cleaned_data['email']

            # check duplicates
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile_setting')

            # save new email on User
            form.save()

            # get or create EmailAddress record
            email_address, created = EmailAddress.objects.get_or_create(
                user=request.user,
                email=email,
                defaults={"verified": False, "primary": True},
            )

            if not created:
                email_address.verified = False
                email_address.save()

            # ✅ send confirmation using the EmailAddress instance
            email_address.send_confirmation(request)

            messages.success(request, f"Confirmation email sent to {email}.")
            return redirect('profile_setting')
        else:
            messages.warning(request, 'Form not valid.')
            return redirect('profile_setting')

    return redirect('home')

@login_required
def profile_emailverify(request):
    try:
        email_address = EmailAddress.objects.get(user=request.user, primary=True)
    except EmailAddress.DoesNotExist:
        messages.error(request, "No primary email found for this account.")
        return redirect('profile_setting')

    # Send the confirmation email
    email_address.send_confirmation(request)

    messages.success(request, f"Verification email sent to {email_address.email}.")
    return redirect('profile_setting')

@login_required
def profile_delete_view(request):
    user= request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request,'Account deleted')
        return redirect('home')
    return render(request,'a_user/profile_delete.html')