import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data2 = pd.read_csv('nodeVSmemory.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data2['Nodes'], data2['Memory'], marker='o', linestyle='-')

# Add labels and title
plt.xlabel('Number of Nodes')
plt.ylabel('Memory Usage (Bytes)')
plt.title('Number of Nodes VS Auxiliary Memory Usage')

# Show the plot
plt.grid(True)
plt.show()
