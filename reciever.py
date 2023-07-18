import numpy as np
import adi
import matplotlib.pyplot as plt
import time

sample_rate = 1e6  # Hz
center_freq = 1000e6  # Hz
num_samps = 10000  # number of samples per call to rx()

# Transmitter configuration
sdr = adi.Pluto("ip:192.168.2.1")  # Replace with the IP address of the transmitter device
sdr.sample_rate = int(sample_rate)
sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = 0  # Increase to increase tx power, valid range is -90 to 0 dB

# Transmit Sinewave
fc = 2000
ts = 1 / float(sample_rate)
t = np.arange(0, num_samps * ts, ts)
x_symbols_i = np.sin(2 * np.pi * t * fc)  # Amplitude of the I-signal
x_symbols_q = np.cos(2 * np.pi * t * fc)  # Amplitude of the Q-signal
x_symbols_iq = x_symbols_i + 1j * x_symbols_q  # j = sqrt(-1). This is the IQ signal
samples = np.repeat(x_symbols_iq, 1)
samples *= 2 ** 14  # Scale the signal according to the range of the SDR

# Start transmitting
sdr.tx_cyclic_buffer = True  # Enable cyclic buffers
sdr.tx(samples)  # Start transmitting

while True:
    # Plot transmitted signal
    plt.figure(0)
    plt.clf()
    plt.subplot(2, 2, 1)
    plt.plot(t, np.real(samples))
    plt.ylabel("Amplitude")
    plt.title('Transmitted - Time Domain')
    plt.xlabel("Time")

    # Plot signal constellation
    plt.subplot(2, 2, 2)
    plt.plot(np.real(samples), np.imag(samples), 'b.')
    plt.xlabel("I")
    plt.ylabel("Q")
    plt.title("Transmitted - Signal Constellation")

    plt.pause(0.05)

    time.sleep(2)
