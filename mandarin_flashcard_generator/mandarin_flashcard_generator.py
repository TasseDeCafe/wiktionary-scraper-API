# goal: create a tool that can clean up the data from my Chinese lessons. This includes
# - adding pinyin to the keywords and sentences - OK
# - adding capital letters to all the words and sentences in English - OK
# - remove lines without a keyword - OK
# - add example sentence to keywords if there is a sentence with the keyword - OK
# - remove google translate column for the sentences - OK
# - remove header - OK
# - remove lines that need clarification from native speaker (lines with "--") - OK
# - remove comments - OK
# - add punctuation when necessary - OK
# - add TTS : https://pypi.org/project/gTTS/

import pandas as pd
from xpinyin import Pinyin
import re
import jieba
import numpy as np


def convert_mandarin_script_to_pinyin(sentence_mandarin):
    segments = jieba.cut(sentence_mandarin)
    output = " ".join(segments)
    p = Pinyin()
    sentence_pinyin = p.get_pinyin(output, splitter='', tone_marks='marks')
    return sentence_pinyin


def add_pinyin_columns(df):
    p = Pinyin()
    # generate pinyin column for the keywords
    column_pinyin_keyword = df['Keyword in Chinese'].apply(lambda x: convert_mandarin_script_to_pinyin(x) if pd.notnull(x) else x)
    # add column to the dataframe
    df['Pinyin of keyword'] = column_pinyin_keyword

    # generate pinyin column for the sentences
    column_pinyin_keyword = df['Sentence in Chinese'].apply(lambda x: convert_mandarin_script_to_pinyin(x) if pd.notnull(x) else x)
    # add column to the dataframe
    df['Pinyin of sentence'] = column_pinyin_keyword
    return df


def remove_roman_characters(cell_content):
    cell_no_roman_characters = re.sub('\([a-zA-Z0-9 ]+\)', '', cell_content)
    cell_no_roman_characters = re.sub('[A-z0-9]+', '', cell_no_roman_characters)
    return cell_no_roman_characters


def remove_roman_characters_column(df):
    column_mandarin_keyword = df['Keyword in Chinese']
    column_no_roman_characters = column_mandarin_keyword.apply(lambda x: remove_roman_characters(x) if pd.notnull(x) else x)
    df['Keyword in Chinese'] = column_no_roman_characters
    return df


def drop_lines_without_keyword(df):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.dropna(axis=0, subset=['Keyword in Chinese'])
    df = df.reset_index(drop=True)
    return df


def add_example_sentences(df):
    list_matching_sentences = []
    for word in df['Keyword in Chinese']:
        if not isinstance(word, float):
            matching_sentences = [sentence for sentence in df['Sentence in Chinese'].dropna() if word.strip() in sentence]
            list_matching_sentences.append(matching_sentences)
    first_matching_sentences = [sentences[0] if sentences else '' for sentences in list_matching_sentences]

    mandarin_sentences_complete = [original_sentence if not pd.isnull(original_sentence) else sentence for original_sentence, sentence in zip(df['Sentence in Chinese'], first_matching_sentences)]
    df['Sentence in Chinese'] = mandarin_sentences_complete
    return df


def remove_google_translate_column(df):
    df = df.drop('Sentence in English', axis=1)
    return df


def capitalize(df):
    df['Keyword in English'] = df['Keyword in English'].str.capitalize()
    return df


def add_punctuation_to_string(sentence):
    if sentence and sentence[-1] not in ('？。'):
        sentence += '。'
    return sentence


def add_punctuation(df):
    df['Sentence in Chinese'] = df['Sentence in Chinese'].apply(add_punctuation_to_string)
    return df


def remove_questions(df):
    df = df[~df['Sentence in Chinese'].str.contains('--')]
    df = df.reset_index(drop=True)
    return df

def reorder_dataframe(df):
    df = df[['Keyword in Chinese', 'Pinyin of keyword', 'Sentence in Chinese', 'Pinyin of sentence', 'Keyword in English']]
    return df


def remove_headers(df):
    df.to_csv('chinese_clean.csv', header=False, index=False)
    return df


def generate_dataframe(df):
    df = remove_roman_characters_column(df)
    df = drop_lines_without_keyword(df)
    df = add_example_sentences(df)
    df = add_punctuation(df)
    df = add_pinyin_columns(df)
    df = remove_google_translate_column(df)
    df = capitalize(df)
    df = remove_questions(df)
    df = reorder_dataframe(df)
    # df = remove_headers(df)
    return df


if __name__ == '__main__':
    data = pd.read_csv("..\mandarin_flashcards.csv")
    data = generate_dataframe(data)
    print(data)
