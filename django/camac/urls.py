from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/v1/', include('camac.user.urls')),
    url(r'^api/v1/', include('camac.instance.urls')),
    url(r'^api/v1/', include('camac.document.urls')),
    url(r'^api/v1/', include('camac.circulation.urls')),
]
