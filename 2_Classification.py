import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii

'''
Kang, ‎2017. https://ui.adsabs.harvard.edu/abs/2017ApJ...845...21K
Galactic and extragalactic contaminant removing
and YSO classification
'''

Name = 'IC348.dat' ##set file name here

##read data from local file
Data = ascii.read(Name)
print(Data.info())

##prepare empty figure and add two axes
fig = plt.figure(figsize=(13, 6), dpi=100)
ax1 = fig.add_axes([0.05, 0.11, 0.38, 0.80])
ax2 = fig.add_axes([0.435, 0.11, 0.01, 0.80])

ax3 = fig.add_axes([0.55, 0.11, 0.38, 0.80])
ax4 = fig.add_axes([0.935, 0.11, 0.01, 0.80])

##set labels and ticks
ax1.set_title('Removing galactic and extragalactic contaminant', fontsize=17)
ax1.set_xlabel('[4.6]-[12]')
ax1.set_ylabel('[3.4]-[4.6]')
ax1.minorticks_on()
ax3.set_title('YSO classification', fontsize=17)
ax3.set_xlabel('[4.6]-[12]')
ax3.set_ylabel('[3.4]-[4.6]')
ax3.minorticks_on()

##draw raw data in first axes
raw = ax1.scatter(Data['W2mag'] - Data['W3mag'], \
            Data['W1mag'] - Data['W2mag'], s = 10, c = Data['W1mag'], \
            cmap = 'jet_r')

Y = ax1.get_ylim()
X = ax1.get_xlim()
ax1.set_xlim(X)
ax1.set_ylim(Y)
##draw magnitude colorbar
fig.colorbar(raw, cax = ax2, label='[3.4](mag)')
ax2.invert_yaxis()

'''
Step 1
Identify and remove likely star-forming galaxies
'''
Index_1 = np.where((Data['W2mag'] - Data['W3mag'] > 1.0) &\
                 (Data['W1mag'] - Data['W2mag'] < 1.0) &\
                 (Data['W1mag'] - Data['W2mag'] < 0.46 *\
                 (Data['W2mag'] - Data['W3mag']) - 0.466) &\
                 ((Data['W1mag'] > 12.0) | (Data['W2mag'] > 11.0)))

ax1.plot([1.0, 1.0], [Y[0], -0.006], 'r--')
ax1.plot([3.19, X[1]], [1.0, 1.0], 'r--')
ax1.plot([1.0, 3.19], [-0.006, 1.0], 'r--', label = 'star-forming galaxies')

'''
Step 2
Identify and remove likely broad-lined AGNs
'''
Index_2 = np.where((Data['W1mag'] > 1.8 *\
                   (Data['W1mag'] - Data['W3mag']) + 4.1) &\
                   ((Data['W1mag'] > 13.0) | (Data['W2mag'] > 12.0) |\
                   (Data['W1mag'] > Data['W1mag'] - Data['W3mag'] + 11.0)))

'''
Step 3
Identify and remove unresolved shock emission knots
'''
Index_3 = np.where((Data['W1mag'] - Data['W2mag'] > 1.0) &\
                   (Data['W2mag'] - Data['W3mag'] < 2.0))

##draw unresolved shock emission knots area
ax1.plot([X[0], 2.0], [1.0, 1.0], 'g--', label = 'shock emission knots')
ax1.plot([2.0, 2.0], [1.0, Y[1]], 'g--')

'''
Step 4
Identify and remove resolved structured PAH emission
'''
Index_4 = np.where((Data['W1mag'] - Data['W2mag'] < 1.0) &\
                   (Data['W2mag'] - Data['W3mag'] > 4.9) |\
                   (Data['W1mag'] - Data['W2mag'] < 0.25) &
                   (Data['W2mag'] - Data['W3mag'] > 4.75))

##draw resolved structured PAH emissions area
ax1.plot([X[1], 4.9], [1.0, 1.0], 'b--', label = 'PAH emission')
ax1.plot([4.9, 4.9], [1.0, 0.25], 'b--')
ax1.plot([4.9, 4.75], [0.25, 0.25], 'b--')
ax1.plot([4.75, 4.75], [0.25, Y[0]], 'b--')


Index = np.hstack((Index_1, Index_2, Index_3, Index_4))

##mask bad sources on axes 1
ax1.scatter(Data['W2mag'][Index] - Data['W3mag'][Index], \
            Data['W1mag'][Index] - Data['W2mag'][Index], s = 20,
            marker = 'x', facecolor = 'red', lw=0.5, label = 'Masked')

