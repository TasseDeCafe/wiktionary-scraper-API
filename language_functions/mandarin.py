from xpinyin import Pinyin
import jieba


def convert_mandarin_script_to_pinyin(sentence_mandarin):
    segments = jieba.cut(sentence_mandarin)
    output = " ".join(segments)
    p = Pinyin()
    sentence_pinyin = p.get_pinyin(output, splitter='', tone_marks='marks')
    return sentence_pinyin
