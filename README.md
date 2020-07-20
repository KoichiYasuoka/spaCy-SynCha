[![Current PyPI packages](https://badge.fury.io/py/spacy-syncha.svg)](https://pypi.org/project/spacy-syncha/)

# spaCy-SynCha

SynCha-CaboCha-MeCab wrapper for spaCy

## Basic Usage

```py
>>> import spacy_syncha
>>> nlp=spacy_syncha.load()
>>> doc=nlp("太郎は花子が読んでいる本を次郎に渡した")
>>> for t in doc:
...   print(t.i,t.orth_,t.lemma_,t.pos_,t.tag_,t.head.i,t.dep_,t.norm_,t.ent_iob_,t.ent_type_)
...
0 太郎 太郎 PROPN 名詞-固有名詞-人名-名 12 nsubj タロウ B PERSON
1 は は ADP 助詞-係助詞 0 case ハ O
2 花子 花子 PROPN 名詞-固有名詞-人名-名 4 nsubj ハナコ B PERSON
3 が が ADP 助詞-格助詞-一般 2 case ガ O
4 読ん 読む VERB 動詞-自立 7 acl ヨン O
5 で で CCONJ 助詞-接続助詞 4 mark デ O
6 いる いる AUX 動詞-非自立 4 aux イル O
7 本 本 NOUN 名詞-一般 12 obj ホン O
8 を を ADP 助詞-格助詞-一般 7 case ヲ O
9 次 次 NOUN 名詞-一般 10 compound ツギ O
10 郎 郎 NOUN 名詞-一般 12 iobj ロウ O
11 に に ADP 助詞-格助詞-一般 10 case ニ O
12 渡し 渡す VERB 動詞-自立 12 ROOT ワタシ O
13 た た AUX 助動詞 12 aux タ O
```

## Installation for Linux (Debian)

First, install [MeCab](https://taku910.github.io/mecab/) and necessary packages:

```sh
sudo apt update
sudo apt install mecab libmecab-dev mecab-ipadic-utf8 python3-pip python3-dev g++ make curl lp-solve
cd /tmp
curl -L 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ' | tar xzf -
cd CRF++-0.58
./configure --prefix=/usr
make && sudo make install
```

Second, install [CaboCha](https://taku910.github.io/cabocha/):

```sh
cd /tmp
curl -sc cabocha.cookie 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU' > /dev/null
curl -Lb cabocha.cookie 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU&confirm='`tr -d '\015' < cabocha.cookie | awk '/_warning_/{print $NF}'` | tar xjf -
cd cabocha-0.69
./configure --prefix=/usr --with-charset=UTF8
make && sudo make install
```

Third, install [SynCha](https://sites.google.com/site/ryuiida/syncha):

```sh
cd /tmp
curl -L 'https://drive.google.com/uc?export=download&id=0B4wOZ_esMVcMazQ0eGdtMnBCaWs' | tar xzf -
sudo mkdir -p /usr/local/bin
sudo mv syncha-0.3.1.1 /usr/local/syncha
( echo '#! /bin/sh' ; echo 'exec /usr/local/syncha/syncha "$@"' ) > syncha
chmod 755 syncha
sudo mv syncha /usr/local/bin
```

And last, install spaCy-SynCha:

```sh
pip3 install spacy_syncha --user
```

## Installation for Linux (Ubuntu)

Same as Debian.

## Installation for Linux (Kali)

Same as Debian.

## Installation for Cygwin

Make sure to get `python37-devel` `python37-pip` `python37-cython` `python37-numpy` `git` `gcc-g++` `perl`, and then:

```sh
pip3.7 install git+https://github.com/KoichiYasuoka/syncha-cygwin
pip3.7 install spacy_syncha --no-build-isolation
```

