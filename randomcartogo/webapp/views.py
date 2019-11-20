from django.shortcuts import render, redirect, get_object_or_404
from .form import CarForm
from .models import Car
from random import randint

def goToListPage(request):
    cars = Car.objects.all()
    return render(request, 'list.html', { 'isShowingInput': True, 'cars': cars })

def goToRandom(request, firstRandom, showingText):
    return render(request, 'random.html', { 'isShowingInput': False, 'firstRandom': firstRandom, 'result': showingText })

def goToAddPage(request, form):
    return render(request, 'add.html', { 'isShowingInput': True, 'form': form, 'isShowingEdit': False })

def save(request, instance):
    if instance is None:
        form = CarForm(request.POST)
    else:
        form = CarForm(request.POST, instance=instance)
    if form.is_valid():
        car = form.save(commit=False)
        car.save()

def add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            save(request, None)
            return goToListPage(request)     
        else: 
            form = CarForm()
        return goToAddPage(request, form)
    else:
        return redirect('mainpage')

def mainpage(request):  
    return goToRandom(request, True, 'Random some car')

def random(request):
    carQuerySet = Car.objects.all()    
    randNum = randint(0, carQuerySet.count()-1)
    carList = list(carQuerySet)
    result = carList[randNum]
    return goToRandom(request, False, result)

def listpage(request):
    return goToListPage(request)

def delete(request, pk):
    if request.user.is_authenticated:
        try:
            car = Car.objects.get(id=pk).delete()
        except Car.DoesNotExist:
            print('not existed')
        return goToListPage(request)
    else:
        return redirect('mainpage')

def edit(request, pk):
    if request.user.is_authenticated:
        car = get_object_or_404(Car, pk=pk)
        if request.method == "POST":
            save(request, car)
            return goToListPage(request)
        else:
            carForm = CarForm(instance=car)
        return goToAddPage(request, carForm)
    else:
        return redirect('mainpage')