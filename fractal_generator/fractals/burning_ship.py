import numpy as np

x_resolution = 1000
y_resolution = 750

x_max, x_min = 1, -2.2
x_range = x_max - x_min

y_max, y_min = 1.2, -1.2
y_range = y_max - y_min

max_iterations = 100

def burning_ship(x0=-0.5, y0=-0.5, zoom=2):
    x_init = x0 - x_range / zoom
    x_final = x0 + x_range / zoom
    y_init = y0 - y_range / zoom
    y_final = y0 + y_range / zoom

    x = np.linspace(x_init, x_final, x_resolution).reshape((1, x_resolution))
    y = np.linspace(y_init, y_final, y_resolution).reshape((y_resolution, 1))
    c = x + 1j * y

    z = np.zeros(c.shape, dtype=np.complex128)
    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iterations):
        z[m] = (np.abs(z.real[m]) + 1j * np.abs(z.imag[m]))**2+ c[m]

        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)

        div_time[diverged] = i
        m[np.abs(z) > 2] = False
    
    return div_time

# burning_ship('magma', x0=-1.7, y0=0, zoom=25)
