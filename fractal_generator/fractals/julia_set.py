from PIL import Image
import numpy as np

x_resolution = 1000
y_resolution = 1000

x_max, x_min = 1.5, -1.5
x_range = x_max - x_min

y_max, y_min = 1.5, -1.5
y_range = y_max - y_min

max_iterations = 100

# c is initial complex value, deg is degree, max_iter is max_iteration
def julia_set(re, im, deg, r, g, b):
    c = complex(re, im)
    max_z_abs = max(2, abs(c))

    js_img = Image.new('RGB', (x_resolution, y_resolution), 'white')
    pixels = js_img.load()

    for x in range(x_resolution):
        z_re = (x / x_resolution) * x_range + x_min
        for y in range(y_resolution):
            z_im = (y / y_resolution) * y_range + y_min
            z = complex(z_re, z_im)

            N = 0
            while abs(z) < max_z_abs and N < max_iterations:
                z = z**deg + c
                N += 1
            
            if N >= max_iterations:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (N * r, N * g, N * b)
    
    js_img.transpose(method=Image.FLIP_TOP_BOTTOM).show()

def julia_set_np(c_re, c_im, deg, x0=0, y0=0, zoom=2):
    x_init = x0 - x_range / zoom
    x_final = x0 + x_range / zoom
    y_init = y0 - y_range / zoom
    y_final = y0 + y_range / zoom

    c = complex(c_re, c_im)
    max_z_abs = max(2, abs(c))

    x = np.linspace(x_init, x_final, x_resolution).reshape((1, x_resolution))
    y = np.linspace(y_init, y_final, y_resolution).reshape((y_resolution, 1))
    z = x + 1j * y

    c = np.full(z.shape, c)

    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iterations):
        z[m] = z[m]**deg + c[m]

        m[np.abs(z) > max_z_abs] = False
        div_time[m] = i

    return div_time

# julia_set(-0.7, 0.27015, 2, 0, 10, 10)
# julia_set(-0.423, 0.745, 2, 0, 10, 10)
# julia_set(-1, -1, 2, 0, 10, 10)

# julia_set_np(-0.423, 0.745, 2, 'terrain')
# julia_set_np(-0.7, 0.27015, 2, 'magma')
