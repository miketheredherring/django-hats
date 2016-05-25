from django.conf.urls import url

urlpatterns = [
    url(r'^test/$', 'django.shortcuts.render', name='test_url'),
]
