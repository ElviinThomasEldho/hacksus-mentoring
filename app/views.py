from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .decorators import *

import xlwt 
import datetime

# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.groups.exists(): 
                groups = set(group.name for group in request.user.groups.all())
                for group in groups:
                    if group == "Admin":
                        return redirect('adminDashboard')
                    elif group == "Team":
                        return redirect('teamDashboard')
                    elif group == "Mentor":
                        return redirect('mentorDashboard')

        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'app/loginUser.html')

@authenticated_user
def logoutUser(request):
    logout(request)
    return redirect('loginUser')

def registerUser(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('registerTeam')

    context = {
        'form': form,
    }

    return render(request, 'app/registerUser.html', context)

def registerTeam(request):
    form = TeamForm()
    
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            team.user = request.user
            team.save()
            group = Group.objects.get(name='Team') 
            group.user_set.add(request.user)            
            return redirect('teamDashboard')

    context = {
        "form": form,
        }
    
    return render(request, "app/registerTeam.html", context)

@admin_mentor_only
def mentorDashboard(request):
    mentor = Mentor.objects.get(user = request.user) 
    openTickets = Ticket.objects.filter(status='Open').order_by('timeCreated')
    acceptedTickets = Ticket.objects.filter(status='Accepted', mentor=mentor).order_by('timeCreated')
    closedTickets = Ticket.objects.filter(status='Closed').order_by('timeCreated')
    judgements = Judgement.objects.filter(mentor = mentor)

    print(judgements)

    form = JudgementForm()
    
    if request.method == 'POST':
        form = JudgementForm(request.POST)
        if form.is_valid():
            judgement = form.save()
            print(judgement)
            judgement.mentor = mentor
            judgement.round = 'Round 1'
            print(judgement.mentor)
            print(judgement.round)
            judgement.save()           
            return redirect('mentorDashboard')

    context = {
        "mentor": mentor,
        "form": form,
        "openTickets": openTickets,
        "acceptedTickets": acceptedTickets,
        "closedTickets": closedTickets,
        "judgements": judgements,
        }
    
    return render(request, "app/mentorDashboard.html", context)

@admin_mentor_only
def viewTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    
    context = {
        "ticket": ticket,
        }
    
    return render(request, "app/viewTicket.html", context)

@admin_mentor_only
def acceptTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    mentor = Mentor.objects.get(user=request.user)
    ticket.mentor = mentor
    ticket.status = 'Accepted'
    ticket.save()
    
    return redirect('mentorDashboard')

@admin_mentor_only
def closeTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    mentor = Mentor.objects.get(user=request.user)
    ticket.mentor = mentor
    ticket.status = 'Closed'
    ticket.save()
    
    return redirect('mentorDashboard')

@admin_mentor_only
def reopenTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    mentor = Mentor.objects.get(user=request.user)
    ticket.mentor = mentor
    ticket.status = 'Open'
    ticket.save()
    
    return redirect('mentorDashboard')


@team_only
def teamDashboard(request):
    team = Team.objects.get(user = request.user)  
    tickets = Ticket.objects.filter(team=team)
    form = TicketForm()

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            ticket.team = team
            ticket.save()        
            return redirect('teamDashboard')
    

    context = {
        "team": team,
        "form": form,
        "tickets": tickets,
        }
    
    return render(request, "app/teamDashboard.html", context)


@admin_only
def adminDashboard(request):
    openTickets = Ticket.objects.filter(status='Open').order_by('timeCreated')
    acceptedTickets = Ticket.objects.filter(status='Accepted').order_by('timeCreated')
    closedTickets = Ticket.objects.filter(status='Closed').order_by('timeCreated')
    judgements = Judgement.objects.all()

    print(judgements)

    context = {
        "user":request.user,
        "openTickets": openTickets,
        "acceptedTickets": acceptedTickets,
        "closedTickets": closedTickets,
        "judgements": judgements,
        }
    
    return render(request, "app/adminDashboard.html", context)


@admin_only
def exportData(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'filename=JudgementData' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    wsJudgement = wb.add_sheet('Judgements List')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True


    columns=[
        ['ID','Mentor','Round','Team Name',"Table Number",'Criteria A', 'Criteria B', 'Criteria C','Criteria D','Time Created']
    ]

    for col_num in range(len(columns[0])):
        wsJudgement.write(row_num, col_num, columns[0][col_num],font_style)
        
    font_style = xlwt.XFStyle()

    judgementList = Judgement.objects.all().values_list('id','mentor','round','teamName','tableNumber','criteriaA','criteriaB', 'criteriaC', 'criteriaD','timeCreated')
   

    judgementList2 = []

    row_num = 0
    for row in judgementList:
        row_num +=1
        temp = list(row)
        temp[9] = str(temp[9].date()) + " " + str(temp[9].time())
        temp[1] = Mentor.objects.get(id=temp[1]).firstName + " " + Mentor.objects.get(id=temp[1]).lastName + " | " + Mentor.objects.get(id=temp[1]).organisation
        # 18
        judgementList2.append(tuple(temp))

    row_num = 0
    for row in judgementList2:
        row_num +=1
        for column_num in range(len(row)):
            wsJudgement.write(row_num, column_num, str(row[column_num]),font_style)

    wb.save(response)

    return response