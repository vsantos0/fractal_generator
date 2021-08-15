from PIL import Image
import numpy as np

x_resolution = 1000
y_resolution = 750

x_max, x_min = 1, -2.2
x_range = x_max - x_min

y_max, y_min = 1.2, -1.2
y_range = y_max - y_min

max_iterations = 100

def get_iter(c):
    z = 0
    N = 0
    while abs(z) < 2 and N < max_iterations:
        z = z**2 + c
        N += 1
    return N

def mandelbrot_set(r, g, b):
    ms_img = Image.new('RGB', (x_resolution, y_resolution), 'white')
    pixels = ms_img.load()

    for x in range(x_resolution):
        z_re = (x / x_resolution) * x_range + x_min
        for y in range(y_resolution):
            z_im = (y / y_resolution) * y_range + y_min
            c = complex(z_re, z_im)

            n = get_iter(c)
    
            if n >= max_iterations:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (n * r, n * g, n * b)

    ms_img.show()

def mandelbrot_set_np(x0=-0.5, y0=0, zoom=2):
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
        z[m] = z[m]**2 + c[m]

        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)

        div_time[diverged] = i
        m[np.abs(z) > 2] = False
    
    return div_time

# mandelbrot_set_np('magma')
