from django.shortcuts import render
from .chatbot_logic import get_response

# Create your views here.
def home(request):
    return render(request, 'home.html')

def query(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if not query:
            response = "Please enter something"
        else:
            response = get_response(query)
        context = {
            'query': query, 'response': response
        }
        return render(request, 'response.html', context)
    else:
        return render(request, 'query.html')
