#!/usr/bin/python3
#Author: Javier Saez Cerezo
#Fecha de inicio de Desarrollo 2 oct 2023

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *


# Funciones

def select_all_inside(event):
	event.widget.select_range(0, 'end')
	
def add_imput(event):
    try:
        medY = medYvar.get()
        medX = medXvar.get()
        desfase = desfasevar.get()
        data = [medY, medX, desfase]
    except:
   	    messagebox.showerror("Error", "Todos los valores introducidos deben ser numeros enteros o decimales separados por un punto")
    insert_data_treeview(data)


def next_widget(event):
      event.widget.tk_focusNext().focus()
    
def insert_data_treeview(data):
    selected_item = treeview.selection()
    if selected_item:
        valores_actuales = treeview.item(selected_item, 'values')
        nuevos_valores = data
        treeview.item(selected_item, values=nuevos_valores)
        return medY.focus_set()
    else:    
        treeview.insert('', 0 , text="", values=data)
        return medY.focus_set()

def borrar_campos():
    records = treeview.get_children()
    for i in records:
        treeview.delete(i)

def imprimir_archivo():
    data = treeview.get_children()
    details = []
    values = []
    for d in data:
        details.append(treeview.item(d))
    for i in details:
        values.append(i.get('values')[:])     
    constructor_script(values)

def borrar_linea():
    details = treeview.selection()
    if details:
        treeview.delete(details)
    else:
        messagebox.showinfo("Aviso", "Seleccione una linea")
        

def insert_data(event):
    details = treeview.focus()
    record = treeview.item(details)
    data = record.get("values")[:]
    if len(data) != 0:
        medY.delete(0, 'end')
        medY.insert(0, data[0])
        medX.delete(0, 'end')
        medX.insert(0, data[1])
        desfase.delete(0, 'end')
        desfase.insert(0, data[2])            

def deseleccionar_con_escape(event):
    if event.keysym == 'Escape':
        treeview.selection_remove(treeview.selection())    



def constructor_script(values):
    file = open("Auto_Trape.scr", "w")
    origeny = 0
    origenx = 0
    contador = 1
    for value in values:
        ver = float(value[0])
        hor = float(value[1])
        des = float(value[2])
        cor1 = f"{round(origenx, 1)},{round(origeny+ver, 1)}"
        cor2 = f"{round(origenx+hor, 1)},{round(origeny+ver+ver-des, 1)}"
        cor3 = f"{round(origenx+hor,1)},{round(origeny+ver-des, 1)}"
        
        file.write(f"""linea {origenx},{origeny} {cor1} {cor2} {cor3} {origenx},{origeny} 
acoalineada {cor1} per {origenx},{origeny} {cor1} 
acoalineada {origenx},{origeny} {cor3} {round(origenx+10, 1)},{round(origeny-10, 1)} acocontinua {cor2} 
 acoalineada {origenx},{origeny} per {cor2} {round(origenx+20, 1)},{round(origeny-20, 1)} 
""")
        if contador == 4:
            origenx = round(origenx+hor+100, 1)
            origeny = 0
            contador = 1
    
        else:
            origenx = origenx
            origeny = round(origeny+ver+60, 1)
            contador = contador+1
    file.close()
    return messagebox.showinfo("Info", "Archivo creado, introduzca 'SCR' en Autocad para cargar el archivo")




# Inicio de Programa #######################################################################################################################

root = ttk.Window(themename="solar")
root.title('AutoTrap')
menu = ttk.Menu(root)
mnu_Archivo = ttk.Menu(root, tearoff=0)
mnu_Archivo.add_command(label=" Salir ", command=root.quit)
menu.add_cascade(label=" Archivo ", menu=mnu_Archivo)
root.config(menu=menu) 


# Frame Principal
frame1 = ttk.Frame(root)
frame1.pack(side='left', anchor='n', fill="both", expand=1)

#Labels
ttk.Label(frame1, text="Medida Y", justify="center").grid(row=0, column=0, padx=50, pady=20)
ttk.Label(frame1, text="Medida X", justify="center").grid(row=0, column=1, padx=50, pady=20)
ttk.Label(frame1, text="Desfase", justify="center").grid(row=0, column=2, padx=50, pady=20)

# Entrys y variables de entrada
medYvar = tk.DoubleVar()
medY = ttk.Entry(frame1, justify="center", textvariable=medYvar)
medY.grid(row=1, column=0)
medY.bind("<FocusIn>", select_all_inside)


medXvar = tk.DoubleVar()
medX = ttk.Entry(frame1, justify="center", textvariable=medXvar)
medX.grid(row=1, column=1)
medX.bind("<FocusIn>", select_all_inside)

desfasevar = tk.DoubleVar()
desfase = ttk.Entry(frame1, justify="center", textvariable=desfasevar)
desfase.grid(row=1, column=2)
desfase.bind("<FocusIn>", select_all_inside)
desfase.bind("<Return>", add_imput)



# Imagen del Romboide de Ejemplo
image1 = Image.open("Romboide.png")
image_resized = image1.resize((600, 400), Image.ANTIALIAS)
test = ImageTk.PhotoImage(image_resized)
label1 = tk.Label(frame1, image=test)
label1.grid(row=2, column=0, columnspan=3)

# Treeview
treeview = ttk.Treeview(frame1, height=15, columns=("#1","#2","#3"), show='headings', selectmode=tk.BROWSE, bootstyle='info')
treeview.heading('#0', text = 'ID', anchor ='center')
treeview.heading('#1', text = 'Medida Y', anchor ='center')
treeview.column('#1', anchor='center', stretch='yes')
treeview.heading('#2', text = 'Medida X', anchor = 'center')
treeview.column('#2', anchor='center', stretch='yes')
treeview.heading('#3', text = 'Desfase', anchor = 'center')
treeview.column('#3', anchor='center', stretch='yes')
treeview.grid(row=3, column=0, columnspan=3)
treeview.bind("<<TreeviewSelect>>", insert_data)
treeview.bind("<Escape>", deseleccionar_con_escape)

# Scrollbar del treeview
scrollbar_y = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=treeview.yview)
scrollbar_y.grid(row=3, column=4, sticky="ns")
treeview.configure(yscroll=scrollbar_y.set)

# Botones
imprimir = ttk.Button(frame1, text="Imprimir", bootstyle='info', command=imprimir_archivo)
imprimir.grid(row=4, column=0)

borrar_linea = ttk.Button(frame1, text="Borrar linea", bootstyle='info', command=borrar_linea)
borrar_linea.grid(row=4, column=1)

borrar_lista = ttk.Button(frame1, text="Limpiar lista", bootstyle='info', command=borrar_campos)
borrar_lista.grid(row=4, column=2)



# Binds
medY.focus_set()
medY.bind('<Return>', next_widget)
medX.bind('<Return>', next_widget)


root.mainloop()