from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils import timezone

from pylogix import PLC
import time
import datetime

from .models import *
from .AB_Pylogix import *

def home(request):
    if(request.method == 'POST'):
        pass

    newest = LogEntry.objects.all().order_by("-date").first()
    return render(request, "home.html", {'tag_1': newest.value1, 'tag_2': newest.value2})

def increment_scores(request):
    print("Test")
    Increment_Scores()
    scan_results = Scan()

    new_entry = LogEntry(
        date = datetime.datetime.now(),
        value1 = scan_results[0],
        value2 = scan_results[1]
    )

    new_entry.save()

    return JsonResponse({'Status': 200})