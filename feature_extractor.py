import nltk
from nltk.corpus import wordnet
from nltk.corpus import framenet as fn
"""
responsible for extracting features:
feature 1: no of words that match.
feature 2: no of frames that match.
feature 3: no of targets that match in the matched frames.
feature 4: no of frame elements that match.
feature 5: no of value of frame elements that match in the matched frame element.
"""


def extract_features(file=None):
    with open(file) as data:
        features = []
        for text, hypothesis in data:
            feature_vector = []
            # count the number of words that match
            no_of_word_match = 0
            for word1 in text.words:
                for word2 in hypothesis.words:
                    no_of_word_match += compare_words(word1, word2)
            feature_vector.append(no_of_word_match)

            # count the frames that match
            no_of_frames_match = 0
            no_of_target_match = 0
            no_of_elements_match = 0
            no_of_roles_match = 0
            for frame1 in text.frames:
                for frame2 in hypothesis.frames:
                    no_of_frames_match += compare_frames(frame1, frame2)
                    no_of_target_match += compare_words(frame1.target, frame2.target)
            feature_vector.append(no_of_frames_match)
            feature_vector.append(no_of_target_match)

        print(compare_words("find", "discover"))
        # with open(file) as data:


def compare_words(word1, word2):
    if word1 == word2:
        return 2
    synsets = wordnet.synsets(word1)
    lemmas = []
    for ss in synsets:
        lemmas.extend([str(lemma.name()) for lemma in ss.lemmas()])
    print(lemmas)
    if word2 in lemmas:
        return 1
    else:
        return 0


def compare_frames(frame1, frame2):
    if frame1 == frame2:
        return 2
    frame_relations = []
    for relation in fn.frame(frame1).frameRelations:
        frame_relations.extend([relation.superFrameName.lower(), relation.subFrameName.lower()])
    print(frame_relations)
    if frame2 in frame_relations:
        return 1
    else:
        return 0


extract_features()
# print(compare_frames("surviving", "killing"))


