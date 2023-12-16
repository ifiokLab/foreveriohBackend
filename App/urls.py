from django.urls import path
from .views import (LoginView,HeartDeceasedView,TributeListView,AddTributeView,MemorialListView, LogoutView,EditMemorialView,SignupView,CreateMemorialView,UserMemorialsView,DeleteMemorialView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('create_memorial/', CreateMemorialView.as_view(), name='create_memorial'),
    path('user_memorials/', UserMemorialsView.as_view(), name='user_memorials'),
    path('memorials/<int:memorial_id>/delete/', DeleteMemorialView.as_view(), name='delete_memorial'),
    path('memorials/<int:memorial_id>/edit/', EditMemorialView.as_view(), name='edit_memorial'),
    path('memorial-list/', MemorialListView.as_view(), name='memorial-list'),
    path('add-tribute/', AddTributeView.as_view(), name='add-tribute'),
    path('tribute-list/<int:deceased_id>/', TributeListView.as_view(), name='tribute-list'),
    path('heart-deceased/<int:deceased_id>/', HeartDeceasedView.as_view(), name='heart-deceased'),
]
