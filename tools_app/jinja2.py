from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment
from markupsafe import Markup, escape

from tools_app.context_preprocessors import debug


def page_link(title):
    escaped = escape(title)
    return Markup(f'<a href="https://en.wikipedia.org/wiki/{escaped}">{escaped}</a>')


def event_link(event):
    escaped = escape(event.timestamp)
    if event.description == 'edit':
        return Markup(f'<a href="http://en.wikipedia.org/wiki/Special:Diff/{event.id}">{event.timestamp}</a>')
    if event.description in ('block', 'reblock', 'unblock', 'newusers', 'create', 'thanks', 'upload'):
        return Markup(f'<a href="http://en.wikipedia.org/w/index.php?title=Special:Log&logid={event.id}">{event.timestamp}</a>')
    else:
        return Markup(f'{event.timestamp}')

def user_link(name):
    escaped = escape(name)
    return Markup(f'<a href="https://en.wikipedia.org/wiki/User:{name}">{name}</a>')


def spi_link(case_name):
    escaped = escape(case_name)
    return Markup(
        f'<a href="https://en.wikipedia.org/wiki/Wikipedia:Sockpuppet investigations/{escaped}">{escaped}</a>')


def contributions(user_name):
    escaped = escape(user_name)
    return Markup(
        f'<a href="https://en.wikipedia.org/wiki/Special:Contributions/{escaped}">contributions</a>')


def deleted_contributions(user_name):
    escaped = escape(user_name)
    return Markup(
        f'<a href="https://en.wikipedia.org/wiki/Special:DeletedContributions/{escaped}">deleted_contributions</a>')


def environment(**options):
    env = Environment(**options)
    env.globals.update({
	'static': static,
	'url': reverse,
        'debug_data': debug,
    })
    env.filters.update({
        'page_link': page_link,
        'event_link': event_link,
        'user_link': user_link,
        'spi_link': spi_link,
        'contributions': contributions,
        'deleted_contributions': deleted_contributions,
    })
    return env
