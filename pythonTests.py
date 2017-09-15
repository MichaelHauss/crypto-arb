from sortedcontainers import SortedDict

d = SortedDict()

d[4]="a"
d[0]="b"
d[3]="c"
d[2]="d"
d[1]="e"

for item in d:
	print(item)