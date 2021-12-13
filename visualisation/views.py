from django.shortcuts import render
from django.http import HttpResponse
from .models import Visualisation
from .utils import get_first, get_plot, get_seaplot
from .forms import UploadedFileForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def main_view(request):
    if request.method == "POST":
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            qv = Visualisation.objects.all()
            x = [x.item for x in qv]
            y = [y.price for y in qv]
            # chart = get_plot(x,y)
            # chart = get_seaplot()
            chart = get_first(request.FILES["data_file"])

            return render(request, 'dashboard/index.html', {'chart': chart})
    
    else:
        form = UploadedFileForm()
        return render(request, 'dashboard/index.html', {'form': form})