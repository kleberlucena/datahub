from django.contrib import messages


def include_toast(cls):
    if hasattr(cls, 'form_valid'):
        original_form_valid = cls.form_valid
        
        def form_valid(self, form):
            response = original_form_valid(self, form)
            messages.success(self.request, 'Formulário salvo com sucesso')
            return response
        
        cls.form_valid = form_valid
        
    if hasattr(cls, 'form_invalid'):
        original_form_invalid = cls.form_invalid
        
        def form_invalid(self, form):
            response = original_form_invalid(self, form)
            for erro in form.errors:
                messages.error(
                    self.request,
                    'Falha na operação, provavelmente no campo {}'.format(erro)
                )
            messages.error(self.request, 'Por favor, verifique os campos')
            return response
        
        cls.form_invalid = form_invalid
        
    if hasattr(cls, 'delete'):
        original_delete = cls.delete    
        
        def delete(self, request, *args, **kwargs):
            response = original_delete(self, request, *args, **kwargs)
            messages.info(self.request, 'Registro deletado com sucesso')
            return response
        
        cls.delete = delete

    return cls

