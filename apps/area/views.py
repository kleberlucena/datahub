from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView



class IndexView(TemplateView):
    template_name = 'area/index.html'