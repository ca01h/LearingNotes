import matplotlib.pyplot as plt
import csv

send = []
rece = []
ip = []

with open('send_rece.csv' ,'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=' ')
	for row in plots:
		if row[0] == '45.80.170.1': continue
		send.append(int(row[1]))
		rece.append(int(row[2]))
		ip.append(row[0])

fig, ax = plt.subplots()
ax.scatter(send, rece, label='')
for i, txt in enumerate(ip):
	if send[i] > 8e6 or rece[i] > 8e6:
		ax.annotate(txt, (send[i], rece[i]))

plt.xlabel('send')
plt.ylabel('receive')
plt.title('')
plt.legend()
plt.show()
