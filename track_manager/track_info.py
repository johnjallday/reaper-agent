
import re
from urllib.request import urlopen

def parse_tracks_info():
    """
    Fetch the track list from the local server and return a list of track names.
    Each line starting with 'TRACK' is parsed; the name is taken as the 3rd column,
    which may contain spaces, stopping at the first purely numeric token.
    """
    url = "http://localhost:2307/_/TRACK"
    # Fetch raw track data
    resp = urlopen(url)
    raw = resp.read().decode('utf-8', errors='ignore')
    # Collect all lines beginning with TRACK
    lines = [ln for ln in raw.splitlines() if ln.startswith('TRACK')]
    names = []
    if not lines:
        return names
    # If tab-delimited, simply split on tabs
    if '\t' in lines[0]:
        for ln in lines:
            cols = ln.split('\t')
            if len(cols) >= 3:
                names.append(cols[2].strip())
        return names
    # Otherwise, fallback to whitespace parsing with trailing-field slicing
    num_re = re.compile(r'^-?\d+(?:\.\d+)?$')
    # Determine number of trailing fields by finding a line with a single-token name
    trailing = None
    for ln in lines:
        tokens = ln.split()
        if len(tokens) > 3 and not num_re.match(tokens[2]) and num_re.match(tokens[3]):
            # tokens[2] is name, tokens[3] is first data field
            trailing = len(tokens) - 3
            break
    # Build names list
    if trailing is not None:
        for ln in lines:
            tokens = ln.split()
            # extract tokens[2] up to the start of trailing data
            if len(tokens) >= 2 + trailing:
                parts = tokens[2:len(tokens) - trailing]
            else:
                parts = tokens[2:]
            names.append(' '.join(parts))
    else:
        # fallback to numeric-break detection
        for ln in lines:
            tokens = ln.split()
            parts = []
            for token in tokens[2:]:
                if num_re.match(token):
                    break
                parts.append(token)
            names.append(' '.join(parts))
    return names


if __name__ == "__main__":
    tracks = parse_tracks_info()
    print(tracks)
