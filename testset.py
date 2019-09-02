tmp=".k/p/t"
len1 = len(tmp.split("/"))


tmp=".k/p/t/q"
len1 = len(tmp.split("/"))


myset = set()

myset.update("1")

myset.update("1")
myset.update("2")
myset.update("3")

for item in myset:
    print(item)