from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token, name='login'),
    url(r'^api-token-refresh/', refresh_jwt_token, name='refresh'),
    url(r'^api/v1/', include('camac.user.urls')),
    url(r'^api/v1/', include('camac.instance.urls')),
]
