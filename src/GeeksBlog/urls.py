from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include,url
from django.contrib import admin

from posts import views

from authenticate.views import (
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("posts.urls"), name='posts'),
    url(r'^comments/', include("comments.urls"), name='comments'),

    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

