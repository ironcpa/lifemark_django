from django.conf.urls import url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_page, name='home'),
    # url(r'^new$', views.new_lifemark, name='new'),
    url(r'^new$', views.CreateLifemarkView.as_view(), name='new'),
    # url(r'^update$', views.update_lifemark, name='update'),
    url(r'^update/(?P<pk>\d+)/$', views.UpdateLifemarkView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteLifemarkView.as_view(), name='delete'),
    url(r'^test$', views.TestListView.as_view(), name='test_list'),
]
