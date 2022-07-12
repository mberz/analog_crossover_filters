# %%
from lcapy import Circuit
import numpy as np
import sympy as sym
import pyfar as pf

# %%
# Create the netlist of a second oder low-pass filter
lp_2nd_order = Circuit(
    """
    P1 1 0; down=1.5, v=v_i(t)
    L 1 2 ; right
    R 2 3; right
    C 3 0_3; down
    W 0 0_3; right
    W 3 4; right
    W 0_3 0_4; right
    R_L 4 0_4; down, v^=v_o(t)""")

lp_2nd_order.draw()

# Calculate the transfer function as a symbolic function
H_2nd_order = lp_2nd_order.transfer(1, 0, 3, 0)

# %%
expr = H_2nd_order.as_expr()
symbols = expr.symbols.copy()
symbols_list = [symbol for symbol in symbols]

# Create a lambda function with numpy optimization for numeric evaluation
func = sym.lambdify(symbols_list, expr.expr, 'numpy')

# %%
# R_L is the load impedance, in reality a loudspeaker
symbols['R_L'] = 8

# R, L, and C specify the filter, R is the inductor wire's DC resistance
symbols['R'] = 0.1
symbols['L'] = 1e-3
symbols['C'] = 10e-6


# The cutoff frequency of the filter is calculated as
f_c = 1/2/np.pi/np.sqrt(symbols['L']*symbols['C'])
f_c
# %%
# The Laplace variable
freqs = np.linspace(20, 20e3, 2**12)
s = 2*np.pi*1j*freqs
symbols['s'] = s

# %%
# Calculate the transfer function using numeric values
H_eval = func(**symbols)

# %%
# Create a digital second order IIR butterworth filter for comparison
impulse = pf.signals.impulse(2**12, sampling_rate=192e3)
h_butter = pf.dsp.filter.butterworth(impulse, 2, f_c)

# %%
# Plot
ax = pf.plot.freq_phase(h_butter, label='Digital IIR')
ax[0].plot(freqs, 20*np.log10(np.abs(H_eval)), label='Analog', linestyle='-.')
ax[0].axvline(f_c, color='k', linestyle=':', label='$f_c$')
ax[1].plot(freqs, (np.angle(H_eval)), linestyle='-.')
ax[1].axvline(f_c, color='k', linestyle=':')
ax[0].legend()
ax[0].set_xlim([20, 20e3])
ax[1].set_xlim([20, 20e3])

# %%
