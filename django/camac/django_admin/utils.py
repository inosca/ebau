from django.utils.html import format_html


def display_color(color):
    return format_html(f"<span style='color: {color}'>⯀</span>")
