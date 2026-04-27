from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils import timezone
from django.core.cache import cache

import datetime

from .scanner_service import *
from .models import *

# Main page with live logging and polling
def home(request):
    if(request.method == 'POST'):
        pass

    return render(request, "home.html")

# The view db page allows users to view all of the logs and search through them
def view_db(request):
    logs = LogEntry.objects.all().order_by("-date")

    # Get values from the form
    search_query = request.GET.get('search', '').strip()
    date_query = request.GET.get('date_filter', '').strip()

    # Filter by search query
    if search_query:
        logs = logs.filter(
            Q(log_type__icontains=search_query) | 
            Q(message__icontains=search_query)
        )

    # Filter by date
    if date_query:
        logs = logs.filter(date__date=date_query)
    
    return render(request, "view_db.html", {'log_entries': logs})

# The statistics page. Shows summarized information about the uptime, error rate, and processing time of the system.
def statistics(request: HttpRequest) -> HttpRequest:
    return render(request, "stats.html")

# ==========
# API ROUTES
# ==========

# Gets the counts of error logs and non-error logs.abs
# Required for the statistics page
@require_http_methods(["GET"])
def get_error_stats(request: HttpRequest) -> JsonResponse:
    total_messages = len(LogEntry.objects.all())
    error_messages = len(LogEntry.objects.filter(log_type="ERROR"))

    return JsonResponse({
        "error": error_messages,
        "non_error": total_messages,
    })

# Gets the numbers of the colors of each processed puck
# Required for the statistics page
@require_http_methods(["GET"])
def get_color_stats(request: HttpRequest) -> JsonResponse:
    white_count = len(LogEntry.objects.filter(log_type="COMPLETE", message__istartswith="white"))
    blue_count = len(LogEntry.objects.filter(log_type="COMPLETE", message__istartswith="blue"))
    red_count = len(LogEntry.objects.filter(log_type="COMPLETE", message__istartswith="red"))

    return JsonResponse({
        "white_count": white_count,
        "blue_count": blue_count,
        "red_count": red_count,
    })

# Gets the production time stats for the last 10 pucks.abs
# Format is response = [[oven_time, gripper_time, turntable_time, sld_time]]
# Required for the statistics page
@require_http_methods(["GET"])
def get_prod_stats(request: HttpRequest) -> JsonResponse:
    response = []


    all_logs = LogEntry.objects.filter(log_type__in=["COMPLETE", "CHECKPOINT"]).order_by("-date")
    for i in range(len(all_logs)):
        log = all_logs[i]
        # Search to find a COMPLETE log entry
        if(log.log_type != "COMPLETE"):
            continue;

        # Get all of the checkpoints leading up to the complete
        j = i
        checkpoints = []
        while(len(checkpoints) < 4):
            j += 1
            if(all_logs[j].log_type != "CHECKPOINT"):
                continue
            query = [[0, "SLD"], [1, "Turntable"], [1, "Gripper"], [1, "Oven"]]
            cur_checkpoint = all_logs[j]
            if(cur_checkpoint.message.split()[query[len(checkpoints)][0]] != query[len(checkpoints)][1]):
                continue

            checkpoints.append(all_logs[j])

        new_entry = []
        for x in range(4):
            new_entry.append(float(checkpoints[x].message.split()[-1][1:-2]))

        if(len(response) >= 10):
            break;

        response.append(new_entry)

    return JsonResponse({"times": response})

# This function gets the time for the last error log.
# It is required for the statistics page
@require_http_methods(["GET"])
def get_time_since_last_error(request: HttpRequest) -> JsonResponse:
    recent_error = LogEntry.objects.filter(log_type="SAFETY").order_by("-date").first()

    if(not recent_error):
        return JsonResponse({'Seconds': -1})

    error_time = recent_error.date;

    diff = timezone.now() - error_time
    seconds = diff.seconds

    return JsonResponse({'Seconds': seconds})

# Gets the uptime of the program
# Required for the statistics page
@require_http_methods(["GET"])
def get_uptime(request: HttpRequest) -> JsonResponse:
    uptime = get_elapsed_time()
    return JsonResponse({'Seconds': uptime})

# Gets the last 10 logs
# Required for the live update home page
@require_http_methods(["GET"])
def get_logs(request):
    entries = LogEntry.objects.all().order_by("-date").values()[:10]

    current_logs = []

    for entry in entries:
        local_date = timezone.localtime(entry['date'])
        current_logs.append(f"[{local_date:%Y-%m-%d %H:%M:%S}] [{entry["log_type"]}] {entry["message"]}")

    return JsonResponse({
        "new_logs": current_logs,
        "sld_data": cache.get("sld_data", []),
    })
