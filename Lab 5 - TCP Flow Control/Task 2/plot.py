import pandas as pd
import matplotlib.pyplot as plt

def get_line_plot():
    sample_rtt = pd.read_csv('sampleRTT.csv')
    est_rtt = pd.read_csv('estRTT.csv')

    plt.plot(sample_rtt['SL'],sample_rtt['SampleRTT'],label='Sample RTT')
    plt.plot(est_rtt['SL'],est_rtt['EstimatedRTT'],label='Estimated RTT')

    plt.xlabel('Sequence Number')
    plt.ylabel('Time (ms)')
    plt.title('Sample RTT vs Estimated RTT')
    plt.legend()

    plt.show()
