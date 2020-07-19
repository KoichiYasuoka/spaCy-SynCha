[![Current PyPI packages](https://badge.fury.io/py/spacy_syncha.svg)](https://pypi.org/project/spacy_syncha/)

# spaCy-SynCha

SynCha-CaboCha-MeCab wrapper for spaCy

## Basic Usage

```py
>>> import spacy_syncha
>>> nlp=spacy_syncha.load()
>>> doc=nlp("私の名前は中野です。")
>>> for t in doc:
...   print(t.i,t.orth_,t.lemma_,t.pos_,t.tag_,t.head.i,t.dep_,t.norm_,t.ent_iob_,t.ent_type_)
...
0 私 私 PRON 名詞-代名詞-一般 2 nmod ワタシ O
1 の の ADP 助詞-連体化 0 case ノ O
2 名前 名前 NOUN 名詞-一般 4 nsubj ナマエ O
3 は は ADP 助詞-係助詞 2 case ハ O
4 中野 中野 PROPN 名詞-固有名詞-地域-一般 4 ROOT ナカノ B LOCATION
5 です です AUX 助動詞 4 cop デス O
6 。 。 PUNCT 記号-句点 4 punct 。 O
```

## Installation for Linux

Make sure to pre-install SynCha, CaboCha, and MeCab:

```sh
pip install spacy_syncha
```

## Installation for Cygwin

Make sure to get `python37-devel` `python37-pip` `python37-cython` `python37-numpy` `git` `gcc-g++` `perl`:

```sh
pip3.7 install git+https://github.com/KoichiYasuoka/syncha-cygwin
pip3.7 install spacy_syncha --no-build-isolation
```

