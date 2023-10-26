from typing import Any, Dict
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView, FormView
from base.decorations.toast_decorator import include_toast
from django.urls import reverse_lazy, reverse
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from . import models, forms
from apps.portal.models import Promotion

import json

class IndexView(TemplateView):
    template_name = 'protect_network/index.html'
    model = models.SpotType
    form_class = forms.SpotTypeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_types = models.SpotType.objects.all()
        context['spot_types'] = spot_types
    
        return context


class DetailSpotView(DetailView):
    model = models.Spot
    template_name = 'protect_network/spot_detail.html'
    context_object_name = 'spot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        spot = self.get_object()
        contact_info = models.ContactInfo.objects.filter(spot=spot)
        opening_hours = models.OpeningHours.objects.filter(spot=spot)
        images = models.Image.objects.filter(spot=spot).order_by('-id')[:12]
        spot_types = models.SpotType.objects.filter(spot=spot)
        progress_bar_math = (spot.next_update / spot.spot_type.update_time) * 100
        progress_bar_math_rounded = round(progress_bar_math)

        context['spot_progress_bar_math'] = progress_bar_math_rounded
        context['spot_contacts'] = contact_info
        context['spot_opening_hours'] = opening_hours
        context['spot_images'] = images
        context['spot_types'] = spot_types

        return context
    


class DetailCardSpotView(DetailView):
    model = models.Spot
    template_name = 'protect_network/spot_detail_card.html'
    context_object_name = 'spot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot = self.get_object()
        images = models.Image.objects.filter(spot=spot).order_by('-id')[:1]
        context['spot_images'] = images
        
        return context
    

