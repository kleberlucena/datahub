from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Avg
from django.http import JsonResponse
from base.mixins import GroupRequiredMixin

from base.decorations.toast_decorator import include_toast
from apps.portal import models as portal_models
from apps.georeference.models import SpotType as geo_spottype
from apps.georeference.models import Spot as geo_spot

from . import models, forms



class IndexView(GroupRequiredMixin, TemplateView):
    template_name = 'protect_network/index.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
    model = models.Network
    form_class = forms.NetworkForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_networks = models.Network.objects.all()
        context['spot_networks'] = spot_networks
        return context


class DetailSpotView(GroupRequiredMixin, DetailView):
    model = models.ProtectNetworkSpot
    template_name = 'protect_network/spot_detail.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
    context_object_name = 'spot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot = self.get_object()

        geospot = geo_spot.objects.all()
        network = models.ProtectNetworkSpot.objects.all()

        contact_info = models.ContactInfo.objects.filter(spot=spot)
        opening_hours = models.OpeningHours.objects.filter(spot=spot)
        images = models.Image.objects.filter(spot=spot).order_by('-id')[:12]
        #spot_types = geo_spottype.objects.filter(spot=spot)
        survey = models.SecuritySurvey.objects.filter(spot=spot)
        #progress_bar_math = (spot.next_update / spot.spot_type.update_time) * 100
        #progress_bar_math_rounded = round(progress_bar_math)
        survey_scores = models.SecuritySurvey.objects.filter(spot=spot).aggregate(average_score=Avg('score'))
        #context['spot_progress_bar_math'] = progress_bar_math_rounded
        context['spot_contacts'] = contact_info
        context['spot_opening_hours'] = opening_hours
        context['spot_images'] = images
        #context['spot_types'] = spot_types
        context['spot_survey'] = survey
        context['spot_survey_score'] = survey_scores['average_score']

        context['geospots'] = geospot
        context['networks'] = network

        return context

# class DetailSpotView(GroupRequiredMixin, DetailView):
#     model = models.Spot
#     template_name = 'protect_network/spot_detail.html'
#     group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
#     context_object_name = 'spot'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         spot = self.get_object()
#         contact_info = models.ContactInfo.objects.filter(spot=spot)
#         opening_hours = models.OpeningHours.objects.filter(spot=spot)
#         images = models.Image.objects.filter(spot=spot).order_by('-id')[:12]
#         spot_types = models.SpotType.objects.filter(spot=spot)
#         survey = models.SecuritySurvey.objects.filter(spot=spot)
#         progress_bar_math = (spot.next_update / spot.spot_type.update_time) * 100
#         progress_bar_math_rounded = round(progress_bar_math)
#         survey_scores = models.SecuritySurvey.objects.filter(spot=spot).aggregate(average_score=Avg('score'))
#         context['spot_progress_bar_math'] = progress_bar_math_rounded
#         context['spot_contacts'] = contact_info
#         context['spot_opening_hours'] = opening_hours
#         context['spot_images'] = images
#         context['spot_types'] = spot_types
#         context['spot_survey'] = survey
#         context['spot_survey_score'] = survey_scores['average_score']
#         return context           


class DetailCardSpotView(GroupRequiredMixin, DetailView):
    model = models.Spot
    template_name = 'protect_network/spot_detail_card.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
    context_object_name = 'spot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot = self.get_object()
        images = models.Image.objects.filter(spot=spot).order_by('-id')[:1]
        context['spot_images'] = images
        return context



@include_toast
class CreateSpotView(GroupRequiredMixin, CreateView):
    model = geo_spot
    form_class = forms.GeoSpotForm
    template_name = 'protect_network/geo_spot_add.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    success_url = reverse_lazy('protect_network:spot_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        self.object.location = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
        user = self.request.user
        self.object.created_by = user
        self.object.updated_by = user
        self.object.updated_at = timezone.now()
        enjoyer = get_object_or_404(portal_models.Enjoyer, user=user)
        entity = enjoyer.entity
        self.object.user_unit = entity
        username = enjoyer
        self.object.user_name = username
        self.object.origin_system=('bacinf')
        self.object.origin_app=('protect_network')
        self.object.save()
        location_value = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
        zipcode_value = form.cleaned_data.get('zipcode')
        city_value = form.cleaned_data.get('city')
        neighborhood_value = form.cleaned_data.get('neighborhood')
        street_value = form.cleaned_data.get('street')
        number_value = form.cleaned_data.get('number')
        complement_value = form.cleaned_data.get('complement')
        reference_value = form.cleaned_data.get('reference')
        address1 = models.Address(
            street=street_value,
            number=number_value,
            complement=complement_value,
            reference=reference_value,
            neighborhood=neighborhood_value,
            city=city_value,
            state="PB",
            region="NE",
            zipcode=zipcode_value,
            place=location_value,
            created_by=self.request.user,
            updated_by=user
        )
        address1.save()
        self.object.addresses.add(address1)
        
        
        spot_type = self.object.spot_type
        spot1 = models.ProtectNetworkSpot(
            spot=self.object,
            update_score=100,
            next_update=spot_type.update_time,
            is_headquarters=form.cleaned_data['is_headquarters'],
            spot_network=form.cleaned_data['spot_network'],
            cnpj=form.cleaned_data['cnpj'],
            parent_company=form.cleaned_data['parent_company'],
            QPP=form.cleaned_data['QPP']
        )
        spot1.save()

        return super().form_valid(form)
    
