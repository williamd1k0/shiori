
import re
import os

PATTERNS_PATHS = [
    'nintendo_3ds'
]

def load_patterns():
    patterns = []
    for p in PATTERNS_PATHS:
        ap = os.path.join(os.path.dirname(os.path.realpath(__file__)), p)
        files = [os.path.join(ap, name) for name in os.listdir(ap)]
        for txt in files:
            with open(txt, encoding='utf-8') as f:
                words = f.read().strip().split('\n')
                patterns.append('|'.join(words))
    return re.compile('|'.join(patterns))

def get_badwords(r, text):
    return r.search(text)


def main(args):
    if len(args) > 1:
        r = load_patterns()
        badwords = get_badwords(r, ' '.join(args[1:]))
        if badwords:
            print('Text contains bad words')
        else:
            print('Text is safe')

if __name__ == '__main__':
    import sys
    main(sys.argv)
