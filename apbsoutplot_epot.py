import sys
import numpy as np
import matplotlib.pyplot as plt

n=len(sys.argv)
electpotperres=[]
electpotperres_ave=[]
electpotperres_std=[]
apbsout_folder=[]
for i in range(1,n):
    apbsout_folder.append(str(sys.argv[i]))
    print(apbsout_folder[-1])

    pqr_file=apbsout_folder[-1]+"/mol_0.pqr"
    f=open(pqr_file,'r')
    pqr=f.readlines()
    f.close()

    atomid=[]
    atomname=[]
    resname=[]
    resnumber=[]
    for lines in pqr:
        l = lines.rstrip('\n').split()
        if l[0]=="ATOM" or l[0]=="HETATOM":
            atomid.append(int(l[1]))
            atomname.append(l[2])
            resname.append(l[3])
            resnumber.append(int(l[4]))
    natoms=len(atomid)
    nres=len(set(resnumber))

    print('Number of residues:',nres)
    print('Number of atoms:',natoms)

    electpotperres.append(np.zeros((5,max(resnumber)+1)))
    for j in range(5):

        apbsout_file=apbsout_folder[-1]+"/mol_"+str(j)+".pqr.txt"

        f=open(apbsout_file,'r')
        apbsout=f.readlines()
        f.close()

        apbs_electpot=[]
        for lines in apbsout[4:]:
            l = lines.rstrip('\n')
            apbs_electpot.append(float(l))

        print('Total electrostatic potential:',sum(apbs_electpot))

        for k in range(natoms):
            electpotperres[-1][j,resnumber[k]]=electpotperres[-1][j,resnumber[k]]+apbs_electpot[k]

    #plot energy per residue
    x=sorted(set(resnumber))
    electpotperres_ave.append(np.mean(electpotperres[-1],axis=0))
    electpotperres_std.append(np.std(electpotperres[-1],axis=0))
    print(len(electpotperres_ave[-1]))
    bar_width = 1./(n)
    plt.bar(x,electpotperres_ave[-1][x],label=apbsout_folder[-1],alpha=0.5)
    plt.errorbar(x, electpotperres_ave[-1][x], yerr=electpotperres_std[-1][x],fmt="o",elinewidth=bar_width/4, markersize=0.5,color='black')

plt.xlabel("Residue",fontsize=16)
plt.ylabel("Electrostatic potential",fontsize=16)
#plt.xticks(np.arange(60, max(x)+1, 10),fontsize=10)
plt.legend()
plt.savefig(apbsout_folder[-1]+'ElectrostaticPotential.png',dpi=300, bbox_inches='tight')
plt.close()
