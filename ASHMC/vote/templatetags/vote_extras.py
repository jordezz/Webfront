from django import template
from django.utils.safestring import mark_safe

from random import shuffle as rshuffle

register = template.Library()


@register.filter
def get_candidate(ballot, choice):
    candidates = ballot.candidate_set.filter(title=choice.choice_label)

    if len(candidates) != 1:
        return ""

    return candidates[0]


@register.filter
def get_valid_candidates(ballot):
    return ballot.candidate_set.all().exclude(is_write_in=True)


@register.filter
def shuffle(queryset):
    if isinstance(queryset, list):
        new_list = queryset[:]
        rshuffle(new_list)
        return new_list

    return queryset.order_by('?')


@register.filter
def irvqs_to_candidate(qs, candidate):
    try:
        return qs.filter(candidate=candidate)[0]
    except IndexError:
        return None


@register.filter
def dir_this(thing):
    return dir(thing)


@register.filter
def prettify_error_listings(error_dict, ballot_id):
    try:
        errors = error_dict[ballot_id]
    except KeyError:
        return ''

    response = """<ul class='errors'>"""

    for key, values in errors.iteritems():
        if key != "__all__":
            response += """<li>"""
            response += """{}<ul>""".format(key)

        for error in values:
            response += """<li>{}</li>""".format(error)

        if key != "__all__":
            response += """</ul>"""
            response += """</li>"""

    response += """</ul>"""

    return mark_safe(response)
