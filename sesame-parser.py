import os
import nltk


# CONLL 2009 format
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


class Parser:

    def __init__(self):
        self.sentences = []
        self.frames = []
        self.elements = []
        self.index_dict = {}
        self.load_data()

    @staticmethod
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

    def load_data(self):
        with open(os.path.join('data', 'predicted-args.conll'), 'r', encoding='utf-8') as data:
            index = 0
            for sentence in self._iter_sents(data):
                words = []
                # print(repr(sentence))
                fe_flag = 0    # flag to track phrases
                phrase = []
                frame_elements = []
                for token in sentence.split('\n'):
                    formatted_token = {}
                    fields = token.split('\t')
                    for idx, field in enumerate(fields):
                        formatted_token[conll_format[idx]] = field
                    frame = formatted_token['PRED']
                    target = formatted_token['FILLPRED'].split('.')[0]
                    word = formatted_token['FORM']
                    # lemma = formatted_token['PLEMMA']
                    if not frame == '_':
                        self.frames.append({frame: target})
                    fe = formatted_token['APREDS'].split('-')
                    if fe_flag:
                        if not fe[0] == 'O':
                            phrase.append(word)
                        else:
                            frame_elements.append({element: ' '.join(phrase)})
                            fe_flag = 0
                            phrase = []
                    if fe[0] == 'B':
                        fe_flag = 1
                        element = fe[1]
                        phrase.append(word)
                    elif fe[0] == 'S':
                        frame_elements.append({fe[1]: word})
                    words.append(word)
                sent = ' '.join(words)
                if sent in self.index_dict.keys():
                    value = self.index_dict[sent]
                    value.append(index)
                else:
                    self.index_dict[sent] = [index]
                self.sentences.append(words)
                self.elements.append(frame_elements)
                index += 1
        # print(self.sentences)
        # print(self.frames)
        # print(self.elements)

    def get_data(self, sentence):
        words = nltk.word_tokenize(sentence.lower())
        sent = ' '.join(words)
        frames = []
        frame_element_list = []
        indexes = self.index_dict.get(sent)
        if indexes:
            for idx in indexes:
                f = self.frames[idx]
                if f not in frames:
                    frames.append(f)
                frame_ele = self.elements[idx]
                if frame_ele not in frame_element_list:
                    frame_element_list.append(frame_ele)
        return frames, frame_element_list


parser = Parser()
frame, fes = parser.get_data("This galaxy was dubbed the Sagittarius Dwarf galaxy ( as it , and the core of the Milky "
                             "Way , lie in the constellation Sagittarius ) , and until recently , it held the record "
                             "for the nearest galaxy , at about 70,000 light years away.")
print(frame)
print(fes)
