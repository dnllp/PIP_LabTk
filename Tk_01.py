# Lab Tk-1: Primera ventana con widgets esenciales
import tkinter as tk
from tkinter import messagebox

# ── 1. Crear la ventana principal (root) ─────────────────────
root = tk.Tk()
root.title('Lab Tk-1 — Practica inicial')
root.geometry('620x480')          # ancho x alto en píxeles
root.resizable(True, True)        # permitir redimensionar
root.configure(bg='#f0f4f8')      # color de fondo

# ── 2. Variables de Tkinter (StringVar, IntVar, BooleanVar) ──
# StringVar vincula una variable Python con un widget
var_nombre   = tk.StringVar()     # texto en el Entry
var_resultado = tk.StringVar(value='(aquí aparecerá el saludo)')

# ── 3. Widgets ────────────────────────────────────────────────
# Label: mostrar texto
lbl_titulo = tk.Label(
    root,
    text='Bienvenido a Tkinter',
    font=('Arial', 28, 'bold'),
    bg='#f0f4f8',
    fg="#f2920d"
)

# Label: instrucción
lbl_inst = tk.Label(root, text='¿Cómo te llamas?',
    bg='#f0f4f8', fg='#595959', font=('Arial', 11))

# Entry: campo de texto de una sola línea
entry_nombre = tk.Entry(
    root,
    textvariable=var_nombre,   # vinculado a StringVar
    font=('Arial', 12),
    width=28,
    relief=tk.FLAT,
    bg='white',
    highlightthickness=2,
    highlightcolor='#2E75B6'
)

# Label de resultado (actualizable)
lbl_resultado = tk.Label(
    root,
    textvariable=var_resultado,  # se actualiza automáticamente
    font=('Arial', 12, 'italic'),
    bg='#f0f4f8',
    fg='#1E5E2E'
)

# ── 4. Callbacks (funciones conectadas a botones) ─────────────
def saludar():
    nombre = var_nombre.get().strip()
    if not nombre:
        messagebox.showwarning('Campo vacío', 'Escribe tu nombre primero.')
        return
    var_resultado.set(f'¡Hola, {nombre}! Bienvenido al lab.')

def limpiar():
    var_nombre.set('')            # vaciar el Entry
    var_resultado.set('(aquí aparecerá el saludo)')
    entry_nombre.focus()          # devolver el foco al Entry

def confirmar_salida():
    if messagebox.askyesno('Salir', '¿Estás seguro que deseas salir?'):
        root.destroy()            # cerrar la ventana

# ── 5. Botones ────────────────────────────────────────────────
btn_saludar = tk.Button(
    root, text='Saludar', command=saludar,
    bg='#2E75B6', fg='white', font=('Arial', 11, 'bold'),
    relief=tk.FLAT, padx=16, pady=6, cursor='hand2'
)
btn_limpiar = tk.Button(
    root, text='Limpiar', command=limpiar,
    bg='#595959', fg='white', font=('Arial', 11),
    relief=tk.FLAT, padx=16, pady=6, cursor='hand2'
)
btn_salir = tk.Button(
    root, text='Salir', command=confirmar_salida,
    bg='#922B21', fg='white', font=('Arial', 11),
    relief=tk.FLAT, padx=16, pady=6, cursor='hand2'
)

# ── 6. Colocar widgets con pack() ─────────────────────────────
# pack() los pone uno abajo del otro por defecto
lbl_titulo.pack(pady=(20, 8))
lbl_inst.pack()
entry_nombre.pack(pady=8, ipady=4)
# Frame para los botones (para ponerlos en fila horizontal)
frame_btns = tk.Frame(root, bg='#f0f4f8')
frame_btns.pack(pady=10)
btn_saludar.pack(in_=frame_btns, side=tk.LEFT, padx=6)
btn_limpiar.pack(in_=frame_btns, side=tk.LEFT, padx=6)
btn_salir.pack(  in_=frame_btns, side=tk.LEFT, padx=6)
lbl_resultado.pack(pady=12)

# ── 7. Atajos de teclado ──────────────────────────────────────
root.bind('<Return>', lambda e: saludar())   # Enter = Saludar
root.bind('<Escape>', lambda e: confirmar_salida())
entry_nombre.focus()   # cursor en el Entry al abrir

# ── 8. Iniciar el event loop ──────────────────────────────────
root.mainloop()        # NUNCA poner código útil después de esto
