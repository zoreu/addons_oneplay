import base64; xor = lambda x, k: ''.join(chr(ord(c) ^ ord(k[i % len(k)])) for i, c in enumerate(x)); exec(xor(base64.b64decode('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').decode(), 'musk'))