@include_toast
class CreateSpotView(CreateView):
    model = models.Spot
    form_class = forms.SpotForm
    template_name = 'protect_network/spot_add.html'
    success_url = reverse_lazy('protect_network:spot_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        self.object.location = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.updated_at = timezone.now()
        self.object.update_score = 100
        # military = get_object_or_404(models.portal_models.Military, user=self.request.user)
        # self.object.user_unit_id = military.id
        promotion = get_object_or_404(Promotion, military__user=self.request.user)
        self.object.user_unit = promotion
        spot_type = self.object.spot_type
        spot_next_update = spot_type.update_time
        is_headquarters = form.cleaned_data['is_headquarters']
        self.object.is_headquarters = is_headquarters
        self.object.next_update = spot_next_update
        self.object.save()
        location_value = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
        zipcode_value = form.cleaned_data.get('zipcode')
        city_value = form.cleaned_data.get('city')
        neighborhood_value = form.cleaned_data.get('neighborhood')
        street_value = form.cleaned_data.get('street')
        number_value = form.cleaned_data.get('number')
        complement_value = form.cleaned_data.get('complement')
        reference_value = form.cleaned_data.get('reference')
        address1 = models.Address(street=street_value,number=number_value, complement=complement_value,reference=reference_value, neighborhood=neighborhood_value,
                                    city=city_value, state="PB", region="NE", zipcode=zipcode_value, place=location_value, created_by=self.request.user,
                                      updated_by=self.request.user)
        address1.save()
        self.object.addresses.add(address1)
        return super().form_valid(form)



@include_toast
class UpdateSpotView(UpdateView):
    model = models.Spot
    template_name = 'protect_network/spot_update.html'
    form_class = forms.SpotForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        self.object.location = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
        self.object.updated_by = self.request.user
        self.object.update_score = 100
        self.object.updated_at = timezone.now()
        spot_type = self.object.spot_type
        spot_next_update = spot_type.update_time
        self.object.next_update = spot_next_update
        tags = self.request.POST.getlist('tags')
        location_value = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
        zipcode_value = form.cleaned_data.get('zipcode')
        city_value = form.cleaned_data.get('city')
        neighborhood_value = form.cleaned_data.get('neighborhood')
        street_value = form.cleaned_data.get('street')
        number_value = form.cleaned_data.get('number')
        complement_value = form.cleaned_data.get('complement')
        reference_value = form.cleaned_data.get('reference')
        address_id = self.object.spotaddresses_set.first().address.id
        existing_address = get_object_or_404(models.Address, id=address_id)
        existing_address.street = street_value
        existing_address.number = number_value
        existing_address.complement = complement_value
        existing_address.reference = reference_value
        existing_address.neighborhood = neighborhood_value
        existing_address.city = city_value
        existing_address.zipcode = zipcode_value
        existing_address.place = location_value
        existing_address.save()
        self.object.addresses.add(existing_address)
        is_headquarters = form.cleaned_data['is_headquarters']
        self.object.is_headquarters = is_headquarters
        self.object.save()
        self.object.tags.set(tags)
        return super().form_valid(form)
    
    def get_success_url(self):
        spot_pk = self.object.pk
        return reverse('protect_network:spot_detail', kwargs={'pk': spot_pk})
    

class SpotListView(ListView):
    model = models.Spot
    template_name = 'protect_network/spot_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SpotListView, self).get_context_data(**kwargs)
        spot = models.Spot.objects.all()

        context['spots'] = spot
        return context


class SpotListCreatedView(ListView):
    model = models.Spot
    template_name = 'protect_network/spot_list_created.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SpotListCreatedView, self).get_context_data(**kwargs)
        spot = models.Spot.objects.all()
        context['spots'] = spot
        return context
    

@include_toast
class CreateSpotTypeView(CreateView):
    model = models.SpotType
    form_class = forms.SpotTypeForm
    template_name = 'protect_network/spot_type_add.html'
    success_url = reverse_lazy('protect_network:type_list')


@include_toast
class UpdateSpotTypeView(UpdateView):
    model = models.SpotType
    template_name = 'protect_network/spot_type_add.html'
    form_class = forms.SpotTypeForm
    success_url = reverse_lazy('protect_network:type_list')


class SpotTypeListView(ListView):
    model = models.SpotType
    template_name = 'protect_network/spot_type_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SpotTypeListView, self).get_context_data(**kwargs)
        spot_type = models.SpotType.objects.all()
        context['spot_types'] = spot_type
        return context
    

@include_toast
class CreateTagView(CreateView):
    model = models.Tag
    form_class = forms.TagForm
    template_name = 'protect_network/tag_add.html'
    success_url = reverse_lazy('protect_network:tag_list')


@include_toast
class UpdateSpotTagsView(UpdateView):
    model = models.Spot
    template_name = 'protect_network/spot_tags_form.html'
    form_class = forms.SpotTagsForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        spot_pk = self.object.pk
        return reverse('protect_network:spot_detail', kwargs={'pk': spot_pk})
    

@include_toast
class UpdateTagView(UpdateView):
    model = models.Tag
    template_name = 'protect_network/tag_add.html'
    form_class = forms.TagForm
    success_url = reverse_lazy('protect_network:tag_list')


class TagListView(ListView):
    model = models.Tag
    template_name = 'protect_network/tag_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        tag = models.Tag.objects.all()
        context['tags'] = tag
        return context
    

@include_toast
class CreateImageSpotView(CreateView):
    model = models.Image
    template_name = 'protect_network/spot_image_add.html'
    form_class = forms.SpotImageForm

    def get_success_url(self):
        spot_id = self.kwargs['spot_id']
        return reverse_lazy('protect_network:spot_detail', kwargs={'pk': spot_id})

    def form_valid(self, form):
        spot_id = self.kwargs['spot_id']
        form.instance.spot_id = spot_id
        spot = get_object_or_404(models.Spot, id=spot_id)
        spot_image = form.save(commit=False)
        spot_image.spot = spot
        spot_image.created_by = self.request.user
        spot_image.save()
        return super().form_valid(form)
    

@include_toast
class ImageDeleteView(DeleteView):
    model = models.Image
    template_name = 'protect_network/spot_image_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_id = self.object.spot.id
        context['spot_id'] = spot_id
        return context
    
    def get_success_url(self):
        spot_id = self.object.spot.id
        return reverse_lazy('protect_network:spot_image_list', kwargs={'spot_id': spot_id})
    

class ImageListView(ListView):
    model = models.Image
    template_name = 'protect_network/spot_image_list.html'
    context_object_name = 'spot_images'
    
    def get_queryset(self):
        spot_id = self.kwargs.get('spot_id')
        queryset = super().get_queryset()
        return queryset.filter(spot_id=spot_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_id = self.kwargs.get('spot_id')
        spot = get_object_or_404(models.Spot, pk=spot_id)
        context['spot_pk'] = spot.pk
        return context
    

@include_toast
class CreateContactInfoView(CreateView):
    model = models.ContactInfo
    template_name = 'protect_network/spot_contact_form.html'
    form_class = forms.ContactInfoForm

    def get_success_url(self):
        spot_id = self.kwargs['spot_id']
        return reverse_lazy('protect_network:spot_detail', kwargs={'pk': spot_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_id = self.kwargs.get('spot_id')
        spot = get_object_or_404(models.Spot, pk=spot_id)
        context['spot_pk'] = spot.pk
        return context
    
    def form_valid(self, form):
        spot_id = self.kwargs['spot_id']
        form.instance.spot_id = spot_id
        return super().form_valid(form)
    

@include_toast
class UpdateContactInfoView(UpdateView):
    model = models.ContactInfo
    template_name = 'protect_network/spot_contact_form.html'
    form_class = forms.ContactInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spot_pk'] = self.object.spot_id
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spot_pk'] = self.object.spot_id
        return context

    def get_success_url(self):
        spot_id = self.object.spot_id
        return reverse('protect_network:spot_detail', args=[spot_id])
    

@include_toast
class CreateOpeningHoursView(CreateView):
    model = models.OpeningHours
    template_name = 'protect_network/spot_opening_hours_form.html'
    form_class = forms.OpeningHoursForm
    
    def get_success_url(self):
        spot_id = self.kwargs['spot_id']
        return reverse_lazy('protect_network:spot_detail', kwargs={'pk': spot_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_id = self.kwargs.get('spot_id')
        spot = get_object_or_404(models.Spot, pk=spot_id)
        context['spot_pk'] = spot.pk
        return context

    def form_valid(self, form):
        spot_id = self.kwargs['spot_id']
        form.instance.spot_id = spot_id
        self.object = form.save(commit=False)
        self.object.open_time_mon = self.request.POST.get('monday_open_name', '')
        self.object.close_time_mon = self.request.POST.get('monday_close_name', '')
        self.object.open_time_tue = self.request.POST.get('tuesday_open_name', '')
        self.object.close_time_tue = self.request.POST.get('tuesday_close_name', '')
        self.object.open_time_wed = self.request.POST.get('wednesday_open_name', '')
        self.object.close_time_wed = self.request.POST.get('wednesday_close_name', '')
        self.object.open_time_thu = self.request.POST.get('thursday_open_name', '')
        self.object.close_time_thu = self.request.POST.get('thursday_close_name', '')
        self.object.open_time_fri = self.request.POST.get('friday_open_name', '')
        self.object.close_time_fri = self.request.POST.get('friday_close_name', '')
        self.object.open_time_sat = self.request.POST.get('saturday_open_name', '')
        self.object.close_time_sat = self.request.POST.get('saturday_close_name', '')
        self.object.open_time_sun = self.request.POST.get('sunday_open_name', '')
        self.object.close_time_sun = self.request.POST.get('sunday_close_name', '')
        self.object.save()
        return super().form_valid(form)
    

@include_toast
class UpdateOpeningHoursView(UpdateView):
    model = models.OpeningHours
    template_name = 'protect_network/spot_opening_hours_form.html'
    form_class = forms.OpeningHoursForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spot_pk'] = self.object.spot_id
        context['load_open_time_mon'] = self.object.open_time_mon
        context['load_close_time_mon'] = self.object.close_time_mon
        context['load_open_time_tue'] = self.object.open_time_tue
        context['load_close_time_tue'] = self.object.close_time_tue
        context['load_open_time_wed'] = self.object.open_time_wed
        context['load_close_time_wed'] = self.object.close_time_wed
        context['load_open_time_thu'] = self.object.open_time_thu
        context['load_close_time_thu'] = self.object.close_time_thu
        context['load_open_time_fri'] = self.object.open_time_fri
        context['load_close_time_fri'] = self.object.close_time_fri
        context['load_open_time_sat'] = self.object.open_time_sat
        context['load_close_time_sat'] = self.object.close_time_sat
        context['load_open_time_sun'] = self.object.open_time_sun
        context['load_close_time_sun'] = self.object.close_time_sun
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.open_time_mon = self.request.POST.get('monday_open_name', '')
        self.object.close_time_mon = self.request.POST.get('monday_close_name', '')
        self.object.open_time_tue = self.request.POST.get('tuesday_open_name', '')
        self.object.close_time_tue = self.request.POST.get('tuesday_close_name', '')
        self.object.open_time_wed = self.request.POST.get('wednesday_open_name', '')
        self.object.close_time_wed = self.request.POST.get('wednesday_close_name', '')
        self.object.open_time_thu = self.request.POST.get('thursday_open_name', '')
        self.object.close_time_thu = self.request.POST.get('thursday_close_name', '')
        self.object.open_time_fri = self.request.POST.get('friday_open_name', '')
        self.object.close_time_fri = self.request.POST.get('friday_close_name', '')
        self.object.open_time_sat = self.request.POST.get('saturday_open_name', '')
        self.object.close_time_sat = self.request.POST.get('saturday_close_name', '')
        self.object.open_time_sun = self.request.POST.get('sunday_open_name', '')
        self.object.close_time_sun = self.request.POST.get('sunday_close_name', '')
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        spot_id = self.object.spot_id
        return reverse('protect_network:spot_detail', args=[spot_id])
    
###### NETWORK - REDE ######

@include_toast
class CreateNetworkView(CreateView):
    model = models.Network
    form_class = forms.NetworkForm
    template_name = 'protect_network/network_form.html'
    success_url = reverse_lazy('protect_network:network_list')


class UpdateNetworkView(UpdateView):
    model = models.Network
    template_name = 'protect_network/network_form.html'
    form_class = forms.NetworkForm
    context_object_name = 'network'

    def get_success_url(self):
        return reverse_lazy('protect_network:network_list')


class NetworkListView(ListView):
    model = models.Network
    template_name = 'protect_network/network_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(NetworkListView, self).get_context_data(**kwargs)
        network = models.Network.objects.all()
        context['networks'] = network
        return context


class NetworkDetailView(DetailView):
    model = models.Network
    template_name = 'protect_network/network_detail.html'
    context_object_name = 'network'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        network = context['network']
        network_responsibles = network.networkresponsible_set.all()
        context['network_responsibles'] = network_responsibles

        return context
    

###### RESPONSIBLE - MILITAR RESPONSÁVEL PELA REDE ######

@include_toast
class CreateResponsibleView(CreateView):
    model = models.NetworkResponsible
    form_class = forms.ResponsibleForm
    template_name = 'protect_network/responsible_form.html'
    success_url = reverse_lazy('protect_network:network_list')

    
class UpdateResponsibleView(UpdateView):
    model = models.NetworkResponsible
    template_name = 'protect_network/responsible_form.html'
    form_class = forms.ResponsibleForm

    def get_success_url(self):
        responsible = self.object
        network_pk = responsible.network.pk
        return reverse_lazy('protect_network:network_detail', kwargs={'pk': network_pk})
    
class DeleteResponsibleView(DeleteView):
    model = models.NetworkResponsible
    template_name = 'protect_network/responsible_delete.html'
    #success_url = reverse_lazy('protect_network:network_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_to_delete'] = self.get_object()
        return context
    
    def get_success_url(self):
        responsible = self.object
        network_pk = responsible.network.pk
        return reverse_lazy('protect_network:network_detail', kwargs={'pk': network_pk})


###### QPP - QPP DO SPOT ######

@include_toast
class CreateQppView(CreateView):
    model = models.Qpp
    form_class = forms.QppForm
    template_name = 'protect_network/qpp_add.html'
    success_url = reverse_lazy('protect_network:qpp_list')


@include_toast
class UpdateQppView(UpdateView):
    model = models.Qpp
    template_name = 'protect_network/qpp_add.html'
    form_class = forms.QppForm
    success_url = reverse_lazy('protect_network:qpp_list')


class QppListView(ListView):
    model = models.Qpp
    template_name = 'protect_network/qpp_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(QppListView, self).get_context_data(**kwargs)
        qpp = models.Qpp.objects.all()
        context['qpps'] = qpp
        return context