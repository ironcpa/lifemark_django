from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from main import views
from accounts import views as account_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.home_page, name='home'),
    url(r'^$', views.LifemarkSearchListView.as_view(), name='home'),
    # url(r'^search$', views.search, name='search'),
    url(r'^search$', views.LifemarkSearchListView.as_view(), name='search'),
    # url(r'^new$', views.new_lifemark, name='new'),
    url(r'^new$', views.CreateLifemarkView.as_view(), name='new'),
    # url(r'^update$', views.update_lifemark, name='update'),
    url(r'^update/(?P<pk>\d+)/$', views.UpdateLifemarkView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteLifemarkView.as_view(), name='delete'),

    url(r'^signup/$', account_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^anon/$', account_views.test_anon_user_view, name='anon'),

    # url(r'^test$', views.TestListView.as_view(), name='test_list'),
    url(r'^test$', views.test_view, name='test'),
]
