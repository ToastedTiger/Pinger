# =============================================================================
# Author:       BM Dierks
# Created:      2020/09/12
# Last Edit:    2020/09/13
# Description:  The inteded purpose of this program is to ping a given website 
#               (google in this case). The returned pings are then graphed in 
#               order to observed the stability of the connection.
#
#               Requires pythonping to be installed in root directory.
# =============================================================================

from pythonping import ping
import matplotlib.pyplot as plot
import numpy as np

# Variables to set
# Threshold below which latency is acceptable in ms
Threshold = 80

# Amount of pings to send
x = range(0,500)

# Size of package to send
package = 50

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

print ("Maximum Latency: \t", max(y), "\nMinimum Latency: \t", min(y), "\nAverage Latency: \t", round(np.average(y),2))

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
            
# Plot results
plot.figure(figsize=(15, 10))
plot.xlabel("Pings[#]")
plot.ylabel("Latency[ms]")
plot.plot(x,yThreshold,'g')
plot.plot(x,y, 'b')
plot.plot(x,yOver, 'r')


print ("DONE!!!")