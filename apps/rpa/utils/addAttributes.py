
def addAttributes(this_obj, field, attrs1 = '', attrs2 = '', attrs3 = ''):
    this_obj.fields[field].widget.attrs.update({
        'class': str(attrs1) + '_escolha ' +  str(attrs2) + str(attrs3)
    })
