from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client, Vehicle
from .forms import ClientForm, VehicleForm


# clients -->
class ViewClientList(ListView):
    model = Client
    template_name = 'garage/client_list.html'
    context_object_name = 'clients'
    ordering = ['-id']  #

class ViewClientCreate(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'garage/client_form.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.success(self.request, "Клиентът беше добавен успешно!")
        return super().form_valid(form)

class ViewClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'garage/client_form.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.success(self.request, "Данните на клиента бяха обновени!")
        return super().form_valid(form)

class ViewClientDelete(DeleteView):
    model = Client
    template_name = 'garage/client_delete_confirmation.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.warning(self.request, "Клиентът беше изтрит от системата.")
        return super().form_valid(form)


# vehicles -->
class ViewVehicleList(ListView):
    model = Vehicle
    template_name = 'garage/vehicle_list.html'
    context_object_name = 'vehicles'
    ordering = ['-id']

class ViewVehicleCreate(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'garage/vehicle_form.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, "Автомобилът беше добавен успешно!")
        return super().form_valid(form)


class ViewVehicleUpdate(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'garage/vehicle_form.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, "Данните на автомобила бяха обновени!")
        return super().form_valid(form)

class ViewVehicleDelete(DeleteView):
    model = Vehicle
    template_name = 'garage/vehicle_delete_confirmation.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def form_valid(self, form):
        messages.warning(self.request, "Автомобилът беше изтрит.")
        return super().form_valid(form)
