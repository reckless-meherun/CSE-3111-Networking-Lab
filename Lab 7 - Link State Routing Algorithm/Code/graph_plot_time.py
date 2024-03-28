import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data1 = pd.read_csv('nodeVStime.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data1['Nodes'], data1['Times'], label='Time VS Nodes')  # Corrected column name to 'Time'

# Add labels and title
plt.xlabel('Number of Nodes')
plt.ylabel('Time (ms)')
plt.title('Number of Nodes VS Time')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
