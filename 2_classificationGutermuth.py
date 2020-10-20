import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from random import uniform

Name = 'IC348.dat' ## file name 

##reading from local file
Data = ascii.read(Name)
print(Data.info())

####J/ApJS/184/18 catalog is cleared from contamination
####so we add 100 random stars for testing. 
##for ii in range (0, 100):
##    Star = 18*np.random.rand(28)
##    Data.add_row(Star)
##print(Data.info())

'''
Step 1
PAH emission galaxies
'''
## prepare empty figures and add two axes for two criteria and colorbar
fig = plt.figure(figsize=(13, 6), dpi=100)
fig.suptitle('PAH emission galaxies', fontsize=15)

##[4.5]−[5.8] versus [5.8]−[8.0]
ax1 = fig.add_axes([0.06, 0.11, 0.38, 0.80])
ax1.set_xlabel('[5.8]-[8.0]')
ax1.set_ylabel('[4.5]-[5.8]')
ax1.minorticks_on()

##[3.6]−[5.8] versus [4.5]−[8.0]
ax2 = fig.add_axes([0.5, 0.11, 0.38, 0.80])
ax2.set_xlabel('[4.5]-[8.0]')
ax2.set_ylabel('[3.6]-[5.8]')
ax2.minorticks_on()

##colorbar
ax3 = fig.add_axes([0.925, 0.11, 0.02, 0.80])

##raw data in first axes
ax1.scatter(Data['_5.8mag'] - Data['_8.0mag'], \
            Data['_4.5mag'] - Data['_5.8mag'], \
            s = 10, c = Data['_4.5mag'], cmap = 'jet_r')
##get axis limits
X = [-1.0, 3.0] #ax1.get_xlim()
Y = [-1.0, 2.0] #ax1.get_ylim()
ax1.set_xlim(X)
ax1.set_ylim(Y)
##plot lines
ax1.plot([1.0, 1.0], [Y[0], 0.0], 'r--') #[5.8]−[8.0] > 1
ax1.plot([1.0, 2.2], [0.0, 1.05], 'r--') #[4.5]−[5.8] < 1.05/1.2×([5.8]−[8.0]−1)
ax1.plot([2.2, X[1]], [1.05, 1.05], 'r--') #[4.5]−[5.8] < 1.05

##raw data in second axes
raw = ax2.scatter(Data['_4.5mag'] - Data['_5.8mag'], \
                  Data['_3.6mag'] - Data['_5.8mag'], \
                  s = 10, c = Data['_4.5mag'], cmap = 'jet_r')
##get axis limits
X = [-2.0, 4.0] #ax2.get_xlim()
Y = [-2.0, 3.0] #ax2.get_ylim()
ax2.set_xlim(X)
ax2.set_ylim(Y)
##plot lines
ax2.plot([1.0, 1.0], [Y[0], 0.0], 'r--') #[4.5]−[5.8] > 1
ax2.plot([1.0, 3.0], [0.0, 1.5], 'r--') #[4.5]−[5.8] < 1.05/1.2×([5.8]−[8.0]−1)
ax2.plot([3.0, X[1]], [1.5, 1.5], 'r--') #[3.6]−[5.8] < 1.5

# magnitude colorbar
fig.colorbar(raw, cax = ax3, label='[4.5](mag)')
ax3.invert_yaxis()

##get contaminations indexes
Index_1 = np.where((Data['_4.5mag'] - Data['_5.8mag'] < 0.875 * \
                   (Data['_5.8mag'] - Data['_8.0mag'] - 1.0)) & \
                   (Data['_4.5mag'] - Data['_5.8mag'] < 1.05) & \
                   (Data['_5.8mag'] - Data['_8.0mag'] > 1.0) & \
                   (Data['_4.5mag'] > 11.5 ))

Index_2 = np.where((Data['_3.6mag'] - Data['_5.8mag'] < 0.75 * \
                   (Data['_4.5mag'] - Data['_8.0mag'] - 1.0)) & \
                   (Data['_3.6mag'] - Data['_5.8mag'] < 1.5) & \
                   (Data['_4.5mag'] - Data['_8.0mag'] > 1.0) & \
                   (Data['_4.5mag'] > 11.5 ))
##delete contamination
Index = np.hstack((Index_1, Index_2))
Data.remove_rows(Index)
plt.show()


'''
Step 2
Galaxies with AGNs
'''
## prepare empty figures and add two axes for two criteria
fig = plt.figure(figsize=(13, 6), dpi=100)

##Broad-line AGNs, [4.5] versus [4.5]−[8.0]
ax1 = fig.add_axes([0.05, 0.11, 0.38, 0.80])
ax1.set_title('Broad-line AGNs')
ax1.set_xlabel('[4.5]-[8.0]')
ax1.set_ylabel('[4.5]')
ax1.minorticks_on()

