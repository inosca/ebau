from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'users', views.UserView,  'user')

urlpatterns = r.urls
