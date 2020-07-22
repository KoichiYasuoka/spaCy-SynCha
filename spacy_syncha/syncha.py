#! /usr/bin/python3 -i
# coding=utf-8

import os
PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))
SYNCHA2UD=os.path.join(PACKAGE_DIR,"syncha2ud")

import numpy
from spacy.language import Language
from spacy.symbols import LANG,NORM,LEMMA,POS,TAG,DEP,HEAD,ENT_IOB,ENT_TYPE
from spacy.tokens import Doc,Span,Token
from spacy.util import get_lang_class

class SynChaLanguage(Language):
  lang="ja"
  max_length=10**6
  def __init__(self):
    self.Defaults.lex_attr_getters[LANG]=lambda _text:"ja"
    self.vocab=self.Defaults.create_vocab()
    self.tokenizer=SynChaTokenizer(self.vocab)
    self.pipeline=[]
    self._meta={
      "author":"Koichi Yasuoka",
      "description":"derived from SynCha-CaboCha-MeCab",
      "lang":"ja_SynCha_CaboCha_MeCab",
      "license":"MIT",
      "name":"SynCha_CaboCha_MeCab",
      "pipeline":"Tokenizer, POS-Tagger, Parser",
      "spacy_version":">=2.2.2"
    }
    self._path=None

class SynChaTokenizer(object):
  to_disk=lambda self,*args,**kwargs:None
  from_disk=lambda self,*args,**kwargs:None
  to_bytes=lambda self,*args,**kwargs:None
  from_bytes=lambda self,*args,**kwargs:None
  def __init__(self,vocab):
    import subprocess
    self.model=lambda s:subprocess.check_output([SYNCHA2UD],input=s.encode("utf-8")).decode("utf-8")
    self.vocab=vocab
  def __call__(self,text):
    t=text.replace("\r","").replace("(","（").replace(")","）").replace("[","［").replace("]","］").replace("{","｛").replace("}","｝")
    u=self.model(t) if t else ""
    vs=self.vocab.strings
    r=vs.add("ROOT")
    words=[]
    lemmas=[]
    pos=[]
    tags=[]
    heads=[]
    deps=[]
    spaces=[]
    norms=[]
    ent_iobs=[]
    ent_types=[]
    for t in u.split("\n"):
      if t=="" or t.startswith("#"):
        continue
      s=t.split("\t")
      if len(s)!=10:
        continue
      id,form,lemma,upos,xpos,dummy_feats,head,deprel,dummy_deps,misc=s
      words.append(form)
      lemmas.append(vs.add(lemma))
      pos.append(vs.add(upos))
      tags.append(vs.add(xpos))
      if deprel=="root":
        heads.append(0)
        deps.append(r)
      else:
        heads.append(int(head)-int(id))
        deps.append(vs.add(deprel))
      spaces.append(False if "SpaceAfter=No" in misc else True)
      i=misc.find("Translit=")
      norms.append(vs.add(form if i<0 else misc[i+9:]))
      if misc.startswith("NE="):
        i=misc.find("|")
        if i<0:
          i=len(misc)
        if misc[3:4]=="B":
          ent_iobs.append(3)
        else:
          ent_iobs.append(1)
        ent_types.append(vs.add(misc[5:i]))
      else:
        ent_iobs.append(2)
        ent_types.append(0)
    doc=Doc(self.vocab,words=words,spaces=spaces)
    a=numpy.array(list(zip(lemmas,pos,tags,deps,heads,norms,ent_iobs,ent_types)),dtype="uint64")
    doc.from_array([LEMMA,POS,TAG,DEP,HEAD,NORM,ENT_IOB,ENT_TYPE],a)
    doc.is_tagged=True
    doc.is_parsed=True
    return doc

def load():
  return SynChaLanguage()

