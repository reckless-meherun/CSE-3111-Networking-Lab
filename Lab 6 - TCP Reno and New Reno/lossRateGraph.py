import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data1 = pd.read_csv('RenoLossRate.csv')
data2 = pd.read_csv('NewRenoLossRate.csv')
# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data1['loss_rate'], data1['rtt'], label = 'TCP Reno')
plt.plot(data2['loss_rate'], data2['rtt'], label = 'TCP New Reno')

# Add labels and title
plt.xlabel('Error(%)')
plt.ylabel('Round Trip Time(ms)')
plt.title('TCP Loss Rates vs RTTs')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

