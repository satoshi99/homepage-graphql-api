from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from api.views import PrivateGraphQLView
from graphql_homepage.schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(PrivateGraphQLView.as_view(graphiql=True, schema=schema))),
    path('mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)