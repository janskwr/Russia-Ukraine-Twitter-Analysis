import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import copy
import matplotlib
from matplotlib.pyplot import figure
# matplotlib.use('Agg')
import csv

import streamlit.components.v1 as components


# def _max_width_(prcnt_width:int = 125):
#     max_width_str = f"max-width: {prcnt_width}%;"
#     st.markdown(f"""
#                 <style>
#                 .reportview-container .main .block-container{{{max_width_str}}}
#                 </style>
#                 """,
#                 unsafe_allow_html=True,
#     )


@st.cache(allow_output_mutation=True)
def load_data():
    names_counts = ['../counts/feb21_counts.csv',
                    '../counts/feb22_counts.csv',
                    '../counts/feb23_counts.csv',
                    '../counts/feb24_counts.csv',
                    '../counts/feb25_counts.csv',
                    '../counts/feb26_counts.csv',
                    '../counts/feb27_counts.csv',
                    '../counts/feb28_counts.csv',
                    '../counts/mar01_counts.csv',
                    '../counts/mar02_counts.csv',
                    '../counts/mar03_counts.csv']
    l = []
    for name in names_counts:

        d = {}
        data_tmp = pd.read_csv(name, sep=',', encoding='utf-8', names=['ngram', 'num'])

        for i, row in data_tmp.iterrows():
            d[row['ngram']] = row['num']
        l.append(Counter(d))

    all_l = Counter()
    for el in l:
        all_l += el

    return l, all_l


@st.cache(allow_output_mutation=True)
def load_data_bigrams():
    names_counts = ['../bigrams/feb21_bigrams.csv',
                    '../bigrams/feb22_bigrams.csv',
                    '../bigrams/feb23_bigrams.csv',
                    '../bigrams/feb24_bigrams.csv',
                    '../bigrams/feb25_bigrams.csv',
                    '../bigrams/feb26_bigrams.csv',
                    '../bigrams/feb27_bigrams.csv',
                    '../bigrams/feb28_bigrams.csv',
                    '../bigrams/mar01_bigrams.csv',
                    '../bigrams/mar02_bigrams.csv',
                    '../bigrams/mar03_bigrams.csv']
    l = []
    for name in names_counts:
        # print(name)
        d = {}
        data_tmp = pd.read_csv(name, sep=',', encoding='utf-8', names=['ngram', 'num'], quoting=csv.QUOTE_NONE)

        for i, row in data_tmp.iterrows():
            d[row['ngram']] = row['num']
        l.append(Counter(d))

    all_l = Counter()
    for el in l:
        all_l += el

    return l, all_l


def plot_all_time(start, stop, data, all_l, option_date, filter_words):
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 6)
    x = ['feb21', 'feb22', 'feb23', 'feb24', 'feb25', 'feb26', 'feb27', 'feb28', 'mar01', 'mar02', 'mar03']

    from_tmp = copy.deepcopy(x)
    from_tmp.append('all time')
    hehe = all_l

    which_counter = from_tmp.index(option_date)

    if which_counter != 11:
        hehe = data[which_counter]

    filter_words = filter_words.split(',')
    for i, l in enumerate(filter_words):  # wybieramy tylko wyrazy
        filter_words[i] = l.lower().strip()

    b = hehe.most_common()
    nb = []

    for w in b:
        dodaj = True
        for w2 in filter_words:

            if w2 in str(w[0]).lower().split():
                dodaj = False
        if dodaj:
            nb.append(w)

    for el in nb[start: stop]:
        y = []
        for k in data:
            y.append(k.get(el[0]))

        ax.plot(x, y, label=el[0] + " " + str(int(el[1])))

    plt.legend()
    ax.legend(bbox_to_anchor=(1.01, 1))

    col1, col2 = st.columns([5, 1])
    col1.pyplot(fig)


def plot_without_all(start, stop, data, all_l, option_date, filter_words):
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 6)
    x = ['feb21', 'feb22', 'feb23', 'feb24', 'feb25', 'feb26', 'feb27', 'feb28', 'mar01', 'mar02', 'mar03']

    from_tmp = copy.deepcopy(x)
    from_tmp.append('all time')
    hehe = all_l

    which_counter = from_tmp.index(option_date)

    filter_words = filter_words.split(',')
    for i, l in enumerate(filter_words):  # wybieramy tylko wyrazy
        filter_words[i] = l.lower().strip()

    if which_counter != 11:
        hehe = data[which_counter]

    a = all_l.most_common(50)
    for i, l in enumerate(a):  # wybieramy tylko wyrazy
        a[i] = l[0].lower()

    b = hehe.most_common()
    nb = []

    for w in b:
        if str(w[0]).lower() not in a:
            nb.append(w)

    nb2 = []

    for w in nb:

        dodaj = True

        for w2 in filter_words:

            if w2 in str(w[0]).lower().split():
                dodaj = False

        if dodaj:
            nb2.append(w)

    for el in nb2[start: stop]:
        y = []
        for k in data:
            y.append(k.get(el[0]))
        plt.plot(x, y, label=el[0] + " " + str(int(el[1])))

    plt.legend()
    ax.legend(bbox_to_anchor=(1.01, 1))

    col1, col2 = st.columns([5, 1])
    col1.pyplot(fig)


st.title('Twitter exploration tool')
st.header('Numerosity based')

data, all_l = load_data()

data_b, all_b = load_data_bigrams()

st.subheader('All time trends')
st.write('Plots most popular words')

option_gram_1 = st.selectbox(
    'Type of n-grams:',
    ('unigrams', 'bigrams'), key='g1')

option_date = st.selectbox(
    'Most popular in:',
    ('all time', 'feb21', 'feb22', 'feb23', 'feb24', 'feb25', 'feb26', 'feb27', 'feb28', 'mar01', 'mar02', 'mar03'),
    key='primary')

filter_words_1 = st.text_input('Filter words (comma separated):', value='the, this, a', key='first_filter')

slider_range = st.slider('Top ngrams:', min_value=1, max_value=100, value=[1, 10], key='slider1')

if option_gram_1 == 'unigrams':
    plot_all_time(slider_range[0] - 1, slider_range[1], data, all_l, option_date, filter_words_1)
else:
    plot_all_time(slider_range[0] - 1, slider_range[1], data_b, all_b, option_date, filter_words_1)

st.subheader('Specific day trends')
st.write('Plots most popular words for certain date excluding 50 most popular words of all time')

option_gram_2 = st.selectbox(
    'Type of n-grams:',
    ('unigrams', 'bigrams'), key='g2')

option_date_2 = st.selectbox(
    'Most popular in:',
    ('feb21', 'feb22', 'feb23', 'feb24', 'feb25', 'feb26', 'feb27', 'feb28', 'mar01', 'mar02', 'mar03'),
    key='secondary')

filter_words = st.text_input('Filter words (comma separated):', value='the, this, a', key='second_filter')

slider_range = st.slider('Top ngrams:', min_value=1, max_value=100, value=[1, 10], key='slider2')

if option_gram_2 == 'unigrams':
    plot_without_all(slider_range[0] - 1, slider_range[1], data, all_l, option_date_2, filter_words)
else:
    plot_without_all(slider_range[0] - 1, slider_range[1], data_b, all_b, option_date_2, filter_words)

st.header('BERTopic')

p1 = open("bar.html")
components.html(p1.read(), height=500, width=1500)

p2 = open("hierarchy.html")
components.html(p2.read(), height=7700, width=1500)

p3 = open("time.html")
components.html(p3.read(), height=400, width=1500)
