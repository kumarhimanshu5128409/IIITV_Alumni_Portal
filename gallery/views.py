from django.shortcuts import render
import os
# Create your views here.


def gallery(request):
    images = load_images_from_folder('static/images/gallery')
    return render(request,'gallery/gallery.html',{'images':images})


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        images.append(filename)
    return images