import os
import math
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.pyplot import plot, ion, show
from PIL import Image
from tkinter import filedialog
from tkinter import *

def ibet(parms,root):
	ipfilename=parms[0]
	opfilename=parms[1]
	tmp=parms[2]
	xcenter=tmp[0].get()
	ycenter=tmp[1].get()
	zcenter=tmp[2].get()
	fi=tmp[3].get()
	gfi=tmp[4].get()
	flags=['',' -R',' -S',' -B',' -Z',' -A']
	flag=flags[list(tmp[5])[0]]
	mycmd='bet '+ipfilename+' '+opfilename+' -c '+xcenter+' '+ycenter+' '+zcenter+' -f '+fi+' -g '+gfi+flag
	root.config(cursor="watch")
	print('Start brain extraction')
	rc=os.system(mycmd)
	print('Finished brain extraction')
	root.config(cursor="")
	plotres(opfilename+'.gz')

def plotres(opfilename):
	nrslice=25
	pdim=int(math.sqrt(nrslice))
	img=nib.load(opfilename)
	dat=img.get_data()
	dims=dat.shape
	tmp=(np.around(np.ndarray.tolist(np.array(list(range(nrslice)))/nrslice*dims[2]),0)).astype(int)
	dat=dat[:,:,tmp]
	pdat=np.zeros([dims[0]*pdim,dims[1]*pdim])
	for x in range(0,nrslice):
 	   yp=math.floor(x/pdim)
 	   xp=x%pdim
 	   pdat[xp*dims[0]:(xp+1)*dims[0],yp*dims[1]:(yp+1)*dims[1]]=dat[:,:,x]
	ion()
	plt.figure(1,dpi=150)
	plt.axis('off')
	plt.imshow(pdat,cmap='gray')
	plt.show()

def onclick_event():
    nrfields=len(fields)
    ents[nrfields] = lb.curselection()
    return ents

def makeform(root,fields,fieldvals,flagnames):
    entries={}
    nrfields=len(fields)
    for i in range(0,nrfields):
        row=tk.Frame(root)
        lab=tk.Label(row,width=22,text=fields[i]+": ",anchor='w')
        ent=tk.Entry(row)
        fieldvals[i]
        ent.insert(0,fieldvals[i])
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, 
                 expand=tk.YES, 
                 fill=tk.X)
        entries[i]=ent
    return entries

root=tk.Tk()
root.filename=filedialog.askopenfilename(initialdir = "/",title = "Select nifti file",filetypes = (("nifti files","*.nii"),("all files","*.*")))
ipfilename=root.filename
opfilename=ipfilename.replace('.nii','_bet.nii')
img=nib.load(ipfilename)
dimsc=(np.array(img.header.get_data_shape())/2.).astype(int)
print('Start brain extraction with default settings')
rc=os.system('bet '+ipfilename+' '+opfilename+' -c '+str(dimsc[0])+' '+str(dimsc[1])+' '+str(dimsc[2])+' -f 0.2')
print('Finished brain extraction')
plotres(opfilename+'.gz')
fields =('x-center','y-center','z-center','Fractional Intensity','Gradient FI')
nrfields=len(fields)
flagnames=('None','Robust brain centre estimation','Eye & optic nerve cleanup','Bias field & neck cleanup','Improve BET with small FOV in Z','Get skull and scalp surfaces')
fieldvals=[str(dimsc[0]),str(dimsc[1]),str(dimsc[2]),'0.2','0.0']
root.title('Set BET parameters')
ents=makeform(root,fields,fieldvals,flagnames)
nrflags=len(flagnames)
row=tk.Frame(root)
lab=tk.Label(row,width=22,text='BET flags:',anchor='w')
row.pack(side=tk.TOP,fill=tk.X, padx=5, pady=5)
lab.pack(side=tk.LEFT)
lb=Listbox(root,width=32,height=nrflags)
for i in range(0,nrflags):
	lb.insert(i+1,flagnames[i])
lb.select_set(0)
ents[nrfields] = lb.curselection()
lb.pack()
lb.bind('<<ListboxSelect>>', lambda event: onclick_event())
b1 = tk.Button(root, text='Store',command=root.quit)
b1.pack(side=tk.LEFT,padx=5,pady=5)
b2 = tk.Button(root, text='Visualise',command=(lambda parms=[ipfilename,opfilename,ents]: ibet(parms,root)))
b2.pack(side=tk.LEFT,padx=5,pady=5)
root.mainloop()
root.destroy
print('Results written to '+opfilename)
os.system('gunzip '+opfilename+'.gz')


