# Lab Tk-3: Indicadores visuales con Canvas
import tkinter as tk
import math, random

root = tk.Tk()
root.title('Lab Tk-3 — Canvas e Indicadores')
root.geometry('700x460')
root.configure(bg='#1e2736')

# ── A. LED INDICADOR ──────────────────────────────────────────
# Un óvalo que cambia de color según el estado
frame_leds = tk.LabelFrame(root, text='Estado del sistema',
    bg='#1e2736', fg='#94a3b8', font=('Arial',9))
frame_leds.grid(row=0, column=0, padx=16, pady=12, sticky='nw')

class LEDIndicador:
    COLORES = {'verde':('#22c55e','#15803d'), 'rojo':('#ef4444','#991b1b'),
               'amarillo':('#fbbf24','#92400e'), 'gris':('#64748b','#334155')}

    def __init__(self, parent, etiqueta, color_ini='gris', fila=0):
        self.canvas = tk.Canvas(parent, width=24, height=24,
            bg='#1e2736', highlightthickness=0)
        self.canvas.grid(row=fila, column=0, padx=(8,4), pady=4)
        self.oval = self.canvas.create_oval(2,2,22,22,
            fill=self.COLORES[color_ini][0], outline=self.COLORES[color_ini][1])
        tk.Label(parent, text=etiqueta, bg='#1e2736', fg='#cbd5e1',
            font=('Arial',10)).grid(row=fila, column=1, sticky='w')

    def set_color(self, color: str):
        c = self.COLORES.get(color, self.COLORES['gris'])
        self.canvas.itemconfig(self.oval, fill=c[0], outline=c[1])

led_conexion = LEDIndicador(frame_leds, 'Conexión serial', 'gris', 0)
led_sensor   = LEDIndicador(frame_leds, 'Sensor OK',       'gris', 1)
led_alarma   = LEDIndicador(frame_leds, 'Alarma activa',   'gris', 2)
led_log      = LEDIndicador(frame_leds, 'Guardando log',   'gris', 3)

# ── B. BARRA DE NIVEL DE TANQUE ───────────────────────────────
frame_tanque = tk.LabelFrame(root, text='Nivel de tanque',
    bg='#1e2736', fg='#94a3b8', font=('Arial',9))
frame_tanque.grid(row=0, column=1, padx=8, pady=12)

cv_tanque = tk.Canvas(frame_tanque, width=80, height=180,
    bg='#0f172a', highlightthickness=1, highlightbackground='#374151')
cv_tanque.pack(padx=12, pady=8)
# Marco del tanque
cv_tanque.create_rectangle(10,10,70,170, outline='#475569', width=2)
# Barra de nivel (empieza vacía)
barra_nivel = cv_tanque.create_rectangle(
    12, 168, 68, 168,   # vacío al inicio (y_top == y_bottom)
    fill='#3b82f6', outline='', tags='nivel')
lbl_nivel = tk.Label(frame_tanque, text='0 %', bg='#1e2736',
    fg='#3b82f6', font=('Courier New',12,'bold'))
lbl_nivel.pack()

def set_nivel(pct: float):
    """Actualizar barra de tanque — pct: 0.0 a 100.0"""
    pct = max(0, min(100, pct))
    altura = 156 * (pct / 100.0)   # altura total del área = 156 px
    y_top  = 168 - altura
    color  = '#22c55e' if pct > 50 else ('#fbbf24' if pct > 20 else '#ef4444')
    cv_tanque.coords(barra_nivel, 12, y_top, 68, 168)
    cv_tanque.itemconfig(barra_nivel, fill=color)
    lbl_nivel.config(text=f'{pct:.0f} %', fg=color)

# ── C. DIAL ANALÓGICO ─────────────────────────────────────────
frame_dial = tk.LabelFrame(root, text='Temperatura (°C)',
    bg='#1e2736', fg='#94a3b8', font=('Arial',9))
frame_dial.grid(row=0, column=2, padx=8, pady=12)

cv_dial = tk.Canvas(frame_dial, width=180, height=180,
    bg='#0f172a', highlightthickness=0)
cv_dial.pack(padx=8, pady=8)

# Arco del dial (semicírculo)
cv_dial.create_arc(20,20,160,160, start=0, extent=180,
    outline='#374151', width=3, style=tk.ARC)
# Marcas de escala (0–100°C)
cx, cy, r = 90, 140, 60
for i, val in enumerate(range(0, 101, 20)):
    angulo = math.radians(180 - (180 * i / 5))
    x1 = cx + (r-8) * math.cos(angulo)
    y1 = cy - (r-8) * math.sin(angulo)
    x2 = cx + r * math.cos(angulo)
    y2 = cy - r * math.sin(angulo)
    cv_dial.create_line(x1,y1,x2,y2, fill='#64748b', width=2)
    cv_dial.create_text(cx+(r+14)*math.cos(angulo), cy-(r+14)*math.sin(angulo),
        text=str(val), fill='#94a3b8', font=('Arial',7))
# Aguja (línea que rota)
aguja = cv_dial.create_line(cx,cy, cx+r*math.cos(math.radians(180)),
    cy, fill='#ef4444', width=3, capstyle=tk.ROUND)
lbl_temp_dial = tk.Label(frame_dial, text='-- °C', bg='#1e2736',
    fg='#ef4444', font=('Courier New',14,'bold'))
lbl_temp_dial.pack()

def set_temperatura(temp: float):
    """Rotar la aguja del dial — temp: 0..100°C"""
    temp = max(0, min(100, temp))
    angulo = math.radians(180 - (180 * temp / 100))
    xp = cx + r * math.cos(angulo)
    yp = cy - r * math.sin(angulo)
    cv_dial.coords(aguja, cx, cy, xp, yp)
    lbl_temp_dial.config(text=f'{temp:.1f} °C')

# ── D. Simulación dinámica ─────────────────────────────────────
temp_sim = 20.0
niv_sim  = 50.0
tick_alarma = False

def tick_simulacion():
    global temp_sim, niv_sim, tick_alarma
    temp_sim += random.uniform(-0.5, 0.8)
    temp_sim  = max(15, min(95, temp_sim))
    niv_sim  += random.uniform(-1.5, 1.5)
    niv_sim   = max(0, min(100, niv_sim))

    set_temperatura(temp_sim)
    set_nivel(niv_sim)

    # Actualizar LEDs
    led_conexion.set_color('verde')
    led_sensor.set_color('verde')
    alarma = temp_sim > 70
    if alarma:
        tick_alarma = not tick_alarma
        led_alarma.set_color('rojo' if tick_alarma else 'gris')  # parpadeo
    else:
        led_alarma.set_color('gris')
    led_log.set_color('verde')

    root.after(200, tick_simulacion)

# Botones de control de simulación
frame_btns = tk.Frame(root, bg='#1e2736')
frame_btns.grid(row=1, column=0, columnspan=3, pady=8)
tk.Button(frame_btns, text='Iniciar simulación', command=tick_simulacion,
    bg='#1E5E2E', fg='white', font=('Arial',10), relief=tk.FLAT, padx=12
).pack(side=tk.LEFT, padx=8)

root.mainloop()
