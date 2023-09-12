from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import ListView
from apps.rpa_manager.models import RiskAssessment, Assessment
from apps.rpa_manager.forms import RiskAssessmentForm, AssessmentForm
from django.urls import reverse
from django.shortcuts import redirect
import weasyprint
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import HttpResponse


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
    
    
class RiskAssessmentCreateView(CreateView):
    model = RiskAssessment
    template_name = 'rpa_manager/create_risk_assessment.html'
    form_class = RiskAssessmentForm
    success_url = reverse_lazy('rpa_manager:create_assessment')


class RiskAssessmentListView(ListView):
    model = RiskAssessment
    template_name = 'rpa_manager/list_risks_analysis.html'  
    context_object_name = 'risk_assessments'


class RiskAssessmentUpdateView(UpdateView):
    model = RiskAssessment
    template_name = 'rpa_manager/update_risk_assessment.html'
    form_class = RiskAssessmentForm
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')


class RiskAssessmentDeleteView(DeleteView):
    model = RiskAssessment
    template_name = 'rpa_manager/delete_risk_assessment.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')


class AssessmentCreateView(CreateView):
    model = Assessment
    template_name = 'rpa_manager/create_assessment.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('rpa_manager:create_assessment')

    def form_valid(self, form):
        last_risk_assessment = RiskAssessment.objects.latest('id')
        form.instance.risk_assessment = last_risk_assessment
        return super().form_valid(form)


class AssessmentUpdateView(UpdateView):
    model = Assessment
    template_name = 'rpa_manager/update_assessment.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')

    def form_valid(self, form):
        self.object = form.save()
        risk_assessment_pk = self.object.risk_assessment.pk
        redirect_url = reverse('rpa_manager:read_risk_assessment', kwargs={'pk': risk_assessment_pk})
        
        return redirect(redirect_url)


class AssessmentDeleteView(DeleteView):
    model = Assessment
    template_name = 'rpa_manager/delete_assessment.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:risk_assessment_list')


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
        
        image_base_path = "/home/marcosdev/Documentos/Programacao/Projetos/bacinf/apps/rpa_manager/templates/rpa_manager/"
        
        pdf_file = weasyprint.HTML(string=html, base_url=image_base_path).write_pdf(stylesheets=[CSS(string=css)])
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="risk-assessment.pdf"'

        return response
    