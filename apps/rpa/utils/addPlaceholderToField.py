
def addPlaceholder(context, field, value):
    context.fields[field].widget.attrs.update({
    'placeholder': value
    })