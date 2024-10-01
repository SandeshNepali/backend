from django.shortcuts import render


def ride_view(request):

    return render(request, "index.html")
