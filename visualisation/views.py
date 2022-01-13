from django.shortcuts import redirect,render
from .models import Visualisation
from .utils import get_first, get_plot, get_seaplot
from .util2 import get_util2_first
# Imaginary function to handle an uploaded file.
from django.http import HttpResponseRedirect
from .models import Document
from .forms import DocumentForm
# Create your views here.

def main_view(request):
    my_view(request)
    qv = Visualisation.objects.all()
    x = [x.item for x in qv]
    y = [y.price for y in qv]
    #chart = get_plot(x,y)
    chart = get_seaplot()
    #chart = get_first()
    #chart = get_util2_first()

    return render(request,'dashboard/index.html',{'chart': chart})

def second_view(request):
    qv = Visualisation.objects.all()
    x = [x.item for x in qv]
    y = [y.price for y in qv]
    #chart = get_plot(x,y)
    chart = get_first()
    #chart = get_util2_first()
    return render(request,'dashboard/index.html',{'chart': chart})

def third_view(request):
    qv = Visualisation.objects.all()
    x = [x.item for x in qv]
    y = [y.price for y in qv]
    #chart = get_plot(x,y)
    # chart = get_first()
    chart = get_util2_first()
    return render(request,'dashboard/index.html',{'chart': chart})

def fourth_view(request):
    qv = Visualisation.objects.all()
    x = [x.item for x in qv]
    y = [y.price for y in qv]
    chart = get_plot(x,y)
    # chart = get_first()
    # chart = get_util2_first()
    return render(request,'dashboard/index.html',{'chart': chart})





def my_view(request):
    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'dashboard/upload.html', context)