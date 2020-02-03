a=['1','2','3']
b=['2','1','3']

if (a!= b):
    print(list(set(a)-set(b)))
    print("a!=b")

tmp=".k/p/t"
len1 = len(tmp.split("/"))


tmp=".k/p/t/q"
len1 = len(tmp.split("/"))

a= tmp.split("/")


myset = set()

myset.update("1")

myset.update("1")
myset.update("2")
myset.update("3")

for item in myset:
    print(item)


chile_ranks = {'ghost':1, 'haberno':2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}


b= chile_ranks.items()
a={}
for r,i in chile_ranks.items():
    a[i]=r
pass

def fun():
    a['9']='s'

fun()
pass
