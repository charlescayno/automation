import matplotlib.pyplot as plt
import matplotlib as mpl
# from pi_style import set_style



def set_style():
    colors = ['#002060', '#00B0F0', '#00B050', '#7030A0', '#3D96AE', '#DB843D', '#8EA5CB', '#CE8E8D', '#B6CB93', '#C00000']
    markers = ["D", "s", "^", "x", "X", "o", "+", "<", ">", "d"]
    mpl.rcParams['xtick.major.width'] = 4.0
    mpl.rcParams['xtick.major.size'] = 7.5
    mpl.rcParams['ytick.major.width'] = 4.0
    mpl.rcParams['ytick.major.size'] = 7.5
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors, marker=markers)
    mpl.rcParams['axes.linewidth'] = 4.0
    mpl.rcParams['axes.labelsize'] = 20.0
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titlesize'] = 26.0
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['lines.linewidth'] = 3.5
    mpl.rcParams['lines.markersize'] = 10.0
    mpl.rcParams['font.weight'] = 'normal'
    mpl.rcParams['font.size'] = 18.0
    mpl.rcParams['grid.color'] = '#A6A6A6'
    mpl.rcParams['grid.linewidth'] = 3.0


set_style()


for i in range(10):
    x = range(10)
    y = []
    for xx in x:
        y.append(0.1*(10-i)*pow(xx, 2))
    plt.plot(x, y, label='Plot'+str(i+1))

plt.xlabel('Load Current (%)')
plt.ylabel('Input Current (uA)')
plt.title('Plot Title')
plt.legend(loc=0)
plt.grid(True)
plt.show()
