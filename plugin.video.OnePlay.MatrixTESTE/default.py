import base64; xor = lambda x, k: ''.join(chr(ord(c) ^ ord(k[i % len(k)])) for i, c in enumerate(x)); exec(xor(base64.b64decode('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').decode(), 'musk'))