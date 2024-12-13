from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    # path('',views.index,name='index'),
    path('login_page',views.login_page,name='login'),
    path('login/process_login',views.process_login,name='process_login'),
    path('logout',views.process_logout,name='process_logout'),
    path('',views.user_table,name='users table'),
    path('add_user',views.add_user,name='add user'),
    path('add_department',views.add_department,name='add department'),
    path('process_add_department/',views.process_add_department,name='process_add_department'),
    path('search_user',views.search_user,name='search user'),
    path('process_add_user',views.process_add_user,name='process_add_user'),
    path('<int:user_id>/user_detail/',views.user_detail,name='user detail'),
    path('<int:user_id>/edit_user/',views.edit_user,name='edit user'),
    path('<int:user_id>/process_edit_user/',views.process_edit_user,name='process edit user'),
    path('<int:user_id>/delete_user/',views.delete_user,name='delete user'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)