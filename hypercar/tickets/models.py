from collections import deque

from django.db import models

# Create your models here.
next_ticket = None
current_number = 0
line_of_cars = {
    'change_oil': deque(),
    'inflate_tires': deque(),
    'diagnostic': deque(),
}
line_of_time = {
    'change_oil': 2,
    'inflate_tires': 5,
    'diagnostic': 30,
}


def get_waiting_time(type_customer):
    global current_number, line_of_time, line_of_cars
    current_number += 1
    line_of_cars[type_customer].append(current_number)
    if current_number < 3:
        return current_number, 0

    if type_customer == 'change_oil':
        return current_number, line_of_time[type_customer] * len(line_of_cars[type_customer]) - line_of_time[type_customer]
    elif type_customer == 'inflate_tires':
        return current_number, line_of_time['change_oil'] * len(line_of_cars['change_oil']) + line_of_time[type_customer] * \
               len(line_of_cars[type_customer]) - line_of_time[type_customer]
    else:
        return current_number, sum(
            [line_of_time[type_cust] * len(line_of_cars[type_cust]) for type_cust in line_of_cars.keys()]) - line_of_time[type_customer]


def work_next_ticket():
    global next_ticket
    ticket = None
    for queue in line_of_cars.values():
        if len(queue) == 0:
            continue
        ticket = queue.popleft()
        break
    next_ticket = ticket
    return next_ticket

def get_next_ticket():
    global next_ticket
    return next_ticket
