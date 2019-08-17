from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .forms import SignUpForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=False)
            # <process form cleaned data>
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            form.save()  # saves the form data
            # authenticates the user info
            user = authenticate(username=username, password=raw_password)
            user.set_password(raw_password)  # will set the password
            user.save()  # save the user in the user table
            # this will show an alert if the account is created succesfully
            messages.success(request, f'Account created for {username}')
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
        return render(request, self.template_name, {'form': form})
