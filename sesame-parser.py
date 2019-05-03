# CONLL 2009 format
import os
conll_format = {
    0: 'ID',
    1: 'FORM',
    2: 'LEMMA',
    3: 'PLEMMA',
    4: 'POS',
    5: 'PPOS',
    6: 'FEAT',
    7: 'PFEAT',
    8: 'HEAD',
    9: 'PHEAD',
    10: 'DEPREL',
    11: 'PDEPREL',
    12: 'FILLPRED',
    13: "PRED",
    14: 'APREDS'
}


def _iter_sents(in_file):
    """
    code taken from https://github.com/EmilStenstrom/conllu
    """
    buf = []
    for line in in_file:
        if line == "\n":
            yield "".join(buf)[:-1]
            buf = []
        else:
            buf.append(line)
    if buf:
        yield "".join(buf)


with open(os.path.join('data', 'predicted-args.conll'), 'r', encoding='utf-8') as data:
    for sentence in _iter_sents(data):
        # print(repr(sentence))
        tokenList = []
        for token in sentence.split('\n'):
            formatted_token = {}
            fields = token.split('\t')
            for idx, field in enumerate(fields):
                formatted_token[conll_format[idx]] = field
            tokenList.append(formatted_token)
        print(tokenList)


