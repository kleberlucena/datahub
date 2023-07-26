from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from apps.rpa_manager.models import Guarnicao, CidadesPB
from apps.rpa_manager.forms import GuarnicaoForm
from datetime import date

class GuarnicaoCreateView(CreateView):
    model = Guarnicao
    form_class = GuarnicaoForm
    template_name = 'controle/pages/guarnicao_register.html'
    success_url = reverse_lazy('rpa_manager:checklist_form')


class GuarnicaoListView(ListView):
    model = Guarnicao
    template_name = 'controle/pages/checklist_form.html'
    context_object_name = 'guarnicoes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['localidades'] = CidadesPB.objects.all()
        return context
    
    def get_queryset(self):
        local_id = self.request.GET.get('local', None)
        return Guarnicao.objects.filter(local_id=local_id, data__date=date.today())
