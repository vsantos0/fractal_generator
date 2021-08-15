from PIL import Image

x_resolution = 1000
y_resolution = 1000

x_max, x_min = 1.5, -1.5
x_range = x_max - x_min

y_max, y_min = 1.5, -1.5
y_range = y_max - y_min

max_iterations = 100

# c is initial complex value, deg is degree, max_iter is max_iteration
def julia_set(re, im, r, g, b):
    c = complex(re, im)
    max_z_abs = max(2, abs(c))

    julia_set = Image.new('RGB', (x_resolution, y_resolution), 'white')
    pixels = julia_set.load()

    for x in range(x_resolution):
        z_re = (x / x_resolution) * x_range + x_min
        for y in range(y_resolution):
            z_im = (y / y_resolution) * y_range + y_min
            z = complex(z_re, z_im)

            N = 0
            while abs(z) < max_z_abs and N < max_iterations:
                # z = complex(abs(z.real), abs(z.imag))**2 + c
                if (z**2 + 1) != 0:
                    z = (1 / (z**2 + 1)) + c
                else:
                    z += c
                N += 1
            
            if N >= max_iterations:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (N * r, N * g, N * b)
    
    julia_set_flipped = julia_set.transpose(method=Image.FLIP_TOP_BOTTOM)
    julia_set_flipped.show()

# julia_set(-0.7, 0.27015, 0, 10, 10)
# julia_set(-0.423, 0.745, 0, 10, 10)
julia_set(-0.9, -0.2, 0, 10, 10)
# julia_set(-2, 0, 0, 10, 10)