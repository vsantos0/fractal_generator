import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from tkinter.constants import END
from fractal_generator.fractals.julia_set import julia_set, julia_set_np
from fractal_generator.helpers import raise_frame
import matplotlib.pyplot as plt
import sqlite3 as sql
from datetime import datetime

def new_js(js_frame, main_frame):
    color_name = StringVar()
    color_list = ['viridis', 'plasma', 'magma', 'cividis', 'terrain'] 

    def get_entries():
        c_re = float(c_re_entry.get())
        c_im = float(c_im_entry.get())
        deg = float(deg_entry.get())
        xcord = float(xcord_entry.get())
        ycord = float(ycord_entry.get())
        zoom = float(zoom_entry.get())
        color = color_options.get()

        return c_re, c_im, deg, xcord, ycord, zoom, color
    
    def fill_entries(id, records):
        record = records[int(id) - 1]

        c_re_entry.delete(0, END)
        c_im_entry.delete(0, END)
        deg_entry.delete(0, END)
        xcord_entry.delete(0, END)
        ycord_entry.delete(0, END)
        zoom_entry.delete(0, END)
        color_options.delete(0, END)

        c_re_entry.insert(0, record[0])
        c_im_entry.insert(0, record[1])
        deg_entry.insert(0, record[2])
        xcord_entry.insert(0, record[3])
        ycord_entry.insert(0, record[4])
        zoom_entry.insert(0, record[5])
        color_options.insert(0, record[6])


    def on_close(event):
        response = messagebox.askyesno("Save", "Do you want to save the parameters used?")
        if response == 1:
            params = get_entries()
            conn = sql.connect('./data/record.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS juliaset (
                    c_real REAL,
                    c_imag REAL,
                    deg REAL,
                    xcord REAL,
                    ycord REAL,
                    zoom REAL,
                    color TEXT,
                    generated DATETIME
                    );""")
            
            c.execute("INSERT INTO juliaset VALUES (:c_real, :c_imag, :deg, :xcord, :ycord, :zoom, :color, :generated)",
                    {
                        'c_real': params[0],
                        'c_imag': params[1],
                        'deg': params[2],
                        'xcord': params[3],
                        'ycord': params[4],
                        'zoom': params[5],
                        'color': params[6],
                        'generated': datetime.now().replace(microsecond=0)
                    })
            
            conn.commit()
            conn.close()

    def generate():
        params = get_entries()
        div_time = julia_set_np(c_re=params[0], c_im=params[1], deg=params[2], 
                                x0=params[3], y0=params[4], 
                                zoom=params[5])

        fig, _ = plt.subplots(figsize=(7, 7))
        fig.canvas.mpl_connect('close_event', on_close)
        plt.imshow(div_time, cmap=params[6])
        plt.gca().set_axis_off()
        plt.gca().invert_xaxis()
        plt.tight_layout(pad=0)

        plt.show()
    
    def configure_load_window(records):
        data = ''
        for record in records:
            items = list(record)
            for i in range(len(items)):
                items[i] = str(items[i])

            data += '       |       '.join(items) + "\n"

        js_data_window = tk.Tk()
        js_data_window.title("Julia Set Record")
        js_data_window.config(bg='#000000')

        table_header = "Real part of c | Imaginary part of c | Degree | x coord | y coord | Zoom | Color | Generated at | ID"
        table_header_label = tk.Label(js_data_window, text=table_header, bg='#000000', font=(None, 20))
        table_header_label.pack(pady=(0, 20))
        
        js_record_label = tk.Label(js_data_window, text=data, bg='#000000')
        js_record_label.pack(pady=(0, 20))

        fill_label = tk.Label(js_data_window, text="Choose ID", bg='#000000')
        fill_label.pack()

        fill_entry = tk.Entry(js_data_window)
        fill_entry.pack(pady=(0, 20))

        fill_button = tk.Button(js_data_window, text="Fill", command=lambda:fill_entries(fill_entry.get(), records), highlightbackground='#000000')
        fill_button.pack(pady=(0,20))

    
    def load():
        conn = sql.connect('./data/record.db')
        c = conn.cursor()
        table_exists = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='juliaset';""").fetchall()

        if table_exists == []:
            messagebox.showerror("Error", "You do not have any data stored.")
            return
        
        c.execute("SELECT *, oid FROM juliaset")
        records = c.fetchall()

        configure_load_window(records)

        conn.commit()
        conn.close()


    title = tk.Label(js_frame, text="Julia Set", font=(None, 40), bg='#000000')
    title.pack(pady=(20, 50))

    c_re_label = tk.Label(js_frame, text="Real part of c", bg='#000000')
    c_re_label.pack()

    c_re_entry = tk.Entry(js_frame)
    c_re_entry.pack(pady=(0, 20))

    c_im_label = tk.Label(js_frame, text="Imaginary part of c", bg='#000000')
    c_im_label.pack()

    c_im_entry = tk.Entry(js_frame)
    c_im_entry.pack(pady=(0, 20))

    deg_label = tk.Label(js_frame, text="Degree", bg='#000000')
    deg_label.pack()

    deg_entry = tk.Entry(js_frame)
    deg_entry.pack(pady=(0, 20))

    xcord_label = tk.Label(js_frame, text="x coordinate", bg='#000000')
    xcord_label.pack()

    xcord_entry = tk.Entry(js_frame)
    xcord_entry.pack(pady=(0, 20))

    ycord_label = tk.Label(js_frame, text="y coordinate", bg='#000000')
    ycord_label.pack()

    ycord_entry = tk.Entry(js_frame)
    ycord_entry.pack(pady=(0, 20))

    zoom_label = tk.Label(js_frame, text="Zoom", bg='#000000')
    zoom_label.pack()

    zoom_entry = tk.Entry(js_frame)
    zoom_entry.pack(pady=(0, 20))

    color = tk.Label(js_frame, text="Color: ", bg='#000000')
    color.pack()

    color_options = ttk.Combobox(js_frame, textvariable=color_name, values=color_list)
    color_options.pack(pady=(0, 20))
    color_options.current(0)

    gen_button = tk.Button(js_frame, text="Generate", command=generate, highlightbackground='#000000')
    gen_button.pack(pady=(0, 20))

    back_button = tk.Button(js_frame, text="Back", command=lambda:raise_frame(main_frame), highlightbackground='#000000')
    back_button.pack(side=tk.LEFT, pady=(0, 20))

    load_button = tk.Button(js_frame, text="Load", command=load, highlightbackground='#000000')
    load_button.pack(side=tk.RIGHT, pady=(0, 20))
