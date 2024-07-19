from django.shortcuts import render

from main.models import Product


# Create your views here.
def index(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'main/index.html', context)