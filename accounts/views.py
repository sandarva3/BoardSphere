from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def signup_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')

            return render(request, 'accounts/signup.html', {'form':form})
        else:
            form = SignupForm()
            return render(request, 'accounts/signup.html', {'form':form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'accounts/myaccount.html'
    success_url = reverse_lazy('myaccount')

    def get_object(self):
        return self.request.user