from django import template
import logging


register = template.Library()


@register.inclusion_tag('downloader/_display_field.html')
def display_field(field, html_label=False):
    """
    Print HTML for a newform field.
    Optionally, a label can be supplied that overrides the default label generated for the form.

    Example:
    {% display_field form.my_field "My New Label" %}

    Credit: http://lincolnloop.com/blog/2008/mar/13/better-newforms/
    """
    html_label = html_label == "True"

    return { 'field': field,
             'html_label': html_label}