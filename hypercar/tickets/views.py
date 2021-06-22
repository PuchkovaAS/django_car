from django.template import loader
from django.views import View
from django.http.response import HttpResponse

from tickets.models import get_waiting_time, line_of_cars, get_next_ticket, work_next_ticket
from django.shortcuts import redirect, reverse


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome")


class TicketView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tickets/ticket.html')

        # print(kwargs['link'])
        # print(request.path)

        num, time = get_waiting_time(kwargs['link'])

        context = {
            "ticket":
                {
                    'num': num,
                    'time': time,
                }
        }
        return HttpResponse(template.render(context, request))


class Processing(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tickets/processing.html')
        latest_question_list = [
            {
                'count': line_of_cars['change_oil'],
                'question_text': 'Change oil queue',
            },
            {
                'count': line_of_cars['inflate_tires'],
                'question_text': 'Inflate tires queue',
            },
            {
                'count': line_of_cars['diagnostic'],
                'question_text': 'Get diagnostic queue',
            },
        ]
        context = {
            'latest_question_list': latest_question_list,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        work_next_ticket()
        return redirect(reverse('next_ticket'))


class MenuView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tickets/index.html')
        latest_question_list = [
            {
                'id': 'change_oil',
                'question_text': 'Change oil',
            },
            {
                'id': 'inflate_tires',
                'question_text': 'Inflate tires',
            },
            {
                'id': 'diagnostic',
                'question_text': 'Get diagnostic test',
            },
        ]
        context = {
            'latest_question_list': latest_question_list,
        }
        return HttpResponse(template.render(context, request))


class NextTicket(View):
    def get(self, request, *args, **kwargs):
        next_ticket = get_next_ticket()
        template = loader.get_template('tickets/next_ticket.html')
        print(next_ticket)
        context = {
            'next_ticket': next_ticket,
        }
        return HttpResponse(template.render(context, request))
