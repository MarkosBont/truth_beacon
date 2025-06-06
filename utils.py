import urllib.parse
import base64
import tldextract
import re

def get_source_name_from_url(url):
    try:
        # Extracting the domain
        ext = tldextract.extract(url)
        if ext.domain:
            return ext.domain.capitalize()
        return "Source"
    except Exception:
        return "Source"


def extract_real_url(url):
    if not url or not isinstance(url, str):
        return None

    try:
        parsed_url = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed_url.query)

        if 'u' in query:
            encoded_url = query['u'][0]

            # Try Base64 decode if it looks like one (A-Za-z0-9+/= and decent length)
            if re.fullmatch(r'[A-Za-z0-9+/=]+', encoded_url) and len(encoded_url) > 20:
                try:
                    decoded_bytes = base64.b64decode(encoded_url)
                    decoded_url = decoded_bytes.decode("utf-8")
                    if decoded_url.startswith("http"):
                        return decoded_url
                except Exception:
                    pass

            # Otherwise, assume it's URL-encoded
            decoded_url = urllib.parse.unquote(encoded_url)
            return decoded_url if decoded_url.startswith("http") else None

        # No 'u' param — check if it's already a real URL
        return url if url.startswith("http") else None

    except Exception:
        return None