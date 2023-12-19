from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"tags", views.TagView)
r.register(r"keywords", views.KeywordView)

urlpatterns = r.urls
