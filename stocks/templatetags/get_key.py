from django import template

register = template.Library()

# Ce tag permet de récupérer des clés de dico qui contiennent des points (Django et sa notation à point n'apprécient pas)
# Nécessaire pour récupérer les infos sur AV vu que les clés ressemblent à "02. open"
@register.filter
def get_key(val, arg):
    return val.get(arg, None)
