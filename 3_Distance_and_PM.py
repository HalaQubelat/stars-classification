import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from scipy import stats
from scipy.optimize import curve_fit

def func(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))



Name = 'IC348_class.dat' ##set file name here

##read data from local file
Data = ascii.read(Name)
print(Data.info())

##prepare empty figure and add two axes
fig = plt.figure(figsize=(20, 10), dpi=100)
fig.suptitle('Proper motion', fontsize=15)
ax1 = fig.add_axes([0.05, 0.11, 0.42, 0.80])#left bottom width height of proper motion map(proper motion)
ax1.set_xlabel('pmRA (mas/year)')
ax1.set_ylabel('pmDE (mas/year)')
ax1.minorticks_on()

#ax2 = fig.add_axes([0.55, 0.11, 0.42, 0.80]) #of distance distribution

##set labels and ticks for first axes
#ax1.set_title('Proper motion', fontsize=17)
#ax1.set_xlabel('pmRA (mas/year)')
#ax1.set_ylabel('pmDE (mas/year)')
#ax1.minorticks_on()


##draw raw data in first axes
#alpha is the transperancy of the graph on matplotlib
#s is the marker size
mask = (Data['Class'] == 'III')
ax1.scatter(Data[mask]['pmRA'], Data[mask]['pmDE'], s = 10, c = 'magenta', \
            alpha = 0.5, label = 'Class III')
mask = (Data['Class'] == 'II')
ax1.scatter(Data[mask]['pmRA'], Data[mask]['pmDE'], s = 10, c = 'green', \
            alpha = 0.5, label = 'Class II')
mask = (Data['Class'] == 'I')
ax1.scatter(Data[mask]['pmRA'], Data[mask]['pmDE'], s = 10, c = 'red', \
            alpha = 0.5, label = 'Class I')
mask = (Data['Class'] == 'TD')
ax1.scatter(Data[mask]['pmRA'], Data[mask]['pmDE'], s = 10, c = 'blue', \
            alpha = 0.5, label = 'transition disk')
ax1.legend()
#plt.show()

##set labels and ticks for second axes
fig = plt.figure(figsize=(13, 6), dpi=100)
ax2 = fig.add_axes([0.55, 0.11, 0.42, 0.80]) #of distance distribution
fig.suptitle('Distance distribution', fontsize=15)
#ax2.set_title('Distance distribution', fontsize=17)
ax2.set_xlabel('Distance (pc)')
ax2.set_ylabel('Number of stars')
ax2.minorticks_on()

##Class III
#question
mask = (Data['Plx'] > 0.5)
Dist = Data[mask]
mask = (Dist['Class'] == 'III')
ax2.hist(1000./Dist[mask]['Plx'], bins=50, color = 'magenta', \
         alpha = 0.5, label = 'Class III')  
X = np.linspace(0, 1000, 50)
try:
    kernel = stats.gaussian_kde(1000./Dist[mask]['Plx'])
    Y = kernel(X)
    ax2.plot(X, Y*np.sum(mask)*np.sum(mask), 'm')
    C = np.argmax(Y)
    X_fit = X[C-5:C+5]
    Y_fit = Y[C-5:C+5]*np.sum(mask)*np.sum(mask)
    popt, pcov = curve_fit(func, X_fit, Y_fit, \
                           p0=(Y_fit.max(), X_fit.mean(), 100.))
    print('Class III distance = ' + str(round(popt[1], 1)))
except:
    pass

##Class II
mask = (Dist['Class'] == 'II')
ax2.hist(1000./Dist[mask]['Plx'], bins=50, color = 'green', \
         alpha = 0.5, label = 'Class II')
try:   
    kernel = stats.gaussian_kde(1000./Dist[mask]['Plx'])
    Y = kernel(X)
    ax2.plot(X, Y*np.sum(mask)*np.sum(mask), 'g')
    C = np.argmax(Y)
    X_fit = X[C-5:C+5]
    Y_fit = Y[C-5:C+5]*np.sum(mask)*np.sum(mask)
    popt, pcov = curve_fit(func, X_fit, Y_fit, \
                           p0=(Y_fit.max(), X_fit.mean(), 50.))
    print('Class II distance = ' + str(round(popt[1], 1)))
except:
    pass

##Class I
mask = (Dist['Class'] == 'I')
ax2.hist(1000./Dist[mask]['Plx'], bins=50, color = 'red', \
         alpha = 0.5, label = 'Class I')
try:  
    kernel = stats.gaussian_kde(1000./Dist[mask]['Plx'])
    Y = kernel(X)
    ax2.plot(X, Y*np.sum(mask)*np.sum(mask), 'r')
    C = np.argmax(Y)
    X_fit = X[C-5:C+5]
    Y_fit = Y[C-5:C+5]*np.sum(mask)*np.sum(mask)
    popt, pcov = curve_fit(func, X_fit, Y_fit, \
                           p0=(Y_fit.max(), X_fit.mean(), 50.))
    print('Class I distance = ' + str(round(popt[1], 1)))
except:
    pass

##Class TD
mask = (Dist['Class'] == 'TD')
ax2.hist(1000./Dist[mask]['Plx'], bins=50, color = 'blue', \
         alpha = 0.5, label = 'transition disk')
try:   
    kernel = stats.gaussian_kde(1000./Dist[mask]['Plx'])
    Y = kernel(X)
    ax2.plot(X, Y*np.sum(mask)*np.sum(mask), 'b')
    C = np.argmax(Y)
    X_fit = X[C-5:C+5]
    Y_fit = Y[C-5:C+5]*np.sum(mask)*np.sum(mask)
    popt, pcov = curve_fit(func, X_fit, Y_fit, \
                           p0=(Y_fit.max(), X_fit.mean(), 50.))
    print('TD distance = ' + str(round(popt[1], 1)))
except:
    pass

ax2.legend()
plt.show()


