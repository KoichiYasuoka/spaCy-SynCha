#! /usr/bin/python3 -i
# coding=utf-8

import os
PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))
SYNCHA2UD=os.path.join(PACKAGE_DIR,"syncha2ud")
UNIDIC2IPADIC=os.path.join(PACKAGE_DIR,"unidic2ipadic")

import numpy
from spacy.language import Language
from spacy.symbols import LANG,NORM,LEMMA,POS,TAG,DEP,HEAD,ENT_IOB,ENT_TYPE
from spacy.tokens import Doc,Span,Token
from spacy.util import get_lang_class

class SynChaLanguage(Language):
  lang="ja"
  max_length=10**6
  def __init__(self,UniDic):
    self.Defaults.lex_attr_getters[LANG]=lambda _text:"ja"
    self.vocab=self.Defaults.create_vocab()
    self.tokenizer=SynChaTokenizer(self.vocab,UniDic)
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
  def __init__(self,vocab,UniDic):
    import subprocess
    self.UniDic=UniDic
    if UniDic:
      d={ "gendai":"dic1", "spoken":"dic2", "qkana":"dic3", "kindai":"dic4", "kinsei":"dic5", "kyogen":"dic6", "wakan":"dic7", "wabun":"dic8", "manyo":"dic9" }
      self.dictkey=d[UniDic]
      self.model=self.ChamameWeb2SynChaUD
    else:
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
  def ChamameWebAPI(self,sentence):
    import random,urllib.request,json
    f={ self.dictkey:"UniDic-"+self.UniDic,
        "st":sentence+"\n\n",
        "f1":"1",
        "f2":"1",
        "f3":"1",
        "f4":"1",
        "f5":"1",
        "f9":"1",
        "f10":"1",
        "out-e":"csv",
        "c-code":"utf-8"
      }
    b="".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(10))
    d="\n".join("--"+b+"\nContent-Disposition:form-data;name="+k+"\n\n"+v for k,v in f.items())+"\n--"+b+"--\n"
    h={ "Content-Type":"multipart/form-data;charset=utf-8;boundary="+b }
    u=urllib.request.Request("https://unidic.ninjal.ac.jp/chamame/chamamebin/webchamame.php",d.encode(),h)
    with urllib.request.urlopen(u) as r:
      q=r.read()
    return q.decode("utf-8").replace("\r","")
  def ChamameWeb2SynChaUD(self,text):
    import subprocess
    s=self.ChamameWebAPI(text)
    m=""
    for t in s.split("\n"):
      w=t.split(",")
      if len(w)<9:
        continue
      if w[1]=="B":
        if m!="":
          m+="EOS\n"
      elif w[1]!="I":
        continue
      p=(w[5]+"-*-*-*-*").split("-")
      m+=w[2]+"\t"+",".join([p[0],p[1],p[2],p[3],"*" if w[6]=="" else w[6],"*" if w[7]=="" else w[7],w[4],w[3],w[2],w[8],w[9]])+"\n"
    m+="EOS\n"
    t=subprocess.check_output(["awk","-f",UNIDIC2IPADIC],input=m.encode("utf-8"))
    u=subprocess.check_output(["cabocha","-f","1","-n","1","-I","1"],input=t)
    return subprocess.check_output([SYNCHA2UD,"-I","1"],input=u).decode("utf-8")

def load(UniDic=None):
  return SynChaLanguage(UniDic)

