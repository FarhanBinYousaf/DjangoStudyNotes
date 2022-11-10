from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('index/',views.index,name="index"),
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.UserLogin,name="login"),
    path('logout',views.userLogout,name="logout"),
    path('adminLogin',views.adminLogin,name="adminLogin"),
    path('admin_home',views.adminHome,name="admin_home"),
    path('user_profile',views.userProfile,name="user_profile"),
    path('change_pass',views.change_pass,name="change_pass"),
    path('edit_profile',views.editProfile,name="edit_profile"),
    path('upload_notes',views.uploadNotes,name="upload_notes"),
    path('view_my_notes',views.viewMyNotes,name="view_my_notes"),
    path('delete_notes/<str:pk>/',views.deleteNotes,name="delete_notes"),
    path('view_users',views.view_users,name="view_users"),
    path('delete_users/<str:pk>/',views.deleteUsers,name="delete_users"),
    path('pending_notes',views.pendingNotes,name="pending_notes"),
    path('accepted_notes',views.acceptedNotes,name="accepted_notes"),
    path('rejected_notes',views.rejectedNotes,name="rejected_notes"),
    path('assign_status/<str:pk>/',views.assignStatus,name="assign_status"),
    path('all_notes',views.allNotes,name="all_notes"),
    path('view_all_notes',views.viewAllNotes,name="view_all_notes"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)