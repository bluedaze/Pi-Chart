import csv
from matplotlib import pyplot as plt

headers =[]
SY = []
SN = []
BY = []
BN = []
name = "AndrewYang"
with open("bracketinfo.txt", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for line in csvreader:
        if line[0] == name:
            if line[1] =="b2": #or line[1] =="b2":
                if line[2]=="SY":
                    SY.append(line[3])
                elif line[2]=="SN":
                    SN.append(line[3])
                elif line[2]=="BY":
                    BY.append(line[3])
                elif line[2]=="BN":
                    BN.append(line[3])

plt.plot(SN, label="Sell No")
plt.plot(SY, label="Sell Yes")
plt.plot(BN, label="Buy No")
plt.plot(BY, label="Buy Yes")
plt.ylim(  (0, 1)  )
plt.legend(loc='lower left')
plt.title("Predict It Betting Data for" + name + " B1 ", fontsize=16, fontweight='bold')
plt.show()
