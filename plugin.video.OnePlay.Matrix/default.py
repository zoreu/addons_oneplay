import base64; xor = lambda x, k: ''.join(chr(ord(c) ^ ord(k[i % len(k)])) for i, c in enumerate(x)); exec(xor(base64.b64decode('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').decode(), 'musk'))