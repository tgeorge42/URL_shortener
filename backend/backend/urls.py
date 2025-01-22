from django.contrib import admin
from django.urls import path, include
from shortener.views import RedirectURLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shortener.urls')),  # Shortener app URLs
    path('go/<str:short_code>/', RedirectURLView.as_view(), name='redirect_url'),  # Redirect to shortlinks
]
