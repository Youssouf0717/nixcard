def normalize_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith("http"):
        return "https://" + url
    return url