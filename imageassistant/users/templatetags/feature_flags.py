from django import template

register = template.Library()

@register.simple_tag
def has_feature_flag(user, flag_name):
    if user.is_authenticated:
        return user.featureflag_set.filter(name=flag_name).exists()
    return False