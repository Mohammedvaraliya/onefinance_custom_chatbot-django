from django.shortcuts import render
from .chatbot_logic import get_response
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')

def query(request):
    now = datetime.now()
    if now.hour < 12:
        greeting = "Good morning"
    elif now.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    if request.method == 'POST':
        query = request.POST.get('input_text', '')
        response = get_response(query)
        return HttpResponse(response)
    else:
        context = {
            'greeting': greeting
        }
        return render(request, 'query.html', context)
