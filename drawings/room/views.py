from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from room.forms import *
from room.models import *


def ChooseRoom(request):
    return render(request, 'room/ChooseRoom.html')


def JoinRoom(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            username = form.cleaned_data['name']
            room = Room.objects.get(name=room_name)
            user = User.objects.create(name=username, room=room, status='Editor')
            user.save()
            request.session['id'] = user.id
            return redirect('Room', room_name=room_name)
        else:
            print(form.errors)
            return render(request, 'room/Room.html')
    else:
        form = CreateRoomForm()
    return render(request, 'room/JoinRoom.html', {'form': form})


def CreateRoom(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            username = form.cleaned_data['name']
            room = Room.objects.create(name=room_name)
            room.save()
            creator = User.objects.create(name=username, room=room, status='Creator')
            creator.save()
            request.session['id'] = creator.id
            return redirect('Room', room_name=room_name)
        else:
            print(form.errors)
            return render(request, 'room/Room.html')
    else:
        form = CreateRoomForm()
    return render(request, 'room/CreateRoom.html', {'form': form})


def ShowRoom(request, room_name):
    if Room.objects.get(name=room_name):
        id = request.session.get('id')
        # room = request.session.get('room')
        username = User.objects.get(id=id).name
        status = User.objects.get(id=id).status
        room = User.objects.get(id=id).room
        roommates = User.objects.filter(room=room)
        return render(request, 'room/Room.html',
                      {'username': username, 'room_name': room_name, 'status': status, 'roommates': roommates})
    else:
        return HttpResponseNotFound("no room")

    # def Middle_Room(request):
#     if request.method=='POST':
#         form = NameForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             room_name = form.cleaned_data['room_name']
#             return CreateRoom(request)
