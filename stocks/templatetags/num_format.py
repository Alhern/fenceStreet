from django import template

register = template.Library()

@register.filter
def num_format(val, decimals=2):
    """
    Pour convertir les nombres en un format plus lisible (1k, 1m, 1.2b...)
    Usage : val=nombre à convertir, decimals=nombre de chiffres que l'on souhaite avoir après la virgule
    """
    if val == None:
        return val
    int_val = int(val)
    formatted_number = '{{:.{}f}}'.format(decimals)
    if int_val < 1000:  # en dessous de 1000 on renvoie tel quel
        return str(int_val)
    elif int_val < 1000000:
        return formatted_number.format(int_val / 1000.0).rstrip('0').rstrip('.') + 'k'
    elif int_val < 1000000000:
        return formatted_number.format(int_val / 1000000.0).rstrip('0').rstrip('.') + 'm'
    else:
        return formatted_number.format(int_val / 1000000000.0).rstrip('0').rstrip('.') + 'b'
