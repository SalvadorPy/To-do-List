import customtkinter as ctk
from tkinter import messagebox
import json
categorias={}
categoria_actual=None
def cargar_datos():
    global categorias
    try:
        with open("datos.json", "r") as archivo:
            categorias = json.load(archivo)
    except FileNotFoundError:
        categorias = {}
    except json.JSONDecodeError:
        categorias = {}
cargar_datos()



ctk.set_appearance_mode("dark")  # puedes cambiar a "light"
ctk.set_default_color_theme("blue")

ventCategorias = ctk.CTk()
ventCategorias.title("Categorías")
ventCategorias.geometry("800x600")






def guardar_datos():
    with open("datos.json", "w") as archivo:
        json.dump(categorias, archivo)

def mostrar_tareas():
    for widget in frmTareas.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frmTareas, text=categoria_actual, font=("Arial", 16)).pack(pady=10)

    entrada_tarea = ctk.CTkEntry(frmTareas)
    entrada_tarea.pack(pady=5)

    def agregar_tarea():
        tarea = entrada_tarea.get()

        if tarea == "":
            return

        categorias[categoria_actual].append({
        "texto": tarea,
        "completada": False
        })
        mostrar_tareas()

    ctk.CTkButton(frmTareas, text="Agregar tarea", command=agregar_tarea).pack(pady=5)
    # 🔽 Mostrar tareas
    for tarea in categorias[categoria_actual]:
        frame_tarea = ctk.CTkFrame(frmTareas,  fg_color="transparent")
        frame_tarea.pack(pady=2)

        texto = tarea["texto"]
        completada = tarea["completada"]

# Cambiar apariencia si está completada
        if completada:
            label = ctk.CTkLabel(frame_tarea, text=texto, fg_color="gray", font=("Arial", 10, "overstrike"))
        else:
            label = ctk.CTkLabel(frame_tarea, text=texto)

        label.pack(side="left")
        def completar(t=tarea):
            t["completada"] = not t["completada"]
            mostrar_tareas()

        ctk.CTkButton(frame_tarea, text="✔",width=5, height=10,     hover_color="#00DB24", command=completar).pack(side="right")

        # tk.Label(frame_tarea, text=tarea).pack(side="left")

        def eliminar(t=tarea):
            categorias[categoria_actual].remove(t)
            mostrar_tareas()

        ctk.CTkButton(frame_tarea, text="✗",width=5, height=10, hover_color="#FF1616",  command=eliminar).pack(side="right")

    

    ctk.CTkButton(
    frmTareas,
    text="Volver al inicio",
    command=volver
    ).pack(pady=10)
    
    guardar_datos()

#Para ir agregando categorias
def agregarCategoria():
    nombre=entrada_categoria.get()

    if nombre=="":
        return
    

    if nombre not in categorias:
        
        categorias[nombre] = []

        refrescar_categorias()  # 👈 SOLO esto



    # limpia la entrada
    entrada_categoria.delete(0, "end")
    guardar_datos()

# Para añadir nueva ventana
def abrir_categoria(nombre):
    print("Abriste:", nombre)
    global categoria_actual
    categoria_actual = nombre

    frmPrincipal.pack_forget()
    frmTareas.pack(fill="both", expand=True)
    mostrar_tareas()

    guardar_datos()
    

def eliminar_categoria(nombre):
    categorias.pop(nombre)
    refrescar_categorias()
    guardar_datos()
# olvidar ventana de la ctegoria abierta y regresar a la primera
def volver():
    frmTareas.pack_forget()
    frmPrincipal.pack(fill="both", expand=True)
    guardar_datos()

# frame principal
frmPrincipal = ctk.CTkFrame(ventCategorias, fg_color="transparent")
frmPrincipal.pack(fill="both", expand=True, padx=0, pady=0)

frmTareas=ctk.CTkFrame(ventCategorias, fg_color="transparent")

# Agregamos un boton y un texto a esta "ventana" que es un frame pero solo se muestra al hacer click 
# en el boton de la categoria, se cual sea.
titulo_tareas = ctk.CTkLabel(frmTareas, text="Tareas", font=("Arial", 16))
titulo_tareas.pack(pady=10)

# frame para las categorias:
frmCategorias=ctk.CTkFrame(frmPrincipal, fg_color="transparent")
frmCategorias.pack(pady=10)


# Frame para mostrar categorias.
frame_lista = ctk.CTkFrame(frmPrincipal, fg_color="transparent")
frame_lista.pack(pady=10)

# poner el boton de cada categoria:
def refrescar_categorias():
    for widget in frame_lista.winfo_children():
        widget.destroy()

    for nombre in categorias:
        fila = ctk.CTkFrame(frame_lista)
        fila.pack(pady=5, fill="x")

        boton = ctk.CTkButton(
            fila,
            text=nombre,
            width=40,
            anchor="w",
            command=lambda n=nombre: abrir_categoria(n)
        )
        boton.pack(side="right")
        botonDelete = ctk.CTkButton(
            fila,
            text="x",
            fg_color="red",
            width=8,
            height=7,
            command=lambda n=nombre: eliminar_categoria(n)
        )
        botonDelete.pack(side="left")


refrescar_categorias()
# Título
titulo = ctk.CTkLabel(
    frmPrincipal,
    text="📂 Mis Categorías",
    font=("Arial", 16)
)
titulo.pack(pady=10)

frmAgregar = ctk.CTkFrame(frmPrincipal)
frmAgregar.pack(pady=10)

entrada_categoria = ctk.CTkEntry(frmAgregar)
entrada_categoria.pack(side="left", padx=5)

boton_agregar = ctk.CTkButton(frmAgregar, text="Agregar", command=agregarCategoria)
boton_agregar.pack(side="left")

refrescar_categorias()
ventCategorias.mainloop()