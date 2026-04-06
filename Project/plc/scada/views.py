from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils import timezone

from .scanner_service import scanner_instance, start_scanner
from .models import *
import datetime

def home(request):
    if(request.method == 'POST'):
        pass

    return render(request, "home.html")

def index(request):
    if(request.method == 'POST'):
        pass

    return render(request, "scada/index.html")

def view_db(request):
    logs = LogEntry.objects.all().order_by("-date")

    # Get values from the form
    search_query = request.GET.get('search', '').strip()
    date_query = request.GET.get('date_filter', '').strip()

    # Apply text search (Type or Message)
    if search_query:
        logs = logs.filter(
            Q(log_type__icontains=search_query) | 
            Q(message__icontains=search_query)
        )

    # Apply date picker filter
    if date_query:
        # date_query will be "YYYY-MM-DD". 
        # __date extracts the date portion of the DateTimeField for comparison.
        logs = logs.filter(date__date=date_query)
    
    return render(request, "view_db.html", {'log_entries': logs})

# Gets the last 10 logs and prints them to the web console
@require_http_methods(["GET"])
def get_logs(request):
    entries = LogEntry.objects.all().order_by("-date").values()[:10]
    current_logs = []

    for entry in entries:
        local_date = timezone.localtime(entry['date'])
        current_logs.append(f"[{local_date:%Y-%m-%d %H:%M:%S}] [{entry["log_type"]}] {entry["message"]}")
    
    return JsonResponse({
        "new_logs": current_logs
    })
