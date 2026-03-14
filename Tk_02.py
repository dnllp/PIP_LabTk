# Lab Tk-2: Panel de control con grid y pestañas
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Lab Tk-2 — Layout')
root.geometry('560x420')

# ── NOTEBOOK (pestañas) ───────────────────────────────────────
nb = ttk.Notebook(root)
nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ── PESTAÑA 1: formulario con grid ───────────────────────────
tab1 = tk.Frame(nb, bg='#f5f5f5')
nb.add(tab1, text='  📋 Configuración  ')

# LabelFrame agrupa widgets con un borde y título
grp_sensor = tk.LabelFrame(tab1, text='Parámetros del sensor',
    bg='#f5f5f5', fg='#1a3a5c', font=('Arial',10,'bold'), pady=8, padx=10)
grp_sensor.grid(row=0, column=0, padx=16, pady=12, sticky='ew')

# Widgets en grid — row, column, sticky='w' para alinear a la izquierda
campos = [
    ('Puerto serial:',  'COM3'),
    ('Baud rate:',      '115200'),
    ('Período (ms):',   '500'),
    ('Umbral T° (°C):', '35.0'),
]
vars_config = {}
for i, (lbl, default) in enumerate(campos):
    tk.Label(grp_sensor, text=lbl, bg='#f5f5f5',
             font=('Arial',10), anchor='w').grid(
        row=i, column=0, sticky='w', pady=4)
    var = tk.StringVar(value=default)
    vars_config[lbl] = var
    tk.Entry(grp_sensor, textvariable=var, width=18,
             font=('Arial',10)).grid(row=i, column=1, padx=8, pady=4)

# Checkbutton
var_guardar = tk.BooleanVar(value=True)
tk.Checkbutton(tab1, text='Guardar log automáticamente',
    variable=var_guardar, bg='#f5f5f5', font=('Arial',10)
).grid(row=1, column=0, sticky='w', padx=16, pady=4)

# Radiobuttons — protocolo
grp_proto = tk.LabelFrame(tab1, text='Protocolo', bg='#f5f5f5',
    font=('Arial',10,'bold'), padx=10, pady=6)
grp_proto.grid(row=2, column=0, padx=16, pady=6, sticky='ew')
var_proto = tk.StringVar(value='ASCII')
for proto in ['ASCII', 'Binario', 'Modbus RTU']:
    tk.Radiobutton(grp_proto, text=proto, variable=var_proto,
        value=proto, bg='#f5f5f5', font=('Arial',10)
    ).pack(side=tk.LEFT, padx=12)

# Botón aplicar
def aplicar_config():
    from tkinter import messagebox
    resumen = '\n'.join(f'{k} {v.get()}' for k,v in vars_config.items())
    messagebox.showinfo('Configuración aplicada', resumen)

tk.Button(tab1, text='Aplicar configuración', command=aplicar_config,
    bg='#2E75B6', fg='white', font=('Arial',11,'bold'),
    relief=tk.FLAT, pady=6
).grid(row=3, column=0, padx=16, pady=12, sticky='ew')

# ── PESTAÑA 2: indicadores con place ─────────────────────────
tab2 = tk.Frame(nb, bg='#1e2736')
nb.add(tab2, text='  📊 Monitor  ')

# Progressbar como indicador de temperatura
tk.Label(tab2, text='Temperatura', bg='#1e2736', fg='#94a3b8',
    font=('Arial',9)).place(x=20, y=20)
pb_temp = ttk.Progressbar(tab2, length=300, maximum=100, mode='determinate')
pb_temp.place(x=20, y=42)
lbl_temp_val = tk.Label(tab2, text='-- °C', bg='#1e2736',
    fg='#ef4444', font=('Courier New', 20, 'bold'))
lbl_temp_val.place(x=340, y=32)

tk.Label(tab2, text='Humedad', bg='#1e2736', fg='#94a3b8',
    font=('Arial',9)).place(x=20, y=80)
pb_hum  = ttk.Progressbar(tab2, length=300, maximum=100, mode='determinate')
pb_hum.place(x=20, y=102)
lbl_hum_val = tk.Label(tab2, text='-- %', bg='#1e2736',
    fg='#22c55e', font=('Courier New', 20, 'bold'))
lbl_hum_val.place(x=340, y=92)

# Simular actualización de valores
import random
def simular():
    t = random.uniform(20, 45)
    h = random.uniform(30, 90)
    pb_temp['value'] = t
    pb_hum['value']  = h
    lbl_temp_val.config(text=f'{t:.1f} °C')
    lbl_hum_val.config(text=f'{h:.1f} %')
    root.after(800, simular)   # repetir cada 800 ms

simular()
root.mainloop()
