from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"tags", views.TagView)
r.register(r"keywords", views.KeywordView)
r.register(r"static-keywords", views.StaticKeywordView, basename="static-keyword")
r.register(r"instance-marks", views.InstanceMarkView)

urlpatterns = r.urls
