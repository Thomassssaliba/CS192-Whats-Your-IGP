# MIT License

# Copyright (c) Justin James Gonzales, Thomas Martin Saliba, Brent Zaguirre

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# “This is a course requirement for CS 192 Software Engineering II under the supervision of 
# Asst. Prof. Ma. Rowena C. Solamo of the Department of Computer Science, College of Engineering, 
# University of the Philippines, Diliman for the AY 2015-2016”.

# =================================================================================

# CODE HISTORY:
# <1/26/2019>
# 1) Code initialization
# 2) License
# 3) Main Functionality (Backend):
#   a.  url calls

# ---------------------------------------------------------------------------------

# <2/08/2019>
# 1)  Creation Date
# 2)  Development Group
# 3)  Client Group
# 4)  Purpose
# 5)  Methods

# =================================================================================   

# Creation Date: <1/26/2019>

# =================================================================================

# Development Group: What's Your IGP

# =================================================================================

# Client Group: What's Your IGP

# =================================================================================

# Purpose:
# > The purpose of the project: "What's Your IGP," is for the fufillment of the course: "CS 192." The project
# aims to centralize the Income Generated Projects (IGP's) online information of all existing organizations
# associated with UP Diliman. It's objective is to offer convenience for both sellers and customers of IGP
# to sell and gather information online.  

# =================================================================================

from django.shortcuts import render
from django.views.generic import (
     ListView,
     DetailView,
     CreateView,
     UpdateView,
     DeleteView
     )
from .models import IGP, ORG
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
#Method name: signup
#Creation Date: February 18,2019
#Purpose of routine: Signup a user that is not yet registered
#Calling arguments: request
#Required Files/Database table: forms.py,signup.html and models.py,home.html
#Return value: user information saved.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            if(form.cleaned_data.get('user_type')!="select2"):
                 user.profile.user_type = "Seller"
            user.profile.college= form.cleaned_data.get('college')
            user.profile.mobile_number = form.cleaned_data.get('mobile_number')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('app-home')                 
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})
#Method name: memsignup
#Creation Date: February 18,2019
#Purpose of routine: Calls a form after signing up as a seller for additional org info
#Calling arguments: request
#Required Files/Database table: forms.py,memsignup.html and models.py
#Return value: orgmember information saved.
def memsignup(request):
    if request.method == 'POST':
               form = Orgform(request.POST)
               if form.is_valid():
                 user = form.save()
                 user.refresh_from_db()  # load the profile instance created by the signal
                 user.profile.org=form.cleaned_data.get('org_name')
                 user.profile.location=form.cleaned_data.get('location')
                 user.save()
                 raw_password = form.cleaned_data.get('password1')
                 user = authenticate(username=user.username, password=raw_password)
                 login(request, user)
                 return redirect('app-home')
    else:
                         form=Orgform()
    return render(request, 'app/memsignup.html', {'form': form})
#Method name: profile
#Creation Date: February 18,2019
#Purpose of routine: renders the template for profile of a buyer
#Calling arguments: request
#Required Files/Database table: buyer_profile.html and models.py
#Return value: Display profile information of user
def profile(request):
     return render(request,'app/buyer_profile.html')
#Method name: list_igp
#Creation Date: February 18,2019
#Purpose of routine: renders the template for list of igp of a buyer
#Calling arguments: request
#Required Files/Database table: buyer_igp.html and models.py
#Return value: Displays list of available igp
def list_igp(request):
     context = {
          'orgs': ORG.objects.all(),
          'igps': IGP.objects.all(),
     }
     return render(request,'app/buyer_igp.html', context)
#Method name: list_org
#Creation Date: February 18,2019
#Purpose of routine: renders the template for list of org of a buyer
#Calling arguments: request
#Required Files/Database table: buyer_igp.html and models.py
#Return value: Displays list of available org
def list_org(request):
     context = {
          'orgs': ORG.objects.all(),
     }
     return render(request,'app/buyer_org.html', context)

#Method name: home
#Creation Date: 
#Purpose of routine: renders the template for home for a user
#Calling arguments: request
#Required Files/Database table: buyer_home.html,home.html and models.py
#Return value: Displays home depending on the user type.
@login_required(login_url='login')
def home(request):
     user = User.objects.get(username=request.user)
     if(user.profile.user_type=="Buyer"):
          return render(request,'app/buyer_home.html')
     else:
          return render(request,'app/home.html')     
     context = {
          'page': ''
     }
     return render(request, 'app/home.html', context)

#Method name: orgs
#Creation Date: 
#Purpose of routine: renders the template for list of orgs for a seller
#Calling arguments: request
#Required Files/Database table: org.html and models.py
#Return value: Displays list of registered orgs
def orgs(request):
     context = {
          'orgs': ORG.objects.all(),
          'page': 'ORGS'
     }
     return render(request, 'app/org.html', context)

def orgigps(request):
     context = {
          'orgs': ORG.objects.all(),
          'igps': IGP.objects.all(),
          'page': org.name
     }
     return render(request, 'app/orgigps.html', context)

class IGPListView(ListView):
     model = IGP
     template_name = 'app/igp.html'
     context_object_name = 'igp'
     ordering = ['-date_posted']

class IGPCreateView(LoginRequiredMixin, CreateView):
     model = IGP
     fields = ['item', 'org', 'itype', 'price']
     success_url ='/app/igps/'

class IGPDeleteView(LoginRequiredMixin, DeleteView):
     model = IGP
     success_url ='/app/igps/'

class IGPUpdateView(LoginRequiredMixin, UpdateView):
     model = IGP
     fields = ['item', 'org', 'itype', 'price']
     success_url ='/app/igps/'

class ORGListView(ListView):
     model = ORG
     template_name = 'app/org.html'
     context_object_name = 'orgs'
     ordering = ['name']

class ORGDetailView(DetailView):
     model = ORG
     orgId = model.id
     template_name = 'app/orgigps_detail.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['org_igps']=IGP.objects.filter(org_id=self.object.id)
          return context
          
class ORGCreateView(LoginRequiredMixin, CreateView):
     model = ORG
     fields = ['name', 'desc']

class ORGUpdateView(LoginRequiredMixin, UpdateView):
     model = ORG
     fields = ['name', 'desc']

class ORGDeleteView(LoginRequiredMixin, DeleteView):
     model = ORG
     success_url ='/app/orgs/'

class BuyerIGP(DetailView):
     model = ORG
     orgId = model.id
     template_name = 'app/buyer_orgigps_detail.html'
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['org_igps']=IGP.objects.filter(org_id=self.object.id)
          return context
