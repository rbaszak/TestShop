from django.urls import include, path
from .views import ShopView, RegisterView, LoginView, LogoutView, UserDetailView, ClientDetailView, BuyView, \
    AddProductView, DeleteProductView

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<slug:login>', UserDetailView.as_view(), name='user_detail'),
    path('client/<slug:login>', ClientDetailView.as_view(), name='client_detail'),
    path('buy/<slug:product_id>', BuyView.as_view(), name='buy'),
    path('add-product/', AddProductView.as_view(), name='add_products'),
    path('delete-product/<slug:product_id>', DeleteProductView.as_view(), name='delete_product')
]
