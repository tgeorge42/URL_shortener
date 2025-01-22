from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from .models import ShortenedURL
import random
import string
import requests
from bs4 import BeautifulSoup

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenURLView(APIView):
    def post(self, request):
        original_url = request.data.get('url')
        if not original_url:
            return Response({"error": "URL is required"}, status=400)

        existing_entry = ShortenedURL.objects.filter(original_url=original_url).first()
        if existing_entry:
            return Response({"short_url": f"{existing_entry.short_code}"}, status=200)

        short_code = generate_short_code()
        while ShortenedURL.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()

        # Scraping the title of the original URL
        try:
            response = requests.get(original_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
        except Exception:
            title = "No Title"

        short_url = ShortenedURL.objects.create(original_url=original_url, short_code=short_code, title=title)
        return Response({"short_url": f"{short_url.short_code}"}, status=201)

class RedirectURLView(APIView):
    def get(self, request, short_code):
        entry = ShortenedURL.objects.filter(short_code=short_code).first()
        if entry:
            return HttpResponseRedirect(entry.original_url)
        return Response({"error": "Shortlink not found"}, status=404)

class ListShortURLsView(APIView):
    def get(self, request):
        shortlinks = ShortenedURL.objects.all().values('original_url', 'short_code', 'title')
        return Response(list(shortlinks), status=200)