ax1.legend()
#plt.show()

'''
YSO classification
'''
##delete contamination
Data.remove_rows(Index)
Data['Class'] = 'none'

##draw cleared data in second axes
Cleared = ax3.scatter(Data['W2mag'] - Data['W3mag'], \
            Data['W1mag'] - Data['W2mag'], s = 10, c = Data['W1mag'], \
            cmap = 'jet_r')
Y = ax3.get_ylim()
X = ax3.get_xlim()
ax3.set_xlim(X)
ax3.set_ylim(Y)

##draw magnitude colorbar
fig.colorbar(Cleared, cax = ax4, label='[3.4](mag)')
ax4.invert_yaxis()

'''
Class I objects
'''
Class_I = np.where((Data['W2mag'] - Data['W3mag'] > 2.0) &\
                   (Data['W1mag'] - Data['W2mag'] > (-0.42 *\
                   (Data['W2mag'] - Data['W3mag']) + 2.2)) &\
                   (Data['W1mag'] - Data['W2mag'] > (0.46 *\
                   (Data['W2mag'] - Data['W3mag']) - 0.9)) &\
                   (Data['W2mag'] - Data['W3mag'] < 4.5))[0]

ax3.scatter(Data['W2mag'][Class_I] - Data['W3mag'][Class_I], \
            Data['W1mag'][Class_I] - Data['W2mag'][Class_I], s = 40,
            facecolor = 'None', edgecolor = 'red', lw = 1.5, label = 'Class I')
Data['Class'][Class_I] = 'I'
##print(Class_I[0])
'''
Class II objects
'''
Class_II = np.where((Data['W1mag'] - Data['W2mag'] > 0.25) &\
                    (Data['W1mag'] - Data['W2mag'] < (0.9 *\
                    (Data['W2mag'] - Data['W3mag']) - 0.25)) &\
                    (Data['W1mag'] - Data['W2mag'] > (-1.5 *\
                    (Data['W2mag'] - Data['W3mag']) + 2.1)) &\
                    (Data['W1mag'] - Data['W2mag'] > (0.46 *\
                    (Data['W2mag'] - Data['W3mag']) - 0.9)) &
                    (Data['W2mag'] - Data['W3mag'] < 4.5))[0]
Class_II = np.setdiff1d(Class_II, Class_I)
##print(Class_II)
Used = np.hstack((Class_I, Class_II))
##print(Used)
ax3.scatter(Data['W2mag'][Class_II] - Data['W3mag'][Class_II], \
            Data['W1mag'][Class_II] - Data['W2mag'][Class_II], s = 40,
            facecolor = 'None', edgecolor = 'green', lw = 1.5, label = 'Class II')
Data['Class'][Class_II] = 'II'

'''
Transition disk objects
'''
Class_TD = np.where((Data['W3mag'] - Data['W4mag'] > 1.5) &\
                    (Data['W1mag'] - Data['W2mag'] > 0.15) &\
                    (Data['W1mag'] - Data['W2mag'] < 0.8) &\
                    (Data['W1mag'] - Data['W2mag'] > (0.46 *\
                    (Data['W2mag'] - Data['W3mag']) - 0.9)) &\
                    (Data['W1mag'] <= 13.0))[0]
Class_TD = np.setdiff1d(Class_TD, Used)
Used = np.hstack((Used, Class_TD))
ax3.scatter(Data['W2mag'][Class_TD] - Data['W3mag'][Class_TD], \
            Data['W1mag'][Class_TD] - Data['W2mag'][Class_TD], s = 40,
            facecolor = 'None', edgecolor = 'blue', lw = 1.5, \
            label = 'Transition disk')
Data['Class'][Class_TD] = 'TD'

'''
Remaining YSO candidates are classified as Class III
with field stars contaminant
'''
Class_III = np.setdiff1d(np.arange(0, len(Data)), Used)
ax3.scatter(Data['W2mag'][Class_III] - Data['W3mag'][Class_III], \
            Data['W1mag'][Class_III] - Data['W2mag'][Class_III], s = 40,
            facecolor = 'None', edgecolor = 'magenta', lw = 1.5, \
            label = 'Class III')
Data['Class'][Class_III] = 'III'

print(Data)
##save table to local file
Data.write(Name.replace('.dat', '_class.dat'), format = 'ascii', \
                        delimiter='\t', overwrite=True)
ax3.legend()
plt.show()