# @include_toast
# class CreateSpotView(GroupRequiredMixin, CreateView):
#     model = models.Spot
#     form_class = forms.SpotForm
#     template_name = 'protect_network/spot_add.html'
#     group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
#     success_url = reverse_lazy('protect_network:spot_list')

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         latitude = form.cleaned_data['latitude']
#         longitude = form.cleaned_data['longitude']
#         self.object.location = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
#         user = self.request.user
#         self.object.created_by = user
#         self.object.updated_by = user
#         self.object.updated_at = timezone.now()
#         self.object.update_score = 100

#         enjoyer = get_object_or_404(portal_models.Enjoyer, user=user)
#         entity = enjoyer.entity
#         self.object.user_unit = entity

#         username = enjoyer
#         self.object.user_name = username


#         spot_type = self.object.spot_type
#         spot_next_update = spot_type.update_time
        
#         is_headquarters = form.cleaned_data['is_headquarters']
#         self.object.is_headquarters = is_headquarters
#         self.object.next_update = spot_next_update
#         self.object.save()
#         location_value = GEOSGeometry(f"POINT ({longitude} {latitude})", srid=4326)
#         zipcode_value = form.cleaned_data.get('zipcode')
#         city_value = form.cleaned_data.get('city')
#         neighborhood_value = form.cleaned_data.get('neighborhood')
#         street_value = form.cleaned_data.get('street')
#         number_value = form.cleaned_data.get('number')
#         complement_value = form.cleaned_data.get('complement')
#         reference_value = form.cleaned_data.get('reference')
#         address1 = models.Address(street=street_value,number=number_value, complement=complement_value,reference=reference_value, neighborhood=neighborhood_value,
#                                     city=city_value, state="PB", region="NE", zipcode=zipcode_value, place=location_value, created_by=self.request.user,
#                                       updated_by=user)
#         address1.save()
#         self.object.addresses.add(address1)

#         spot1 = geo_spot(name=self.object.name, details=self.object.details, spot_type=self.object.spot_type ,latitude=self.object.latitude,
#                                    longitude=self.object.longitude,created_at=timezone.now(),updated_at=timezone.now(),created_by=user,updated_by=user,is_temporary=self.object.is_temporary,
#                                     date_initial=self.object.date_initial, date_final=self.object.date_final,active=self.object.active,
#                                       location=self.object.location,origin_system="bacinf",origin_app="point_interest",user_name=username,user_unit=entity)
#         spot1.save()
#         return super().form_valid(form)


@include_toast
class UpdateSpotView(GroupRequiredMixin, UpdateView):
    model = models.Spot
    template_name = 'protect_network/spot_update.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
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
    

class SpotListView(GroupRequiredMixin, ListView):
    model = models.ProtectNetworkSpot
    template_name = 'protect_network/spot_list.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(SpotListView, self).get_context_data(**kwargs)
        spot = geo_spot.objects.all()
        network = models.ProtectNetworkSpot.objects.all()
        context['spots'] = spot
        context['networks'] = network
        return context


class SpotListCreatedView(GroupRequiredMixin, ListView):
    model = models.ProtectNetworkSpot
    template_name = 'protect_network/spot_list_created.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(SpotListCreatedView, self).get_context_data(**kwargs)
        spot = geo_spot.objects.all()
        network = models.ProtectNetworkSpot.objects.all()
        context['spots'] = spot
        context['networks'] = network
        return context
    

@include_toast
class CreateSpotTypeView(GroupRequiredMixin, CreateView):
    model = models.geo_spottype
    form_class = forms.SpotTypeForm
    template_name = 'protect_network/spot_type_add.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    success_url = reverse_lazy('protect_network:type_list')


