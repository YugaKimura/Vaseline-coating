import matplotlib.pyplot as plt
import pandas as pd
A=pd.read_csv("ld.csv",header=None)
#print(A)
fig,ax=plt.subplots()
ax.boxplot((A.iloc[:865,0],A.iloc[:,1].dropna(),A.iloc[:,2].dropna()))
ax.set_xticklabels(["pre","propet","post"])
ax.set_ylabel("landing time")
#plt.plot(A[8],A[9]*-1,color="green",marker=None)
#plt.scatter(A[10],A[11]*-1,color="purple",marker="o")
#plt.savefig("1106pre_line.png")
plt.show()