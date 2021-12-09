from django.shortcuts import render
from .models import Visualisation
from .utils import get_first, get_plot, get_seaplot

# Create your views here.

def main_view(request):
    qv = Visualisation.objects.all()
    x = [x.item for x in qv]
    y = [y.price for y in qv]
    # chart = get_plot(x,y)
    chart = get_seaplot()
    # chart = get_first()

    return render(request,'dashboard/index.html',{'chart': chart})