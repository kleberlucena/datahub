from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from apps.rpa_manager.models import RiskAssessment, Assessment
from apps.rpa_manager.forms import RiskAssessmentForm, AssessmentForm


class RiskAssessmentCreateView(CreateView):
    model = RiskAssessment
    template_name = 'rpa_manager/create_risk_assessment.html'
    form_class = RiskAssessmentForm
    success_url = reverse_lazy('rpa_manager:create_assessment')


class AssessmentCreateView(CreateView):
    model = Assessment
    template_name = 'rpa_manager/create_assessment.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('rpa_manager:create_assessment')


class RiskAssessmentListView(ListView):
    model = RiskAssessment
    template_name = 'rpa_manager/list_risks_analysis.html'  
    context_object_name = 'risk_assessments'

    def get_queryset(self):
        return RiskAssessment.objects.prefetch_related('assessment')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RiskAssessmentUpdateView(UpdateView):
    model = RiskAssessment
    template_name = 'risk_assessment_form.html'
    form_class = RiskAssessmentForm
    success_url = reverse_lazy('rpa_manager:painel')