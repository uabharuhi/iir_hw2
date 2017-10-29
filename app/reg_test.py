import re

s = '1234-5567  wqw qesas 1234ww ab.cd -'
pat=re.compile(r'([0-9a-zA-Z\-]+)|([^0-9^a-z^A-Z^\-]+)')

for m in re.finditer(pat, s):
    s= m.group(1)
    print(s is None)
    print("g1:%s"%(m.group(1)))
    print("g2:%s"%(m.group(2)))
