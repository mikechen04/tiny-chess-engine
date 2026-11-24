import sys,time
T=time.time;R=range;W=50000
def J(b):return b[::-1].swapcase()
D={'P':(-10,-20,-11,-9),'N':(-21,-19,21,19,-12,8,-8,12),'B':(-11,-9,9,11),'R':(-10,1,10,-1)}
D['Q']=D['K']=D['B']+D['R']
def F(p,i):
 r,c=divmod(i,10);k=9-r;f=abs(2*c-9);n=14-f-abs(2*r-11);f=(7-f)//2
 return[100+2*k*k+3*f*k,285+5*n,320+3*n,500+20*(k==6)+5*(2<c<7),940+2*n,30000-15*k+15*(c in(2,3,7,8)),30000+4*n][p]
Z={p:[F(j,i)for i in R(120)]for j,p in enumerate('PNBRQKE')};Z['M']=Z['K']
def A(b,s):
 if'p'in b[s-11]+b[s-9]:return 1
 for d in D['N']:
  if b[s+d]=='n':return 1
 for d in D['K']:
  j=s+d
  if b[j]=='k':return 1
  while b[j]=='.':j+=d
  if b[j]in'q'+'br'[d in D['R']]:return 1
def G(P,z=0):
 b,s,c,e=P
 for i,p in enumerate(b):
  if'@'<p<'[':
   for d in D[p]:
    j=i+d
    while 1:
     q=b[j]
     if q<'.'or'@'<q<'['or p=='P'and(d%10==0 and q!='.'or d==-20 and(i<81 or b[i-10]!='.')or d%10 and q=='.'and j!=e):break
     for x in('QNRB'if p=='P'and j<30 else p):
      if q!='.'or x!=p or z<1:yield i,j,x
     if p in'PNK'or q!='.':break
     j+=d
 k=b.find('K')
 for n,r in(0,91),(1,98):
  d=(r>k)*2-1
  if c[n]>z and all(b[x]=='.'for x in R(k+d,r,d))and not any(A(b,k+t*d)for t in(0,1,2)):yield k,k+2*d,'K'
def V(P,m):
 b=P[0];i,j,x=m;p=b[i];q=b[j];v=Z[x][j]-Z[p][i]
 if q!='.':v+=Z[q.upper()][119-j]
 if p=='K'and abs(j-i)==2:v+=Z['R'][i+j>>1]-Z['R'][91+7*(j>i)]
 if p=='P'and j==P[3]:v+=Z['P'][109-j]
 return v
def M(P,m):
 b,s,c,e=P;i,j,x=m;p=b[i];s+=V(P,m);b=list(b);b[j]=x;b[i]='.'
 if p=='K'and abs(j-i)==2:b[91+7*(j>i)]='.';b[i+j>>1]='R'
 if p=='P'and j==e:b[j+10]='.'
 return J(''.join(b)),-s,(c[2]*(j!=28),c[3]*(j!=21),c[0]*(i!=91)*(p!='K'),c[1]*(i!=98)*(p!='K')),(p=='P'and i-j==20)*(129-i)
def L(P,m):b=J(M(P,m)[0]);return not A(b,b.find('K'))
H=set();Y={};K={}
def S(P,d,a,B,y):
 if T()>E:1/0
 b,s,c=P[:3]
 if s<-2e4:return-W
 if y and b in H:return 0
 h=A(b,b.find('K'))or 0;d+=h and d>0;q=d<1;f=-W
 if q:
  if s>=B:return s
  f=s;a=max(a,s)
 e=Y.get(P)
 if e and y and e[0]>=d and(e[2]==0 or e[2]>0 and e[1]>=B or e[2]<0 and e[1]<=a):return e[1]
 if d>2 and y and not h:
  v=-S((J(b),-s,c[2:]+c[:2],0),d-3,-B,1-B,y+1)
  if v>=B:return v
 t=e and e[3];g=K.get(y);o=a;u=0;H.add(b)
 for n,m in enumerate(sorted((m for m in G(P,q)if y or L(P,m)),key=lambda m:(m==t)*1e5+(m==g)*50+V(P,m),reverse=1)):
  X=M(P,m);r=d>2 and n>3 and not h and b[m[1]]=='.'and m[2]==b[m[0]]
  if r:v=-S(X,d-2,-a-1,-a,y+1)
  if not r or v>a:v=-S(X,d-1,-B,-a,y+1)
  if v>f:f=v;u=m
  a=max(a,v)
  if a>=B:
   if b[m[1]]=='.':K[y]=m
   break
 H.discard(b)
 if f==-W and not q:f=(y-30000)*h
 Y[P]=d,f,(f>=B)-(f<=o),u
 return f
def U(s):i=ord(s[0])+4-10*int(s[1]);return i if w else 119-i
def C(b):return sum(Z[p][i]for i,p in enumerate(b)if p.isupper())
def O(s):print(s,flush=1)
def N(i):i=i if w else 119-i;return chr(i%10+96)+str(10-i//10)
for l in sys.stdin:
 l=l.split()+['moves'];c=l[0]
 if c=='uci':O('id name Tiny\nuciok')
 if c=='isready':O('readyok')
 if c=='quit':break
 if c=='position':
  k=l.index('moves');f=l[2:k]if l[1]=='fen'else'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'.split();b=f[0]
  for x in R(1,9):b=b.replace(str(x),'.'*x)
  b=' '*20+''.join(' '+r+' 'for r in b.split('/'))+' '*20;w=f[1]=='w';c=tuple(x in f[2]for x in'QKkq')
  e=f[3]>'-'and U(f[3]);P=(b,0,c,e)if w else(J(b),0,c[2:]+c[:2],e)
  H=set()
  for u in l[k+1:-1]:H.add(P[0]);i=U(u);P=M(P,(i,U(u[2:]),u[4:].upper()or P[0][i]));w^=1
  b=P[0];Z['K']=Z['ME'[sum(map(b.count,'QRBNqrbn'))<7]];P=(b,C(b)-C(J(b)))+P[2:]
 if c=='go':
  o=dict(zip(l[1::2],l[2::2]));z=T();t=int(o.get('bw'[w]+'time',0))/1e3;n=int(o.get('bw'[w]+'inc',0))/1e3
  h=int(o.get('movetime',0))/1e3*.85 or t and min(t/15+n*.8,t/3)or('depth'in o)*1e9+5;E=z+h
  u=next((m for m in G(P)if L(P,m)),0)
  if len(Y)>3e5:Y={}
  for d in R(1,int(o.get('depth',99))+1):
   try:S(P,d,-W,W,0)
   except:break
   u=Y[P][3]or u
   if T()-z>h/2:break
  O('bestmove '+(u and N(u[0])+N(u[1])+(u[2]!=P[0][u[0]])*u[2].lower()or'0000'))
