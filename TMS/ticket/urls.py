from django.urls import path

from . import views

urlpatterns = [
    path('raiseNewTicket', views.RaiseNewTicket.as_view(),
         name='raiseNewTicket'),
    path('addTicketEvent', views.AddTicketEvent.as_view(),
         name='addTicketEvent'),
    path('getTicketTags', views.GetTicketTags.as_view(),
         name='getTicketTags'),
    path('getTickets', views.GetTickets.as_view(),
         name='getTicketTags'),
    path('getTicketEvents', views.GetTicketEvents.as_view(),
         name='getTicketEvents'),
]
