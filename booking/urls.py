from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    ReservationCreateView,
    CancelReservationView,
    ReservationDetailView,
    ReservationListView,
    HomeView,
    ReservationUpdateView,
    CheckAvailableTablesView,
    MyView, ContactFormView
)
from booking.apps import BookingConfig

app_name = BookingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('reservation/new/', ReservationCreateView.as_view(), name='reservation_new'),
    path('reservation/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservation/<int:pk>/cancel/', CancelReservationView.as_view(), name='cancel_reservation'),
    path('reservation/edit/<int:pk>/', ReservationUpdateView.as_view(), name='edit_reservation'),
    path('check-available-tables/', CheckAvailableTablesView.as_view(), name='check_available_tables'),
    path('my-view/', cache_page(60 * 15)(MyView.as_view()), name='my_view'),
    path('contact/', ContactFormView.as_view(), name='contact'),
]
