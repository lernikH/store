from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Շնորհավորում բարեհաջող գրանցման համար')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.users, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)
    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = sum(basket.quantity for basket in baskets)
    context = {'title': 'Store-Профиль',
               'form': form,
               'baskets': Basket.objects.all(),
               'total_sum': total_sum,
               'total_quantity': total_quantity,

               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
