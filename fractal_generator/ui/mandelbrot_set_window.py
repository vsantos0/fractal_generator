import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from tkinter.constants import END
from fractal_generator.fractals.mandelbrot_set import mandelbrot_set, mandelbrot_set_np
from fractal_generator.helpers import raise_frame
import matplotlib.pyplot as plt
import sqlite3 as sql
from datetime import datetime

def new_ms(ms_frame, main_frame):
    color_name = StringVar()
    color_list = ['viridis', 'plasma', 'magma', 'cividis', 'terrain'] 

    def get_entries():
        xcord = float(xcord_entry.get())
        ycord = float(ycord_entry.get())
        zoom = float(zoom_entry.get())
        color = color_options.get()

        return xcord, ycord, zoom, color
    
    def fill_entries(id, records):
        record = records[int(id) - 1]

        xcord_entry.delete(0, END)
        ycord_entry.delete(0, END)
        zoom_entry.delete(0, END)
        color_options.delete(0, END)

        xcord_entry.insert(0, record[0])
        ycord_entry.insert(0, record[1])
        zoom_entry.insert(0, record[2])
        color_options.insert(0, record[3])
    
    def on_close(event):
        response = messagebox.askyesno("Save", "Do you want to save the parameters used?")
        if response == 1:
            params = get_entries()
            conn = sql.connect('./data/record.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS mandelbrotset (
                    xcord REAL,
                    ycord REAL,
                    zoom REAL,
                    color TEXT,
                    generated DATETIME
                    );""")
            
            c.execute("INSERT INTO mandelbrotset VALUES (:xcord, :ycord, :zoom, :color, :generated)",
                    {
                        'xcord': params[0],
                        'ycord': params[1],
                        'zoom': params[2],
                        'color': params[3],
                        'generated': datetime.now().replace(microsecond=0)
                    })
            
            conn.commit()
            conn.close()

    def generate():
        params = get_entries()
        div_time = mandelbrot_set_np(x0=params[0], y0=params[1], zoom=params[2])

        fig, _ = plt.subplots(figsize=(7, 5.25))
        fig.canvas.mpl_connect('close_event', on_close)
        plt.imshow(div_time, cmap=params[3])
        plt.gca().set_axis_off()
        plt.tight_layout(pad=0)

        plt.show()
    
    def configure_load_window(records):
        data = ''
        for record in records:
            items = list(record)
            for i in range(len(items)):
                items[i] = str(items[i])

            data += '       |       '.join(items) + "\n"

        ms_data_window = tk.Tk()
        ms_data_window.title("Mandelbrot Set Record")
        ms_data_window.config(bg='#000000')

        table_header = "x coord | y coord | Zoom | Color | Generated at | ID"
        table_header_label = tk.Label(ms_data_window, text=table_header, bg='#000000', font=(None, 20))
        table_header_label.pack(pady=(0, 20))
        
        ms_record_label = tk.Label(ms_data_window, text=data, bg='#000000')
        ms_record_label.pack(pady=(0, 20))

        fill_label = tk.Label(ms_data_window, text="Choose ID", bg='#000000')
        fill_label.pack()

        fill_entry = tk.Entry(ms_data_window)
        fill_entry.pack(pady=(0, 20))

        fill_button = tk.Button(ms_data_window, text="Fill", command=lambda:fill_entries(fill_entry.get(), records), highlightbackground='#000000')
        fill_button.pack(pady=(0,20))
    
    def load():
        conn = sql.connect('./data/record.db')
        c = conn.cursor()
        table_exists = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='mandelbrotset';""").fetchall()

        if table_exists == []:
            messagebox.showerror("Error", "You do not have any data stored.")
            return
        
        c.execute("SELECT *, oid FROM mandelbrotset")
        records = c.fetchall()

        configure_load_window(records)

        conn.commit()
        conn.close()

    title = tk.Label(ms_frame, text="Mandelbrot Set", font=(None, 40), bg='#000000')
    title.pack(pady=(20, 50))

    xcord_label = tk.Label(ms_frame, text="x coordinate", bg='#000000')
    xcord_label.pack()

    xcord_entry = tk.Entry(ms_frame)
    xcord_entry.pack(pady=(0, 20))

    ycord_label = tk.Label(ms_frame, text="y coordinate", bg='#000000')
    ycord_label.pack()

    ycord_entry = tk.Entry(ms_frame)
    ycord_entry.pack(pady=(0, 20))

    zoom_label = tk.Label(ms_frame, text="Zoom", bg='#000000')
    zoom_label.pack()

    zoom_entry = tk.Entry(ms_frame)
    zoom_entry.pack(pady=(0, 20))

    color = tk.Label(ms_frame, text="Color: ", bg='#000000')
    color.pack()

    color_options = ttk.Combobox(ms_frame, textvariable=color_name, values=color_list)
    color_options.pack(pady=(0, 20))
    color_options.current(0)

    gen_button = tk.Button(ms_frame, text="Generate", command=generate, highlightbackground='#000000')
    gen_button.pack(pady=(0, 20))

    back_button = tk.Button(ms_frame, text="Back", command=lambda:raise_frame(main_frame), highlightbackground='#000000')
    back_button.pack(side=tk.LEFT, pady=(0, 20))

    load_button = tk.Button(ms_frame, text="Load", command=load, highlightbackground='#000000')
    load_button.pack(side=tk.RIGHT, pady=(0, 20))
