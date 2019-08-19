from django.contrib import admin

from django.conf.urls import include,url

urlpatterns = [
    # Examples:
    # url(r'^$', 'firstdata.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^appmap/', include('appmap.urls')),
    
]
