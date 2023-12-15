from django.db import models
from django.contrib.auth.models import User
from datetime import date, timezone, timedelta

# Create your models here.
class Venue(models.Model):
    name = models.CharField("Venue Name", max_length=255, null=True)
    floor = models.IntegerField("Floor", null=True)
    
    def __str__(self):
        return self.name + " | Floor " + str(self.floor)
    

class Team(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField("Team Name", max_length=255, null=True)
    tableNumber = models.IntegerField("Table Number", null=True)
    venue = models.ForeignKey(Venue, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.tableNumber) + " | " + self.name
    

class Mentor(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    firstName = models.CharField("First Name", max_length=255, null=True)
    lastName = models.CharField("Last Name", max_length=255, null=True)
    email = models.EmailField("Email Address", null=True)
    organisation = models.CharField("Organisation", max_length=255, null=True)
    
    def __str__(self):
        return str(self.id) + " | " + self.firstName + " " + self.lastName + " | " + self.organisation  
    

class Ticket(models.Model):
    STATUS = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Accepted', 'Accepted'),
    )

    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, null=True, on_delete=models.CASCADE)
    title = models.CharField("Issue Title", max_length=255, null=True)
    desc = models.CharField("Issue Description", max_length=255, null=True)
    platform = models.CharField("Platform Information", max_length=255, null=True)
    status = models.CharField("Status", max_length=255, choices=STATUS, default='Open', null=True)
    timeCreated = models.DateTimeField("Created Time", auto_now_add=True)
    timeClosed = models.DateTimeField("Closed Time", auto_now_add=True)
    
    def __str__(self):
        return str(self.id) + " | " + str(self.team.tableNumber) + " | " + self.team.name + " | " + self.status
    
    

class Judgement(models.Model):
    GRADE = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    
    ROUND = (
        ('Round 1', 'Round 1'),
        ('Round 2', 'Round 2'),
        ('Round 3', 'Round 3'),
        ('Round 4', 'Round 4')
    )

    mentor = models.ForeignKey(Mentor, null=True, on_delete=models.CASCADE)
    teamName = models.CharField("Team Name", max_length=255, null=True)
    tableNumber = models.CharField("Table Number",max_length=10,  null=True)
    round = models.CharField("Round", max_length=255, choices=ROUND, null=True)
    criteriaA = models.CharField("Criteria A", max_length=255, choices=GRADE, null=True)
    criteriaB = models.CharField("Criteria B", max_length=255, choices=GRADE, null=True)
    criteriaC = models.CharField("Criteria C", max_length=255, choices=GRADE, null=True)
    criteriaD = models.CharField("Criteria D", max_length=255, choices=GRADE, null=True)
    timeCreated = models.DateTimeField("Time Created", auto_now_add=True)
    
    def __str__(self):
        # return str(self.id) + " | " + str(self.mentor.firstName) + " | " + self.tableNumber + " | " + self.round
        return str(self.id)