# =============================================================================
# Author:       BM Dierks
# Created:      2020/09/12
# Last Edit:    2020/09/13
# Description:  The intended purpose of this program is to ping a given website 
#               (google in this case). The returned pings are then graphed in 
#               order to observed the stability of the connection.
#
#               Requires pythonping to be installed in root directory.
# =============================================================================

from pythonping import ping
import matplotlib.pyplot as plot
import numpy as np
from datetime import datetime

timeStart = datetime.now()
# Variables to set
# Threshold below which latency is acceptable in ms
Threshold = 80

# Amount of pings to send
pingCount = 2000
x = range(0,pingCount)

# Size of package to send
package = 64

# Maximum timout time in sec
timeout = 2

# Initiates variables
x1 = []
y = []
yThreshold = []
yOver = []
overVal = []
futFlag = False

# Loop to ping server
for i in x:
    latency = ping('www.google.com',size = (package-8) ,count = 1, timeout = timeout)
    CurrentPing = latency.rtt_min_ms
    yThreshold.append(Threshold)
    y.append(CurrentPing)
    if CurrentPing < Threshold:
        yOver.append(None)
    else:
        yOver.append(CurrentPing)

runTime = datetime.now()-timeStart

# Write pings above threshold to new array
for i in x:
    if yOver[i]:
        if i !=0:
            yOver[i-1] = y[i-1]
        if i !=len(yOver)-1:
            futFlag = True
    elif futFlag and not yOver[i]:
        yOver[i] = y[i]
        futFlag = False

stdDev=round(np.std(y), 2)
runTimeSec = runTime.seconds+runTime.microseconds*1e-6

# Print out network statistics
print ("\nPing Information:\n------------------")
print ("Maximum Latency\t\t: \t", max(y), "ms\nMinimum Latency\t\t: \t", min(y), "ms\nAverage Latency\t\t: \t", round(np.average(y),2),"ms")
print ("Standard Deviation\t:\t", stdDev,"ms")
print ("Total Runtime\t\t: \t", runTime.seconds,"s", int(round(runTime.microseconds/10000, 0)*10),"ms")
print ("Average Speed\t\t: \t", round(8*pingCount*package/pow(1024,2)*runTimeSec,2),"Mbps")


# Plot results
plot.figure(figsize=(15, 10))
plot.plot(x,yThreshold,'g')
plot.plot(x,y, 'b')
plot.plot(x,yOver, 'r')
plot.xlabel("Pings[#]")
#secax = ax.secondary_xaxis('top')#, functions=(forward, inverse))
#secax.xaxis.set_minor_locator(AutoMinorLocator())
#secax.set_xlabel('$X_{other}$')

plot.ylabel("Latency[ms]")

plot.show()



# Program Done
print ("DONE!!!") 