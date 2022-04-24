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
>>> import deplacy
>>> deplacy.render(doc,Japanese=True)
太郎 PROPN ═╗<══════════╗ nsubj(主語)
は   ADP   <╝           ║ case(格表示)
花子 PROPN ═╗<╗         ║ nsubj(主語)
が   ADP   <╝ ║         ║ case(格表示)
読ん VERB  ═══╝═╗═╗<╗   ║ acl(連体修飾節)
で   CCONJ <════╝ ║ ║   ║ mark(標識)
いる AUX   <══════╝ ║   ║ aux(動詞補助成分)
本   NOUN  ═╗═══════╝<╗ ║ obj(目的語)
を   ADP   <╝         ║ ║ case(格表示)
次   NOUN  <╗         ║ ║ compound(複合)
郎   NOUN  ═╝═╗<╗     ║ ║ iobj(間接目的語)
に   ADP   <══╝ ║     ║ ║ case(格表示)
渡し VERB  ═╗═══╝═════╝═╝ ROOT(親)
た   AUX   <╝             aux(動詞補助成分)
>>> from deplacy.deprelja import deprelja
>>> for b in spacy_syncha.bunsetu_spans(doc):
...   for t in b.lefts:
...     print(spacy_syncha.bunsetu_span(t),"->",b,"("+deprelja[t.dep_]+")")
...
花子が -> 読んでいる (主語)
読んでいる -> 本を (連体修飾節)
太郎は -> 渡した (主語)
本を -> 渡した (目的語)
次郎に -> 渡した (間接目的語)
```

`spacy_syncha.load(UniDic)` loads spaCy Language pipeline for SynCha-CaboCha-MeCab. Available `UniDic` options are:

* `UniDic="gendai"`: Use [現代書き言葉UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_bccwj).
* `UniDic="spoken"`: Use [現代話し言葉UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_csj).
* `UniDic="qkana"`: Use [旧仮名口語UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_qkana).
* `UniDic="kindai"`: Use [近代文語UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_kindai).
* `UniDic="kinsei"`: Use [近世江戸口語UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_kinsei-edo).
* `UniDic="kyogen"`: Use [中世口語UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_chusei-kougo).
* `UniDic="wakan"`: Use [中世文語UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_chusei-bungo).
* `UniDic="wabun"`: Use [中古和文UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_wabun).
* `UniDic="manyo"`: Use [上代語UniDic](https://clrd.ninjal.ac.jp/unidic/download_all.html#unidic_jodai).
* `UniDic=None`: Use IPADic (default).

You can simply use `syncha2ud` on the command line to get [Universal Dependencies](https://universaldependencies.org/format.html):

```sh
echo 太郎は花子が読んでいる本を次郎に渡した | syncha2ud
```

## Installation for Linux (Debian)

First, install [MeCab](https://taku910.github.io/mecab/) and necessary packages:

```sh
sudo apt update
sudo apt install mecab libmecab-dev mecab-ipadic-utf8 python3-pip python3-dev g++ make curl lp-solve
cd /tmp
curl -L 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ' | tar xzf -
cd CRF++-0.58
./configure --prefix=/usr --libdir=`mecab-config --libs-only-L`
make && sudo make install
```

Second, install [CaboCha](https://taku910.github.io/cabocha/):

```sh
cd /tmp
curl -sc cabocha.cookie 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU' > /dev/null
curl -Lb cabocha.cookie 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU&confirm='`tr -d '\015' < cabocha.cookie | awk '/_warning_/{print $NF}'` | tar xjf -
cd cabocha-0.69
./configure --prefix=/usr --libdir=`mecab-config --libs-only-L` --with-charset=UTF8
make && sudo make install
```

Third, install [SynCha](https://sites.google.com/site/ryuiida/syncha):

```sh
cd /tmp
curl -L 'https://drive.google.com/uc?export=download&id=0B4wOZ_esMVcMazQ0eGdtMnBCaWs' | tar xzf -
sudo mkdir -p /usr/local/bin
sudo mv syncha-0.3.1.1 /usr/local/syncha
( echo '#! /bin/sh' ; echo 'exec /usr/local/syncha/syncha "$@"' ) > syncha
sudo install syncha /usr/local/bin
```

And last, install spaCy-SynCha:

```sh
pip3 install spacy_syncha --user
```

## Installation for Linux (Ubuntu)

Same as Debian.

## Installation for Linux (Kali)

Same as Debian.

## Installation for Linux (CentOS)

First, install [MeCab](https://taku910.github.io/mecab/) and necessary packages:

```sh
sudo yum update
sudo yum install python3-pip python3-devel gcc-c++ make curl bzip2 lpsolve epel-release
sudo rpm -ivh https://packages.groonga.org/centos/latest/groonga-release-latest.noarch.rpm
sudo yum install mecab mecab-devel mecab-ipadic
cd /tmp
curl -L 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ' | tar xzf -
cd CRF++-0.58
./configure --prefix=/usr --libdir=`mecab-config --libs-only-L`
make && sudo make install
```

Second, third, and last are same as Debian.

## Installation for Cygwin

Make sure to get `python37-devel` `python37-pip` `python37-cython` `python37-numpy` `git` `gcc-g++` `perl`, and then:

```sh
pip3.7 install git+https://github.com/KoichiYasuoka/syncha-cygwin
pip3.7 install spacy_syncha
```

## Installation for Google Colaboratory

Try [notebook](https://colab.research.google.com/github/KoichiYasuoka/spaCy-SynCha/blob/master/spacy_syncha.ipynb).

## Benchmarks

Results of [舞姬/雪國/荒野より-Benchmarks](https://colab.research.google.com/github/KoichiYasuoka/spaCy-SynCha/blob/master/benchmark.ipynb)

|[舞姬](https://github.com/KoichiYasuoka/UniDic2UD/blob/master/benchmark/maihime-benchmark.tar.gz)|LAS|MLAS|BLEX|
|---------------|-----|-----|-----|
|UniDic="kindai"|84.91|70.37|74.07|
|UniDic="qkana" |81.13|66.67|70.37|
|UniDic="kinsei"|72.22|57.14|57.14|

|[雪國](https://github.com/KoichiYasuoka/UniDic2UD/blob/master/benchmark/yukiguni-benchmark.tar.gz)|LAS|MLAS|BLEX|
|---------------|-----|-----|-----|
|UniDic="qkana" |87.50|81.63|77.55|
|UniDic="kinsei"|85.71|83.33|75.00|
|UniDic="kindai"|83.19|77.55|73.47|

|[荒野より](https://github.com/KoichiYasuoka/UniDic2UD/blob/master/benchmark/koyayori-benchmark.tar.gz)|LAS|MLAS|BLEX|
|---------------|-----|-----|-----|
|UniDic="kindai"|67.02|32.43|43.24|
|UniDic="qkana" |63.87|32.88|43.84|
|UniDic="kinsei"|63.54|29.73|40.54|

## Reference

* 安岡孝一: [形態素解析部の付け替えによる近代日本語(旧字旧仮名)の係り受け解析](http://hdl.handle.net/2433/254677), 情報処理学会研究報告, Vol.2020-CH-124「人文科学とコンピュータ」, No.3 (2020年9月5日), pp.1-8.
