import matplotlib.pyplot as plt
import numpy as np

# Define the labels and values
labels = ['Reno', 'New Reno']
upload_values = [23526,33926]  # replace with your upload values
download_values = [27129,34966]  # replace with your download values

# Define the x locations for the groups
x = np.arange(len(labels))

# Define the width of the bars
width = 0.35

# Plot the data
plt.figure(figsize=(10,6))
plt.bar(x - width/2, upload_values, width, label='Upload')
plt.bar(x + width/2, download_values, width, label='Download')

# Add labels and title
plt.xlabel('TCPs')
plt.ylabel('Bytes per second')
plt.title('Throughput comparison')

# Add xticks
plt.xticks(x, labels)

# Add legend
plt.legend()

# Show the plot
plt.show()