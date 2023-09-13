from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import ListView
from apps.rpa_manager.models import RiskAssessment, Assessment
from apps.rpa_manager.forms import RiskAssessmentForm, AssessmentForm
from django.urls import reverse
from django.shortcuts import redirect
import weasyprint
from weasyprint import CSS
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


MESSAGE_MODEL_NAME = "Avaliação de risco"

class RiskAssessmentListView(ListView):
    model = RiskAssessment
    template_name = 'rpa_manager/list_risks_analysis.html'  
    context_object_name = 'risk_assessments'

    def get_queryset(self):
        queryset = RiskAssessment.objects.all().order_by('-date')
        return queryset
    
    
class RiskAssessmentDetailView(DetailView):
    model = RiskAssessment
    template_name = 'rpa_manager/detail_risk_assessment.html'
    context_object_name = 'risk_assessment'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessments = Assessment.objects.filter(risk_assessment=self.object)
        context['assessments'] = assessments  

        return context
    
    
class RiskAssessmentCreateView(GroupRequiredMixin, CreateView):
    model = RiskAssessment
    form_class = RiskAssessmentForm
    template_name = 'rpa_manager/create_risk_assessment.html'
    success_url = reverse_lazy('rpa_manager:create_assessment')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'info_responsible': self.request.user}
        return kwargs

    def form_valid(self, form):
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} criada, faça a análise de risco')
        return super().form_valid(form)
    
    


class RiskAssessmentUpdateView(GroupRequiredMixin, UpdateView):
    model = RiskAssessment
    template_name = 'rpa_manager/update_risk_assessment.html'
    form_class = RiskAssessmentForm
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']

    def form_valid(self, form):
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        return super().form_valid(form)
    
    
class RiskAssessmentDeleteView(GroupRequiredMixin, DeleteView):
    model = RiskAssessment
    template_name = 'rpa_manager/delete_risk_assessment.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response
    
    
class AssessmentCreateView(GroupRequiredMixin, CreateView):
    model = Assessment
    template_name = 'rpa_manager/create_assessment.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('rpa_manager:create_assessment')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def form_valid(self, form):
        last_risk_assessment = RiskAssessment.objects.latest('id')
        form.instance.risk_assessment = last_risk_assessment
        
        messages.success(self.request, f'Análise criada com sucesso!')
        return super().form_valid(form)


class AssessmentUpdateView(GroupRequiredMixin, UpdateView):
    model = Assessment
    template_name = 'rpa_manager/update_assessment.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def form_valid(self, form):
        self.object = form.save()
        risk_assessment_pk = self.object.risk_assessment.pk
        redirect_url = reverse('rpa_manager:read_risk_assessment', kwargs={'pk': risk_assessment_pk})
        
        messages.info(self.request, f'Análise editada com sucesso!')
        return redirect(redirect_url)


class AssessmentDeleteView(GroupRequiredMixin, DeleteView):
    model = Assessment
    template_name = 'rpa_manager/delete_assessment.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'Análise excluída com sucesso!')
        return response


class RiskAssessmentPDFDetailView(DetailView):
    model = RiskAssessment
    template_name = 'rpa_manager/generate_risk_asssessment_pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        risk_assessment = self.object
        assessments = risk_assessment.assessment_set.all()
        context['risk_assessment'] = risk_assessment
        context['assessments'] = assessments
        return context

    def render_to_response(self, context, **response_kwargs):
        html = render_to_string(self.template_name, context)
        css = '''
        @page { size: A4; margin: 2cm; }
        body { word-wrap: break-word; }
        '''
        
        pdf_file = weasyprint.HTML(string=html).write_pdf(stylesheets=[CSS(string=css)])
        
        # inline - open in the same page
        # attachment - download
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="risk-assessment.pdf"'

        return response


def duplicate_risk_assessment(request, risk_assessment_id):
    original_risk_assessment = get_object_or_404(RiskAssessment, id=risk_assessment_id)
    
    new_risk_assessment = RiskAssessment.objects.create(
        operational_scenario=f"{original_risk_assessment.operational_scenario} (cópia)",
        date=original_risk_assessment.date,
        expiration_date=original_risk_assessment.expiration_date,
        operator=original_risk_assessment.operator,
        cnpj=original_risk_assessment.cnpj,
        keep_distance_from_3rd=original_risk_assessment.keep_distance_from_3rd,
        pilots_capabilities=original_risk_assessment.pilots_capabilities,
        accident_procedure=original_risk_assessment.accident_procedure,
        info_responsible=original_risk_assessment.info_responsible,
    )

    for assessment in original_risk_assessment.assessment_set.all():
        Assessment.objects.create(
            situation=assessment.situation,
            probability_of_occurrence=assessment.probability_of_occurrence,
            severity_of_occurrence=assessment.severity_of_occurrence,
            risk=assessment.risk,
            hierarchy_authorization=assessment.hierarchy_authorization,
            tolerability=assessment.tolerability,
            mitigation_measures_risk=assessment.mitigation_measures_risk,
            risk_assessment=new_risk_assessment,
        )

    return redirect('rpa_manager:risk_assessment_list')