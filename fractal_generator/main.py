import tkinter as tk
from ui.julia_set_window import new_js
from ui.mandelbrot_set_window import new_ms
from ui.burning_ship_window import new_bs
from helpers import raise_frame

root = tk.Tk()
root.title("Fractal Generator")
root.config(bg='#000000')

main_frame = tk.Frame(root, bg='#000000', padx=100)
js_frame = tk.Frame(root, bg='#000000', padx=100)
ms_frame = tk.Frame(root, bg='#000000', padx=100)
bs_frame = tk.Frame(root, bg='#000000', padx=100)

main_title = tk.Label(main_frame, text="Menu", font=(None, 40), bg='#000000')
main_title.pack(pady=(20, 150))

js_button = tk.Button(main_frame, text="Julia Set", command=lambda:raise_frame(js_frame), highlightbackground='#000000')
js_button.pack(pady=(0, 30))

ms_button = tk.Button(main_frame, text="Mandelbrot Set", command=lambda:raise_frame(ms_frame), highlightbackground='#000000')
ms_button.pack(pady=(0, 30))

bs_button = tk.Button(main_frame, text="Burning Ship", command=lambda:raise_frame(bs_frame), highlightbackground='#000000')
bs_button.pack(pady=(0, 30))

new_js(js_frame, main_frame)
new_ms(ms_frame, main_frame)
new_bs(bs_frame, main_frame)

for frame in (main_frame, js_frame, ms_frame, bs_frame):
    frame.grid(row=0, column=0, sticky='news')

raise_frame(main_frame)
root.mainloop()
