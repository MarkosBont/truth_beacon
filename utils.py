import urllib.parse
import base64
import tldextract

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
    parsed_url = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed_url.query)

    if 'u' in query:
        encoded_url = query['u'][0]

        if not encoded_url.startswith("http"):
            try:
                decoded_bytes = base64.b64decode(encoded_url)
                decoded_url = decoded_bytes.decode("utf-8")
                return decoded_url
            except Exception:
                pass

        return urllib.parse.unquote(encoded_url)

    return url  # Return the original if no 'u' param is found