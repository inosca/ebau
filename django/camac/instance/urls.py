from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'forms', views.FormView, 'form')
r.register(r'instances', views.InstanceView, 'instance')
r.register(r'form-fields', views.FormFieldView, 'form-field')

urlpatterns = r.urls
