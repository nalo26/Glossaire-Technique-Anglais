english = []
french = []
important = []
with open('page1.csv', encoding="utf-8") as f:
	f = f.read()
	a = f.split('\n')
	for line in a:
		line = line.split(';')
		if line[2] == 'True': print(line)