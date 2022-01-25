from calendar import HTMLCalendar
from .models import Task
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, tasks):
        tasks_per_day = tasks.filter(due__day=day)
        d = ''
        for task in tasks_per_day:
            d += f'<li> {task.title} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'


    # formats a week as a tr
    def formatweek(self, theweek, tasks):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, tasks)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(
            due__year=self.year, due__month=self.month, created_by=self.user)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        return cal