##raw data in first axes
ax1.scatter(Data['_4.5mag'] - Data['_8.0mag'], \
            Data['_4.5mag'], \
            s = 10, c = 'green', label = 'YSOs')
##get axis limits
Y = [18, 4.0] #ax1.get_ylim()
X = [-2.0, 6.0] #ax1.get_xlim()
ax1.set_xlim(X)
ax1.set_ylim(Y)

##plot lines
ax1.plot([0.5, 0.5], [Y[0], 13.5], 'r--') #[4.5]−[5.8] > 0.5
ax1.plot([2.3, 2.3+(Y[0]-13.5)*0.4], [13.5, Y[0]], 'r--') #[4.5]>13.5+([4.5]−[8.0]−2.3)/0.4
ax1.plot([0.5, 2.3], [13.5, 13.5], 'r--')

##to ﬂag as likely AGN all sources that follow all of these three conditions:
I_0 = np.where((Data['_4.5mag'] - Data['_8.0mag'] > 0.5) & \
                   (Data['_4.5mag'] > 13.5 + \
                   (Data['_4.5mag'] - Data['_8.0mag'] - 2.3) / 0.4) & \
                   (Data['_4.5mag'] >  13.5))[0]

##Additionally, a source ﬂagged as a likely AGN must follow any one of
#the following three conditions:
##use OR (|) instead AND (&)
I_1 = np.where((Data[I_0]['_4.5mag'] > 14 + \
               (Data[I_0]['_4.5mag'] - Data[I_0]['_8.0mag'] - 0.5)) | \
               (Data[I_0]['_4.5mag'] > 14.5 - \
               (Data[I_0]['_4.5mag'] - Data[I_0]['_8.0mag'] - 1.2) / 0.3) | \
               (Data[I_0]['_4.5mag'] > 14.5))[0]
##and select indexes for both conditions
Index_3 = np.array(I_0)[np.array(I_1)]

##mark contamination on figure
ax1.scatter(Data[Index_3]['_4.5mag'] - Data[Index_3]['_8.0mag'], \
            Data[Index_3]['_4.5mag'], \
            s = 10, c = 'red', label = 'Marked as broad-line AGNs')
ax1.legend()
##delete contamination
Data.remove_rows(Index_3)


'''
Step 3
Unresolved knots of shock emission
'''
##shock emission, [3.6]-[4.5] versus [4.5]−[8.0]
ax2 = fig.add_axes([0.55, 0.11, 0.38, 0.80])
ax2.set_title('Unresolved knots of shock emission')
ax2.set_xlabel('[4.5]-[5.8]')
ax2.set_ylabel('[3.6]-[4.5]')
ax2.minorticks_on()

##raw data in first axes
ax2.scatter(Data['_4.5mag'] - Data['_5.8mag'], \
            Data['_3.6mag'] - Data['_4.5mag'], \
            s = 10, c = 'red', label = 'Shock emission')
##get axis limits
Y = [-1, 3.5] #ax2.get_ylim() #
X = [-1.0, 3.0] #ax2.get_xlim() #
ax2.set_xlim(X)
ax2.set_ylim(Y)

##plot lines shock emission
ax2.plot([X[0], 0.415], [1.05, 1.05], 'r--') #[3.6]−[4.5] > 1.05
ax2.plot([0.415, 0.85], [1.05, 2.0], 'r--') 
ax2.plot([0.85, 0.85], [2.0, Y[1]], 'r--')
##plot lines PAH-contaminated apertures
ax2.plot([X[1], 1.77], [1.65, 1.65], 'r--')
ax2.plot([1.77, 0.7+(Y[0]+0.15) / 1.4], [1.65, Y[0]], 'r--')

##the following constraints are likely
##dominated by shock emission and thus are removed
Index_4 = np.where((Data['_3.6mag'] - Data['_4.5mag'] > 2.18 * \
                   (Data['_4.5mag'] - Data['_5.8mag'] - 0.3) + 0.8) & \
                   (Data['_4.5mag'] - Data['_5.8mag'] <= 0.85) & \
                   (Data['_3.6mag'] - Data['_4.5mag'] > 1.05))
Data.remove_rows(Index_4)

##All sources that obey all of the following constraints are consistent
##with sources that have PAH-contaminated apertures, ignore sigma = errors
Index_5 = np.where((Data['_3.6mag'] - Data['_4.5mag'] <= 1.4 * \
                   (Data['_4.5mag'] - Data['_5.8mag'] - 0.7) + 0.15) & \
                   (Data['_3.6mag'] - Data['_4.5mag'] <= 1.65))

