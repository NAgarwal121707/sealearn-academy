from urllib.parse import urlparse, parse_qs
from django import template

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """Convert common YouTube URLs to an embeddable URL. Return empty string for non-YouTube URLs."""
    if not url:
        return ''
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower().replace('www.', '')
        video_id = ''
        if host in {'youtu.be'}:
            video_id = parsed.path.strip('/').split('/')[0]
        elif host in {'youtube.com', 'm.youtube.com'}:
            if parsed.path == '/watch':
                video_id = parse_qs(parsed.query).get('v', [''])[0]
            elif parsed.path.startswith('/shorts/') or parsed.path.startswith('/embed/'):
                video_id = parsed.path.strip('/').split('/')[1]
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
    except Exception:
        return ''
    return ''
