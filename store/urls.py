
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info, name='update_info'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('categories/<str:cat>', views.category, name='category'),
    path('categories_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),

    path('api/', views.APIRootView.as_view(), name='api_root'),
    path('api/product/', views.ProductList.as_view(), name='api_product'),
    path('api/product/<int:pk>', views.ProductDetails.as_view(), name='api_product_details'),
    path('api/category/', views.CategoryList.as_view(), name='api_category'),
    path('api/category/<int:pk>', views.CategoryDetails.as_view(), name='api_category_details'),
    path('api/profile/', views.ProfileList.as_view(), name = 'api_profile'),
    path('api/profile/<int:pk>', views.ProfileDetails.as_view(), name = 'api_profile_details'),
    path('api/order/', views.OrderList.as_view(), name='api_order'),
    path('api/order/<int:pk>', views.OrderDetails.as_view(), name='api_order_details'),
    path('api/order-item/', views.OrderItemList.as_view(), name='api_order_item'),
    path('api/order-item/<int:pk>', views.OrderItemDetails.as_view(), name='api_order_item_details'),

]