@include_toast
class UpdateSpotTypeView(GroupRequiredMixin, UpdateView):
    model = geo_spottype
    template_name = 'protect_network/spot_type_add.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    form_class = forms.SpotTypeForm
    success_url = reverse_lazy('protect_network:type_list')


class SpotTypeListView(GroupRequiredMixin, ListView):
    model = geo_spottype
    template_name = 'protect_network/spot_type_list.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(SpotTypeListView, self).get_context_data(**kwargs)
        spot_type = geo_spottype.objects.all()
        context['spot_types'] = spot_type
        return context
    

@include_toast
class CreateTagView(GroupRequiredMixin, CreateView):
    model = models.Tag
    form_class = forms.TagForm
    template_name = 'protect_network/tag_add.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    success_url = reverse_lazy('protect_network:tag_list')


@include_toast
class UpdateSpotTagsView(GroupRequiredMixin, UpdateView):
    model = models.Spot
    template_name = 'protect_network/spot_tags_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    form_class = forms.SpotTagsForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        spot_pk = self.object.pk
        return reverse('protect_network:spot_detail', kwargs={'pk': spot_pk})
    


@include_toast
class UpdateTagView(GroupRequiredMixin, UpdateView):
    model = models.Tag
    template_name = 'protect_network/tag_add.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    form_class = forms.TagForm
    success_url = reverse_lazy('protect_network:tag_list')



class TagListView(GroupRequiredMixin, ListView):
    model = models.Tag
    template_name = 'protect_network/tag_list.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        tag = models.Tag.objects.all()
        context['tags'] = tag
        return context
    


@include_toast
class CreateImageSpotView(GroupRequiredMixin, CreateView):
    model = models.Image
    template_name = 'protect_network/spot_image_add.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
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
class ImageDeleteView(GroupRequiredMixin, DeleteView):
    model = models.Image
    template_name = 'protect_network/spot_image_delete.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot_id = self.object.spot.id
        context['spot_id'] = spot_id
        return context
    
    def get_success_url(self):
        spot_id = self.object.spot.id
        return reverse_lazy('protect_network:spot_image_list', kwargs={'spot_id': spot_id})
    

class ImageListView(GroupRequiredMixin, ListView):
    model = models.Image
    template_name = 'protect_network/spot_image_list.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
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
class CreateContactInfoView(GroupRequiredMixin, CreateView):
    model = models.ContactInfo
    template_name = 'protect_network/spot_contact_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
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
class UpdateContactInfoView(GroupRequiredMixin, UpdateView):
    model = models.ContactInfo
    template_name = 'protect_network/spot_contact_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    form_class = forms.ContactInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spot_pk'] = self.object.spot_id
        return context
    
    def get_success_url(self):
        spot_id = self.object.spot_id
        return reverse('protect_network:spot_detail', args=[spot_id])
    
    
@include_toast
class DeleteContactInfoView(GroupRequiredMixin, DeleteView):
    model = models.ContactInfo
    template_name = 'protect_network/spot_contact_delete.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_to_delete'] = self.get_object()
        return context

    def get_success_url(self):
        spot_id = self.object.spot_id
        return reverse('protect_network:spot_detail', args=[spot_id])
    

@include_toast
class CreateOpeningHoursView(GroupRequiredMixin, CreateView):
    model = models.OpeningHours
    template_name = 'protect_network/spot_opening_hours_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
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
class UpdateOpeningHoursView(GroupRequiredMixin, UpdateView):
    model = models.OpeningHours
    template_name = 'protect_network/spot_opening_hours_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
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


@include_toast
class CreateNetworkView(GroupRequiredMixin, CreateView):
    model = models.Network
    form_class = forms.NetworkForm
    template_name = 'protect_network/network_form.html'
    group_required = ['profile:protect_network_manager']
    success_url = reverse_lazy('protect_network:network_list')


@include_toast
class UpdateNetworkView(GroupRequiredMixin, UpdateView):
    model = models.Network
    template_name = 'protect_network/network_form.html'
    group_required = ['profile:protect_network_manager']
    form_class = forms.NetworkForm
    context_object_name = 'network'

    def get_success_url(self):
        return reverse_lazy('protect_network:network_list')



class NetworkListView(GroupRequiredMixin, ListView):
    model = models.Network
    template_name = 'protect_network/network_list.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(NetworkListView, self).get_context_data(**kwargs)
        network = models.Network.objects.all()
        context['networks'] = network
        return context



