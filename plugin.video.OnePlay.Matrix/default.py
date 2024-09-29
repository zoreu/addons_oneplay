import base64; xor = lambda x, k: ''.join(chr(ord(c) ^ ord(k[i % len(k)])) for i, c in enumerate(x)); exec(xor(base64.b64decode('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').decode(), 'musk'))