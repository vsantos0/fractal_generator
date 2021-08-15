from PIL import Image
import numpy as np
import math

x_resolution = 1000
y_resolution = 700

x_max, x_min = 1, -2.2
x_range = x_max - x_min

y_max, y_min = 1.2, -1.2
y_range = y_max - y_min

max_iterations = 100

def get_iter(c):
    z = 0
    N = 0
    while abs(z) < 2 and N < max_iterations:
        # z = complex(abs(z.real), abs(z.imag))**2 + c
        if (z**2 + 1) != 0:
            z = (1 / (z**2 + 1)) + c
        else:
            z += c
        N += 1
    return N

def mandelbrot_set(r, g, b):
    mandelbrot_set = Image.new('RGB', (x_resolution, y_resolution), 'white')
    pixels = mandelbrot_set.load()

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

    mandelbrot_set.show()

mandelbrot_set(0, 10, 10)
