from django.urls import path
from . import views

urlpatterns=[
    path('',views.e_login),
    path('admin_home',views.admin_home),
    path('users_details',views.list_user),
    path('property_list',views.admin_view_properties),
    path('approve/<int:property_id>',views.approve_property),
    
    path('user_reg',views.user_reg),
    path('user_home',views.user_home),
    path('add_property',views.add_property),
    path('add_amn',views.add_amenity),
    path('user_property',views.user_view_properties),
    path('edit_property/<int:property_id>/',views.edit_property),
    path('del_property/<int:property_id>/',views.delete_property),
    path('buy_page',views.buy_page),
    path('rent_page',views.rent_page),
    path('detailed/<int:property_id>/',views.property_detail),
    path('p_search',views.property_search),
    path('contact/<int:property_id>/',views.contact_seller_view),
    path('success',views.success_page),
    path('seller_req',views.seller_contact_messages),



    path('logout',views.e_logout),
]