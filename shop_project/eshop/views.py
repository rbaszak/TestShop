from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import RegisterForm, LoginForm, ClientForm, AddressForm, ProductForm, CategoryForm
from .models import Product, User, Client, Address, ProductCategory


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'register.html'

    # when 'GET' request
    def get(self, request, *args, **kwargs):
        # form instance for template
        form = self.form_class()
        context = {'form': form}
        return render(request, 'register.html', context)

    # when 'POST' request
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # handle fields
            form.db_save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('shop'))

        else:
            context = {'form': form}
            return render(request, 'register.html', context)


class ShopView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'product_list.html'


class AddProductView(View):
    form_class = ProductForm
    category_class = CategoryForm
    template_name = 'add_product.html'

    # when 'GET' request
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}

        return render(request, 'add_product.html', context)

    def post(self, request, *args, **kwargs):
        # get data from form

        form = self.form_class(request.POST)

        if form.is_valid():
            # client object
            product = Product(**form.cleaned_data)
            product.save()

            return HttpResponseRedirect(reverse('shop'))
        else:
            context = {'form': form}
            return render(request, 'login.html', context)


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'delete_product.html'

    def get_object(self, queryset=None):
        _id = self.kwargs.get("product_id")
        return get_object_or_404(Product, id=_id)

    def get_success_url(self):
        return reverse('shop')


class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        # form instance for template
        form = self.form_class()
        context = {'form': form}
        return render(request, 'login.html', context)

        # when 'POST' request

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # save login to session
            login = request.POST['login']
            request.session['login'] = login
            user = User.objects.get(login=login)
            request.session['wallet'] = user.wallet
            if user.admin:
                request.session['admin'] = True
            return HttpResponseRedirect(reverse('shop'))
        else:
            context = {'form': form}
            return render(request, 'login.html', context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        for key in request.session.keys():
            request.session[key] = None
        return HttpResponseRedirect(reverse('shop'))


class UserDetailView(DetailView):
    template_name = 'user_detail.html'

    # getting user object information
    def get_object(self, queryset=None):
        # kwargs are passed from url
        login_ = self.kwargs.get("login")

        # if accessing not currently logged user
        if login_ != self.request.session['login']:
            raise Http404

        return get_object_or_404(User, login=login_)


class BuyView(DetailView):
    template_name = 'order.html'

    def get_object(self, queryset=None):
        # kwargs are passed from url
        product_id = self.kwargs.get("product_id")

        return get_object_or_404(Product, id=product_id)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(login=self.request.session['login'])

        if user.wallet >= float(request.POST['price_out']):
            user.wallet -= float(request.POST['price_out'])
            self.request.session['wallet'] = user.wallet
            user.save()

            product = Product.objects.get(id=request.POST['product_id'])
            product.number -= int(request.POST['number'])
            product.save()

        return HttpResponseRedirect(reverse('shop'))


class ClientDetailView(UpdateView):
    template_name = 'client_detail.html'
    form_class = ClientForm
    address_form_class = AddressForm

    def get_object(self, queryset=None):
        # kwargs are passed from url
        login_ = self.kwargs.get("login")

        # if accessing not currently logged user
        if login_ != self.request.session['login']:
            raise Http404

        return get_object_or_404(User, login=login_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pass form
        # instantiate clientform
        form = self.form_class()
        form2 = self.address_form_class()
        context['form'] = form
        context['form2'] = form2

        # get user if logged
        try:
            login = self.request.session['login']
            context['logged_as'] = login
            user = User.objects.get(login=login)
            context['wallet'] = user.wallet
        except KeyError:
            context['logged_as'] = None

        return context

    # handle post request
    def post(self, request, *args, **kwargs):
        # get data from form

        form = self.form_class(request.POST)
        form2 = self.address_form_class(request.POST)

        # login from url
        login_ = self.kwargs.get("login")

        # get user associated with submitted data
        user = User.objects.get(login=login_)
        if form.is_valid() and form2.is_valid():
            # client object
            client = Client(**form.cleaned_data)
            address = Address(**form2.cleaned_data)
            address.save()

            client.address = address
            client.save()

            user.client = client
            user.save()

            return HttpResponseRedirect(reverse('shop'))
        else:
            context = {'form': form}
            return render(request, 'login.html', context)
