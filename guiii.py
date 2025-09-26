"""
Basic Unit Converter - Tkinter GUI
"""
import tkinter as tk
from tkinter import ttk, messagebox

def convert_length(value, from_unit, to_unit):
    units = {
        'meter': 1.0,
        'kilometer': 1000.0,
        'centimeter': 0.01,
        'millimeter': 0.001,
        'mile': 1609.34,
        'yard': 0.9144,
        'foot': 0.3048,
        'inch': 0.0254
    }
    if from_unit not in units or to_unit not in units:
        raise ValueError('Invalid unit')
    value_in_meters = value * units[from_unit]
    return value_in_meters / units[to_unit]

def on_convert():
    try:
        value = float(entry_value.get())
        from_unit = combo_from.get()
        to_unit = combo_to.get()
        result = convert_length(value, from_unit, to_unit)
        label_result.config(text=f'{value} {from_unit} = {result:.4f} {to_unit}')
    except Exception as e:
        messagebox.showerror('Error', str(e))

def main():
    root = tk.Tk()
    root.title('Basic Unit Converter')
    root.geometry('350x200')

    units = ['meter', 'kilometer', 'centimeter', 'millimeter', 'mile', 'yard', 'foot', 'inch']

    tk.Label(root, text='Value:').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global entry_value
    entry_value = tk.Entry(root)
    entry_value.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text='From:').grid(row=1, column=0, padx=10, pady=10, sticky='e')
    global combo_from
    combo_from = ttk.Combobox(root, values=units, state='readonly')
    combo_from.grid(row=1, column=1, padx=10, pady=10)
    combo_from.current(0)

    tk.Label(root, text='To:').grid(row=2, column=0, padx=10, pady=10, sticky='e')
    global combo_to
    combo_to = ttk.Combobox(root, values=units, state='readonly')
    combo_to.grid(row=2, column=1, padx=10, pady=10)
    combo_to.current(1)

    btn_convert = tk.Button(root, text='Convert', command=on_convert)
    btn_convert.grid(row=3, column=0, columnspan=2, pady=10)

    global label_result
    label_result = tk.Label(root, text='')
    label_result.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