Data.remove_rows(Index_5)

ax2.scatter(Data['_4.5mag'] - Data['_5.8mag'], \
            Data['_3.6mag'] - Data['_4.5mag'], \
            s = 10, c = 'green', label = 'YSOs')
ax2.legend()
plt.show()


##classification
Data['Class'] = 'none'
## prepare empty figures and add two axes for two criteria
fig = plt.figure(figsize=(13, 6), dpi=100)

'''
Class I objects
'''
##Class I objects, [3.6]-[4.5] versus [4.5]−[5.8]
ax1 = fig.add_axes([0.07, 0.11, 0.38, 0.80])
ax1.set_title('Class I objects')
ax1.set_xlabel('[4.5]-[5.8]')
ax1.set_ylabel('[3.6]-[4.5]')
ax1.minorticks_on()

##raw data in first axes
ax1.scatter(Data['_4.5mag'] - Data['_5.8mag'], \
            Data['_3.6mag'] - Data['_4.5mag'], \
            s = 10, c = 'green', label = 'Cleared YSOs')
##get axis limits
Y = ax1.get_ylim() #[-1.0, 3.5] #
X = ax1.get_xlim() #[-1.0, 3.0] #
ax1.set_xlim(X)
ax1.set_ylim(Y)
##plot lines
ax1.plot([X[1], 0.7], [0.7, 0.7], 'r--')
ax1.plot([0.7, 0.7], [0.7, Y[1]], 'r--')

Class_I = np.where((Data['_4.5mag'] - Data['_5.8mag'] > 0.7) &\
                   (Data['_3.6mag'] - Data['_4.5mag'] > 0.7)) 

ax1.scatter(Data['_4.5mag'][Class_I] - Data['_5.8mag'][Class_I], \
            Data['_3.6mag'][Class_I] - Data['_4.5mag'][Class_I], \
            s = 10, c = 'red', label = 'Class I')
ax1.legend()
Data['Class'][Class_I] = 'I'

'''
Class II objects
'''
####Class II objects, [3.6]-[5.8] versus [4.5]−[8.0]
ax2 = fig.add_axes([0.52, 0.11, 0.38, 0.80])
ax2.set_title('Class II objects')
ax2.set_xlabel('[4.5]-[8.0]')
ax2.set_ylabel('[3.6]-[5.8]')
ax2.minorticks_on()

##raw data in first axes
cb = ax2.scatter(Data['_4.5mag'] - Data['_8.0mag'], \
            Data['_3.6mag'] - Data['_5.8mag'], \
            s = 10, c = Data['_3.6mag']-Data['_4.5mag'])

ax2.scatter(Data['_4.5mag'][Class_I] - Data['_8.0mag'][Class_I], \
            Data['_3.6mag'][Class_I] - Data['_5.8mag'][Class_I], \
            s = 20, facecolor = 'None', edgecolor = 'red', lw = 1.0, \
            label = 'Class I')

##get axis limits
Y = ax2.get_ylim() #[-2.0, 6.0] #
X = ax2.get_xlim() #[-2.0, 6.0] #
ax2.set_xlim(X)
ax2.set_ylim(Y)
##plot lines
ax2.plot([X[1], 0.5], [0.15, 0.15], 'r--')
ax2.plot([0.5, ((Y[1]-0.5)/3.5)+0.5], [0.15, Y[1]], 'r--')

Class_II = np.where((Data['_4.5mag'] - Data['_8.0mag'] > 0.5) & \
                    (Data['_3.6mag'] - Data['_5.8mag'] > 0.35) & \
                    (Data['_3.6mag'] - Data['_5.8mag'] <= 3.5 * \
                    (Data['_4.5mag'] - Data['_8.0mag'] - 0.5)+ 0.5) & \
                    (Data['_3.6mag'] - Data['_4.5mag']> 0.15))

Class_II = np.setdiff1d(Class_II, Class_I)
Data['Class'][Class_II] = 'II'

ax2.scatter(Data['_4.5mag'][Class_II] - Data['_8.0mag'][Class_II], \
            Data['_3.6mag'][Class_II] - Data['_5.8mag'][Class_II], \
            s = 20, facecolor = 'None', edgecolor = 'magenta', lw = 1.0, \
            label = 'Class II')
ax2.legend()
##colorbar
ax3 = fig.add_axes([0.925, 0.11, 0.02, 0.80])
# magnitude colorbar
fig.colorbar(cb, cax = ax3, label='[3.6]-[4.5]')
ax3.invert_yaxis()

plt.show()

print(Data)
##save table to local file
Data.write(Name.replace('.dat', '_class.dat'), format = 'ascii', \
                        delimiter='\t', overwrite=True)






