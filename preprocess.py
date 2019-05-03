import xml.etree.ElementTree as elementTree
from xml.etree.ElementTree import  Element

tree = elementTree.parse('data/FATEv09.xml')
root = tree.getroot()
sentences = []
terminal_dict = {}
nonterminals_dict = {}
for sentence in root.iter('s'):
    sentence_id = sentence.attrib
    sentences.append(sentence)
    # print(sentence)
    for terminal in sentence.iter('terminals'):
        for data in terminal.getchildren():
            terminal_dict[data.attrib.get('id')] = data.attrib
    # for nonterminal in sentence.iter('nonterminals'):

    # for sem in sentence.iter('sem'):
    #     print('lol')
print(terminal_dict)
