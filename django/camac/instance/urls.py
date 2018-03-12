from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'forms', views.FormView, 'form')
r.register(r'instances', views.InstanceView, 'instance')
r.register(r'form-fields', views.FormFieldView, 'form-field')
r.register(r'instance-states', views.InstanceStateView, 'instance-state')

urlpatterns = [
    url(
        r'form-config',
        views.FormConfigDownloadView.as_view(),
        name='form-config-download'
    ),
]

urlpatterns.extend(r.urls)
