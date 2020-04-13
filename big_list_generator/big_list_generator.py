import pandas as pd 
import jieba
import re


def clean_big_list(df):
    df = df.rename(columns={'Unnamed: 3': 'Chinese keyword'})
    return df


def clean_conversations(df):
    df = df.rename(columns={'Chinese - Sentence': 'Chinese sentence'})
    return df


def get_unique_words_conversations(df):
    df = df.dropna(axis=0, subset=['Chinese sentence'])
    # tokenize the sentences
    chinese_sentences = df['Chinese sentence'].apply(jieba.cut)
    chinese_sentences = chinese_sentences.apply(list)
    unique_words = set([word for sublist in chinese_sentences for word in sublist])
    # remove numbers from the list
    unique_words_no_integers = {x for x in unique_words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())}
    # remove latin words from the list
    unique_words_no_integers_latin = {x for x in unique_words_no_integers if x not in re.findall('[a-zA-Z]+', x)}
    punctuation_signs = ", ！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
    # remove special characters from the list
    unique_words_no_special_char = {x for x in unique_words_no_integers_latin if x not in punctuation_signs}
    return unique_words_no_special_char


def get_unique_words_big_list(df):
    df = df.dropna(axis=0, subset=['Chinese keyword'])
    big_list_words = set(df['Chinese keyword'])
    return big_list_words


def get_matching_sentences(words, df):
    list_matching_sentences = []
    for word in words:
        matching_sentences = [sentence for sentence in df['Chinese sentence'].dropna() if word.strip() in sentence]
        list_matching_sentences.append(matching_sentences)
    first_matching_sentences = [sentences[0] if sentences else '' for sentences in list_matching_sentences]
    return first_matching_sentences


def generate_big_list(df):
    # get the list of unique words in the conversations sheet
    conversations_unique_words = get_unique_words_conversations(df)
    # get the list of unique words in the big list sheet
    big_list_words = get_unique_words_big_list(df)
    # get the words and sentences from the conversations that are not in the big list
    intersection = conversations_unique_words.intersection(big_list_words)
    new_unique_words = conversations_unique_words - intersection
    matching_sentences = get_matching_sentences(new_unique_words, df)
    # generate the final csv final
    dataframe_new_words = pd.DataFrame(list(zip(new_unique_words, matching_sentences)), columns=['Keyword', 'Sentence'])
    # flip the columns
    dataframe_new_words = dataframe_new_words[['Sentence', 'Keyword']]
    dataframe_new_words.to_csv('dataframe_new_words.csv')
    return dataframe_new_words


if __name__ == '__main__':
    pass
    # generate_big_list()

