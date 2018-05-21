# -*- coding: utf-8 -*-
import copy
Gram = [] #gram的集合
symbol = []#符号表
Var = []#语法非终结符
states = [] # 状态的集合
Action = {}
Goto = {}

def read_grammer():
  fp = open('gram.txt','r+')
  for line in fp:
    line = line.rstrip('\n \t');
    #print line
    Gram.append(line)
    pro = line.split('->')[0]
    if pro not in symbol:
      symbol.append(pro)
      Var.append(pro)

    body = line.split('->')[1]
    body = body.split(' ')
    for it in body:
      if it not in symbol and it.isdigit():#数字表示关键字
        symbol.append(it)
  fp.close();

def first_sig(x):
  first = []
  if x.isdigit():
    first.append(x)
  elif x == '45':
    first.append(x)
  else:
    for it in Gram:
      #print it
      if x == it.split('->')[0]:
        #print '------------------------------'
        #print 'x: '+x
        y = it.split('->')[1].split(' ')[0]
        #print 'y: '+y
        tmp = first_sig(y)
        #print tmp
        if len(tmp) > 0:
          for t in tmp:
            if t not in first:
              first.append(t)
  return first
def first_set(x):
  return first_sig(x[0])

def close(I):
  '''
  构造文法集 I 的闭包,I是一个list
  '''
  C = I;
  for c in C:
    strlist = c.split('->')[1].split(' ')
    ch = strlist[strlist.index('.')+1]
    #print 'ch: '+ch
    if ch != ',':
      if ch.isdigit():
        continue;
      first_arr = strlist[strlist.index('.')+2:len(strlist)]
      #print 'first1 : '+str(first_arr)
      first_arr.remove(',')
      first = first_set(first_arr)
      #print 'first: '+str(first)
      for item in Gram:
        #print 'pro: '+item.split('->')[0]
        if ch == item.split('->')[0]:
          #print 'aaa'
          for n in first:
            newi = ch + '->. '+item.split('->')[1]+' , '+n
            if newi not in C:
              C.append(newi);
  return C;

def changeIndex(Item):
  strlist = Item.split('->')[1].split(' ')
  i = strlist.index('.')
  strlist[i] = strlist[i+1]
  strlist[i+1] = '.'
  newi = Item.split('->')[0] + '->' + ' '.join(strlist)
  return newi


def Go(I,X):
  J = [];
  for it in I:
    strlist = it.split('->')[1].split(' ')
    ch = strlist[strlist.index('.')+1]
    if ch==X:
      J.append(changeIndex(it))
  return close(J)


def CreatLR():
  it = Gram[0]
  one = it.split('->')[0] + '->. '+it.split('->')[1]+' , '+'45'
  t = []
  t.append(one)
  states.append(close(t))
  for si in states:
    for x in symbol:
      I = Go(si,x)
      if len(I) > 0 and I not in states:
        states.append(I)
        #print I

def CreatTable():
  for item in states:
    if '$-><S> . , 45' in item:#45 is the end of input
      Action[(states.index(item),'45')] = ('E',0)
      continue;
    for it in item:
      strlist = it.split('->')[1].split(' ')
      ch = strlist[strlist.index('.')+1]
      if ch.isdigit():
        s = Go(item,ch)
        pos = states.index(s)
        Action[(states.index(item),ch)] = ('S',pos)
      if ch == ',':
        newstr = copy.deepcopy(strlist)
        newstr.pop(len(newstr)-1)
        newstr.remove('.')
        newstr.remove(',')
        pro = it.split('->')[0]+'->'+' '.join(newstr)
        pos = Gram.index(pro)
        Action[(states.index(item),strlist[len(strlist)-1])] = ('R',pos)
    for k in Var:
      s = Go(item,k)
      if len(s) > 0:
        pos = states.index(s)
        Goto[(states.index(item),k)] = pos


if __name__ == '__main__':
    read_grammer()
    CreatLR()
    CreatTable()
    afp = open('Action.txt','w')
    gfp = open('Goto.txt','w')
    for ac in Action.keys():
      afp.write(' '.join([str(ac[0]),ac[1]])+' '+' '.join([Action[ac][0],str(Action[ac][1])])+'\n')
    for gt in Goto.keys():
      gfp.write(' '.join([str(gt[0]),str(Var.index(gt[1]))])+' '+str(Goto[gt])+'\n')
    afp.close();
    gfp.close()
    fp = open('gram.txt','r+')
    nfp = open('newg.txt','w')
    for line in fp:
      line = line.rstrip('\n \t');
      pro = line.split('->')[0]
      body = line.split('->')[1]
      body = body.split(' ')
      nfp.write(str(Var.index(pro))+' '+str(len(body))+'\n')
    nfp.close()
    print len(states)

