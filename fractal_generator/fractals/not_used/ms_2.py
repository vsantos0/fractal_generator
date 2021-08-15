from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

x_resolution = 1000
y_resolution = 750

x_max, x_min = 1, -2.2
x_range = x_max - x_min

y_max, y_min = 1.2, -1.2
y_range = y_max - y_min

max_iterations = 100

def ms_2(r, g, b):
    x = np.linspace(x_min, x_max, x_resolution).reshape((1, x_resolution))
    y = np.linspace(y_min, y_max, y_resolution).reshape((y_resolution, 1))
    c = x + 1j * y

    z = np.zeros(c.shape, dtype=np.complex128)
    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iterations):
        z[m] = z[m]**2 + c[m]

        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)

        div_time[diverged] = i
        m[np.abs(z) > 2] = False
    
    # print(div_time.shape)
    
    # mandelbrot_set = Image.fromarray(div_time.astype(np.uint8)).convert('RGB')

    # data = np.array(mandelbrot_set)

    # data[:,:,0] = data[:,:,0] * r
    # data[:,:,1] = data[:,:,1] * g
    # data[:,:,2] = data[:,:,2] * b

    # im2 = Image.fromarray(data).convert('RGB')
    # im2.show()

    # for x in range(mandelbrot_set.size[0]):
    #     for y in range(mandelbrot_set.size[1]):
    #         curr = mandelbrot_set.getpixel((x, y))
    #         new_color = (curr[0] * r, curr[1] * g, curr[2] * b)
    #         mandelbrot_set.putpixel((x, y), new_color)
            
    # mandelbrot_set.show()

    plt.imshow(div_time, cmap='terrain')
    plt.gca().set_axis_off()
    # plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
    #         hspace = 0, wspace = 0)
    # plt.margins(0,0)
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())   
    plt.tight_layout(pad=0)
    # plt.margins(0)

    plt.show()
    # plt.savefig('image.png', bbox_inches='tight', pad_inches = 0)


ms_2(2, 3, 1)