class NetworkDetailView(GroupRequiredMixin, DetailView):
    model = models.Network
    template_name = 'protect_network/network_detail.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
    context_object_name = 'network'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        network = context['network']
        network_responsibles = network.networkresponsible_set.all()
        context['network_responsibles'] = network_responsibles

        return context
    


@include_toast
class CreateResponsibleView(GroupRequiredMixin, CreateView):
    model = models.NetworkResponsible
    form_class = forms.ResponsibleForm
    template_name = 'protect_network/responsible_form.html'
    group_required = ['profile:protect_network_manager']
    success_url = reverse_lazy('protect_network:network_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        network = get_object_or_404(models.Network, id=self.kwargs['pk'])
        kwargs['network'] = network
        return kwargs

  
class UpdateResponsibleView(GroupRequiredMixin, UpdateView):
    model = models.NetworkResponsible
    template_name = 'protect_network/responsible_form.html'
    group_required = ['profile:protect_network_manager']
    form_class = forms.ResponsibleForm

    def get_success_url(self):
        responsible = self.object
        network_pk = responsible.network.pk
        return reverse_lazy('protect_network:network_detail', kwargs={'pk': network_pk})


class DeleteResponsibleView(GroupRequiredMixin, DeleteView):
    model = models.NetworkResponsible
    template_name = 'protect_network/responsible_delete.html'
    group_required = ['profile:protect_network_manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_to_delete'] = self.get_object()
        return context
    
    def get_success_url(self):
        responsible = self.object
        network_pk = responsible.network.pk
        return reverse_lazy('protect_network:network_detail', kwargs={'pk': network_pk})


@include_toast
class CreateQppView(GroupRequiredMixin, CreateView):
    model = models.Qpp
    form_class = forms.QppForm
    template_name = 'protect_network/qpp_add.html'
    group_required = ['profile:protect_network_manager']
    success_url = reverse_lazy('protect_network:qpp_list')


@include_toast
class UpdateQppView(GroupRequiredMixin, UpdateView):
    model = models.Qpp
    template_name = 'protect_network/qpp_add.html'
    group_required = ['profile:protect_network_manager']
    form_class = forms.QppForm
    success_url = reverse_lazy('protect_network:qpp_list')


class QppListView(GroupRequiredMixin, ListView):
    model = models.Qpp
    template_name = 'protect_network/qpp_list.html'
    group_required = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(QppListView, self).get_context_data(**kwargs)
        qpp = models.Qpp.objects.all()
        context['qpps'] = qpp
        return context
    

@include_toast
class CreateSurveyView(GroupRequiredMixin, CreateView):
    model = models.SecuritySurvey
    form_class = forms.SecuritySurveyForm
    template_name = 'protect_network/survey_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']

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
        response = super().form_valid(form)
        return response

    def post_save(self, instance, created):
        score = 0
        boolean_fields = [
            'security_cameras', 'security_cameras_rec', 'private_security',
            'external_lights', 'alarm_system', 'fire_extinguisher',
            'emergency_out', 'fire_alarm_system', 'security_barriers'
        ]
        for field in boolean_fields:
            value = getattr(instance, field)
            if value:
                score += 10
        instance.score = score
        instance.save()

    def form_valid(self, form):
        spot_id = self.kwargs['spot_id']
        form.instance.spot_id = spot_id
        response = super().form_valid(form)
        self.post_save(self.object, True)

        return response


@include_toast
class UpdateSurveyView(GroupRequiredMixin, UpdateView):
    model = models.SecuritySurvey
    template_name = 'protect_network/survey_form.html'
    group_required = ['profile:protect_network_advanced', 'profile:protect_network_manager']
    form_class = forms.SecuritySurveyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spot_pk'] = self.object.spot_id
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        spot_id = self.kwargs['pk']
        spot = get_object_or_404(models.Spot, pk=spot_id)
        self.object.spot = spot
        score = 0
        boolean_fields = [
            'security_cameras', 'security_cameras_rec', 'private_security',
            'external_lights', 'alarm_system', 'fire_extinguisher',
            'emergency_out', 'fire_alarm_system', 'security_barriers'
        ]
        for field in boolean_fields:
            value = getattr(self.object, field)
            if value:
                score += 10
        self.object.score = score
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        spot_id = self.object.spot_id
        return reverse('protect_network:spot_detail', args=[spot_id])
    

def get_responsibles(request):
    responsibles = portal_models.Military.objects.all()
    data = [{'id': responsible.id, 'text': f"{responsible.rank} {responsible.nickname}"} for responsible in responsibles]
    return JsonResponse(data, safe=False)