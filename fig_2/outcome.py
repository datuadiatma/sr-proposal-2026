import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams.update({"font.size":5.5,"axes.linewidth":0.6,"xtick.major.width":0.6,
                     "ytick.major.width":0.6,"xtick.major.size":2,"ytick.major.size":2})

# Epochs (GTS2020); colors from the ICS chart
STAGES=[("Middle Ordovician",471.3,458.2),("Late Ordovician",458.2,443.1)]
STAGE_COL=["#4DB47E","#7FCA93"]
SECTIONS=[("Kårgärde",470.5,457.56),
          ("Monitor + Antelope Range",467.0,443.5),
          ("Germany Valley",459.1,452.0)]
REEF=(462.0,443.5,"Reef-builder expansion")
T_DROP,T_REBOUND=460.5,457.0

t=np.linspace(471.3,443.1,400)
drop=1/(1+np.exp((t-T_DROP)/0.8))
reb=1/(1+np.exp((t-T_REBOUND)/1.2))
h1=1-0.75*drop
h2=h1+0.6*reb

fig=plt.figure(figsize=(3.0,1.65))
ax=fig.add_axes([0.13,0.58,0.84,0.30]); ax2=fig.add_axes([0.13,0.19,0.84,0.37],sharex=ax)
ax.plot(t,h1,color="#1b6ca8",lw=1.3); ax.plot(t,h2,color="#c2452d",lw=1.3,ls=(0,(3,1.5)))
ax.text(443.4,h1[-1]+0.07,"H1",color="#1b6ca8",ha="right",va="bottom",fontweight="bold")
ax.text(443.4,h2[-1]+0.07,"H2",color="#c2452d",ha="right",va="bottom",fontweight="bold")
ax.set_ylim(0.1,1.12); ax.set_yticks([0.25,1.0]); ax.set_yticklabels(["low","high"])
ax.set_ylabel("δ$^{88/86}$Sr",labelpad=1)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="x",length=0,labelbottom=False)
for (n,o,y),c in zip(STAGES,STAGE_COL):
    ax.add_patch(Rectangle((y,1.14),o-y,0.2,color=c,lw=0,clip_on=False))
    ax.text((o+y)/2,1.24,n,ha="center",va="center",fontsize=5)
    ax.plot([y,y],[1.14,1.34],color="white",lw=0.6,clip_on=False)

y=0
for name,a,b in SECTIONS[::-1]:
    ax2.add_patch(Rectangle((b,y+0.2),a-b,0.55,color="#666",lw=0))
    inside=(a-b)>9
    ax2.text((a+b)/2 if inside else a+0.3,y+0.47,name,va="center",
             ha="center" if inside else "right",color="white" if inside else "#333",fontsize=4.8)
    y+=1
a,b,lab=REEF
ax2.annotate("",xy=(b,y+0.47),xytext=(a,y+0.47),arrowprops=dict(arrowstyle="->",color="#8a6d1d",lw=0.9,shrinkA=0,shrinkB=0))
ax2.text(a+0.3,y+0.47,lab,va="center",ha="right",color="#8a6d1d",fontsize=4.8)
y+=1

# Deep-ocean oxygenation: same timing that drives H2 (rise with the drop, fade at the rebound)
oxy=drop*(1-reb)
cmap=LinearSegmentedColormap.from_list("oxy",["#ffffff","#2a7f8f"])
ax2.imshow(oxy[None,:],extent=(t[0],t[-1],y+0.2,y+0.75),aspect="auto",cmap=cmap,vmin=0,vmax=1,interpolation="bilinear")
ax2.text(463.0,y+0.47,"Deep-ocean oxygenation",va="center",ha="right",color="#2a7f8f",fontsize=4.8)
ax2.set_ylim(0,y+1); ax2.set_yticks([])
for s in ["top","right","left"]: ax2.spines[s].set_visible(False)
ax2.set_xlim(471.3,443.1); ax2.set_xticks([470,465,460,455,450,445])
ax2.set_xlabel("Age (million years ago)",labelpad=1)
fig.savefig("fig2_outcome.png",dpi=600)
