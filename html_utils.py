import bleach


def strip_html(html: str):
    """
    a wrapper for bleach.clean() that strips ALL tags from the input
    """
    tags = []
    attr = {}
    styles = []
    strip = True
    return bleach.clean(html,
                        tags=tags,
                        attributes=attr,
                        styles=styles,
                        strip=strip)
