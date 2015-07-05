from django import template

from django_user_agents.utils import get_and_set_user_agent

register = template.Library()

@register.filter()
def ua(request):
    # return get_and_set_user_agent(request)
    return 'hola'
