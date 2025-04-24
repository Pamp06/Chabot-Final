import tkinter as tk
from tkinter import *
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import ttkbootstrap as tb
import sqlite3
import train as entrenar
import threading
import time
import os
import subprocess
import webbrowser
import ctypes
from datetime import datetime

class Ventana(tb.Window):
    def __init__(self):
        super().__init__()
        self.set_icon()
        self.nombre_usuario=None
            
        # Conexion SQLite
        self.DB_PATH = 'chatbotf.db'
        self.ventana_login()
        
    def set_icon(self):
        ruta_icono = os.path.join("static", "images", "Admin.ico")

        # Establece el ícono en la ventana de Tkinter
        if os.path.exists(ruta_icono):
            self.iconbitmap(ruta_icono)
            
            if os.name == "nt":
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("tu.aplicacion.id")
                self.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el archivo de ícono en {ruta_icono}")
            
    # Funcion para centrar las ventanas
    def centrar_ventana(self):
        self.update_idletasks()

        ancho_ventana = self.winfo_width()
        alto_ventana = self.winfo_height()

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho_ventana // 2)
        y = (pantalla_alto // 2) - (alto_ventana // 2)

        self.geometry(f"+{x}+{y}")
        
    def resaltar_boton(self, nombre_boton):
        botones = {
            "btn_usuarios": self.btn_usuarios,
            "btn_intent": self.btn_intent,
            "btn_patterns": self.btn_patterns,
            "btn_responses": self.btn_responses,
            "btn_buttons": self.btn_buttons,
            "btn_movimientos": self.btn_movimientos,
            "btn_reco": self.btn_reco
        }
        
        for boton in botones.values():
            boton.config(bootstyle="primary")
        
        if nombre_boton in botones:
            botones[nombre_boton].config(bootstyle="secondary")
            
    # Ventana login
    def ventana_login(self):
        self.geometry("300x280")
        self.grid_columnconfigure(1, weight=1)
        self.resizable(False, False)

        self.frame_login = Frame(master=self)
        self.frame_login.grid(row=0, column=1, sticky=NSEW)

        lblframe_login = tb.LabelFrame(master=self.frame_login, text="Acceso")
        lblframe_login.pack(padx=10, pady=20)

        lbl_titulo = tb.Label(master=lblframe_login, text="Iniciar Sesión", font=("Calibri", 20))
        lbl_titulo.pack(padx=10, pady=15)

        self.ent_usuario = tb.Entry(master=lblframe_login, width=40, justify=CENTER)
        self.ent_usuario.pack(padx=10, pady=10)
        self.ent_clave = tb.Entry(master=lblframe_login, width=40, justify=CENTER)
        self.ent_clave.pack(padx=10, pady=10)
        self.ent_clave.config(show="*")
        btn_entrar = tb.Button(master=lblframe_login, width=38, text="Iniciar Sesión", bootstyle="primary", command=self.logueo_usuarios)
        btn_entrar.pack(padx=10, pady=10)
        self.bind('<Return>', lambda event: self.logueo_usuarios())

        self.centrar_ventana()
        
    def ventana_menu(self):
        self.geometry("545x540")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.frame_left = Frame(master=self, width=200)
        self.frame_left.grid(row=0, column=0, sticky="ns")

        self.frame_center = Frame(master=self)
        self.frame_center.grid(row=0, column=1, sticky="nsew")

        self.imagen = PhotoImage(file=r"src\img\IUTEPAL1.png") # Ruta de la imagen del menu

        lbl_imagen = Label(master=self.frame_center, image=self.imagen)
        lbl_imagen.grid(row=0, column=0, padx=10, pady=10)

        self.btn_usuarios = tb.Button(master=self.frame_left, text="Usuarios", width=15, bootstyle="primary", command=self.ventana_lista_usuarios)
        self.btn_usuarios.grid(row=0, column=0, padx=10, pady=10)

        self.btn_intent = tb.Button(master=self.frame_left, text="Intenciones", width=15, bootstyle="primary", command=self.ventana_lista_intents)
        self.btn_intent.grid(row=1, column=0, padx=10, pady=10)

        self.btn_patterns = tb.Button(master=self.frame_left, text="Patrones", width=15, bootstyle="primary", command=self.ventana_lista_patterns)
        self.btn_patterns.grid(row=2, column=0, padx=10, pady=10)

        self.btn_responses = tb.Button(master=self.frame_left, text="Respuestas", width=15, bootstyle="primary", command=self.ventana_lista_responses)
        self.btn_responses.grid(row=3, column=0, padx=10, pady=10)

        self.btn_buttons = tb.Button(master=self.frame_left, text="Botones", width=15, bootstyle="primary", command=self.ventana_lista_buttons)
        self.btn_buttons.grid(row=4, column=0, padx=10, pady=10)

        self.btn_movimientos = tb.Button(master=self.frame_left, text="Movimientos", width=15, bootstyle="primary", command=self.ventana_lista_movimientos)
        self.btn_movimientos.grid(row=5, column=0, padx=10, pady=10)

        self.btn_reco = tb.Button(master=self.frame_left, text="Recomendaciones", width=16, bootstyle="primary", command=self.ventana_lista_reco)
        self.btn_reco.grid(row=6, column=0, padx=10, pady=10)
        
        btn_intent = tb.Button(master=self.frame_left, text="Entrenar", width=15, bootstyle="warning", command=self.entrenar_bot)
        btn_intent.grid(row=7, column=0, padx=10, pady=10)
        
        btn_ejecutar_bot = tb.Button(master=self.frame_left, text="Ejecutar Bot", width=15, bootstyle="success", command=self.ejecutar_bot)
        btn_ejecutar_bot.grid(row=8, column=0, padx=10, pady=10)
        
        self.centrar_ventana()
        self.crear_footer()
        
    def crear_footer(self):
        self.footer = tb.Frame(master=self, bootstyle="light")
        self.footer.grid(row=1, column=0, columnspan=2, sticky="ew", pady=0)
        
        ruta_imagen = os.path.join("src", "img", "FOOT.png")  # Ruta de la imagen
        if os.path.exists(ruta_imagen):
            self.imagen_institucion = tk.PhotoImage(file=ruta_imagen)
            self.lbl_imagen = tb.Label(master=self.footer, image=self.imagen_institucion)
            self.lbl_imagen.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        else:
            print(f"Advertencia: No se encontró el archivo de imagen en {ruta_imagen}")
            
        self.menu_usuario = Menu(self.footer, tearoff=0)
        self.menu_usuario.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        
        self.btn_usuario = tb.Menubutton(master=self.footer, text="Usuario", width=13, bootstyle="primary")
        self.btn_usuario.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.btn_usuario["menu"] = self.menu_usuario
        
    def actualizar_nombre_usuario(self, nombre_usuario):
        self.btn_usuario.config(text=nombre_usuario)
        self.nombre_usuario=nombre_usuario

    # Cerrar sesion apartado
    def cerrar_sesion(self):
        self.footer.destroy()
        self.frame_left.destroy()
        self.frame_center.destroy()
        
        self.ventana_login()
        self.bind('<Return>', lambda event: self.logueo_usuarios())
        
    # Usuarios apartado
    def ventana_lista_usuarios(self):
        self.geometry("725x540")
        self.resaltar_boton("btn_usuarios")
        self.frame_lista_usuarios = tb.Frame(master=self)
        self.frame_lista_usuarios.grid(row=0, column=1, columnspan=2, sticky=NSEW)
        
        lblframe_botones_lista_usuarios = tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_botones_lista_usuarios.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        btn_nuevo_lista_usuarios = tb.Button(master=lblframe_botones_lista_usuarios, text="Nuevo", width=15, bootstyle="success", command=self.ventana_nuevo_usuario)
        btn_nuevo_lista_usuarios.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_lista_usuarios = tb.Button(master=lblframe_botones_lista_usuarios, text="Modificar", width=15, bootstyle="secondary", command=self.ventana_modificar_usuario)
        btn_modificar_lista_usuarios.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_lista_usuarios = tb.Button(master=lblframe_botones_lista_usuarios, text="Eliminar", width=15, bootstyle="danger", command=self.eliminar_usuario)
        btn_eliminar_lista_usuarios.grid(row=0, column=2, padx=10, pady=10)

        lblframe_busqueda_lista_usuarios = tb.LabelFrame(master=self.frame_lista_usuarios, text="Filtro de Datos")
        lblframe_busqueda_lista_usuarios.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        
        self.ent_buscar_lista_usuario = tb.Entry(master=lblframe_busqueda_lista_usuarios, width=90)
        self.ent_buscar_lista_usuario.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_usuario.bind('<Key>', self.buscar_usuarios)
        
        lblframe_tree_lista_usuarios = tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_tree_lista_usuarios.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Código", "Usuario", "Clave", "Rol","last_login")

        # Tabla
        self.tree_lista_usuarios = tb.Treeview(master=lblframe_tree_lista_usuarios, height=17, columns=columnas, show='headings', bootstyle='info')
        self.tree_lista_usuarios.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        
        lblframe_tree_lista_usuarios.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_usuarios.grid_rowconfigure(0, weight=1)

        # Encabezados
        self.tree_lista_usuarios.heading('Código', text='Código', anchor=W)
        self.tree_lista_usuarios.heading('Usuario', text='Usuario', anchor=W)
        self.tree_lista_usuarios.heading('Clave', text='Clave', anchor=W)
        self.tree_lista_usuarios.heading('Rol', text='Rol', anchor=W)
        self.tree_lista_usuarios.heading('last_login',text='Ultimo inicio de sesión', anchor=W)
        
        self.tree_lista_usuarios['displaycolumns'] = ('Usuario', 'Rol','last_login')
        
        # Tamaño columnas
        self.tree_lista_usuarios.column("Código", width=0)
        self.tree_lista_usuarios.column("Usuario", width=100)
        self.tree_lista_usuarios.column("Clave", width=0)
        self.tree_lista_usuarios.column("Rol", width=150)
        self.tree_lista_usuarios.column("last_login",width=100)
        
        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_usuarios, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)
        tree_scroll.config(command=self.tree_lista_usuarios.yview)
        
        self.buscar_usuarios('')
        self.centrar_ventana()
        
    def buscar_usuarios(self, event):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        registro = self.tree_lista_usuarios.get_children()
        for elementos in registro:
            self.tree_lista_usuarios.delete(elementos)

        cursor.execute("SELECT * FROM usuarios WHERE nombre LIKE ?", (self.ent_buscar_lista_usuario.get() + '%',))
        datos_usuarios = cursor.fetchall()
        
        for fila in datos_usuarios:
            self.tree_lista_usuarios.insert('', 0, fila[0], values=(fila[0], fila[1], fila[2], fila[3],fila[4]))

        conn.commit()
        cursor.close()
        conn.close()

    def logueo_usuarios(self):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            con_usuario = self.ent_usuario.get()
            con_clave = self.ent_clave.get()

            cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND clave=?", (con_usuario, con_clave))
            datos_log = cursor.fetchall()

            if datos_log:
                for fila in datos_log:
                    nombre_usuario_logueado = fila[1]
                    clave_usuario_logueado = fila[2]
                if nombre_usuario_logueado == self.ent_usuario.get() and clave_usuario_logueado == self.ent_clave.get():
                    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute("UPDATE usuarios SET last_login = ? WHERE nombre = ?", (fecha_actual, con_usuario))
                    self.unbind('<Return>')

                    self.ventana_menu()
                    self.frame_login.destroy()

                    self.actualizar_nombre_usuario(nombre_usuario_logueado)
                else:
                    messagebox.showwarning('Logueo', 'Usuario o Contraseña ingresada son incorrectos')
            else:
                messagebox.showwarning('Logueo', 'Usuario o Contraseña ingresada son incorrectos')

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showwarning('Logueo', f'Error al conectar con la base de datos: {str(e)}')

    def ventana_nuevo_usuario(self):
        self.frame_nuevo_usuario = Toplevel(master=self)
        self.frame_nuevo_usuario.title("Nuevo Usuario")
        self.frame_nuevo_usuario.resizable(False, False)
        self.centrar_vetana_new(400,250)
        self.frame_nuevo_usuario.grab_set()
        
        ruta_icono = os.path.join("static", "images", "Admin.ico")
        if os.path.exists(ruta_icono):
            self.frame_nuevo_usuario.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

        lblframe_nuevo_usuario = tb.LabelFrame(master=self.frame_nuevo_usuario, text="Nuevo Usuario")
        lblframe_nuevo_usuario.pack(padx=15, pady=15)
        
        lbl_nombre_nuevo_usuario = Label(master=lblframe_nuevo_usuario, text='Nombre')
        lbl_nombre_nuevo_usuario.grid(row=1, column=0, padx=10, pady=10)
        self.ent_nombre_nuevo_usuario = tb.Entry(master=lblframe_nuevo_usuario, width=40)
        self.ent_nombre_nuevo_usuario.grid(row=1, column=1, padx=10, pady=10)

        lbl_clave_nuevo_usuario = Label(master=lblframe_nuevo_usuario, text='Clave')
        lbl_clave_nuevo_usuario.grid(row=2, column=0, padx=10, pady=10)
        self.ent_clave_nuevo_usuario = tb.Entry(master=lblframe_nuevo_usuario, width=40)
        self.ent_clave_nuevo_usuario.grid(row=2, column=1, padx=10, pady=10)
        self.ent_clave_nuevo_usuario.config(show='*')

        lbl_rol_nuevo_usuario = Label(master=lblframe_nuevo_usuario, text='Rol')
        lbl_rol_nuevo_usuario.grid(row=3, column=0, padx=10, pady=10)
        self.cbo_rol_nuevo_usuario = tb.Combobox(master=lblframe_nuevo_usuario, width=38, values=['Administrador'])
        self.cbo_rol_nuevo_usuario.grid(row=3, column=1, padx=10, pady=10)
        self.cbo_rol_nuevo_usuario.current(0)
        self.cbo_rol_nuevo_usuario.config(state='readonly')

        btn_Guardar_nuevo_usuario = Button(master=lblframe_nuevo_usuario, text='Guardar', width=36, command=self.guardar_usuario)
        btn_Guardar_nuevo_usuario.grid(row=4, column=1, padx=10, pady=10)
        
        self.ent_nombre_nuevo_usuario.focus_set()
        self.frame_nuevo_usuario.bind('<Return>', lambda event: self.guardar_usuario())

    def guardar_usuario(self):
        if self.ent_nombre_nuevo_usuario.get() == '' or self.ent_clave_nuevo_usuario.get() == '' or self.cbo_rol_nuevo_usuario.get() == '':
            messagebox.showerror('Guardando Usuarios', 'Los campos a llenar no pueden estar vacíos')
            return
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            # Verificar si el usuario ya existe
            cursor.execute("SELECT nombre FROM usuarios WHERE nombre = ?", (self.ent_nombre_nuevo_usuario.get(),))
            if cursor.fetchone():
                messagebox.showerror('Error', 'El nombre de usuario ya existe')
                return

            guardar_datos_usuarios = (str(self.ent_nombre_nuevo_usuario.get()), 
                                    str(self.ent_clave_nuevo_usuario.get()), 
                                    str(self.cbo_rol_nuevo_usuario.get()))

            cursor.execute("INSERT INTO usuarios (nombre, clave, rol) VALUES (?, ?, ?)", guardar_datos_usuarios)

            conn.commit()
            messagebox.showinfo('Guardando Usuario', 'Usuario Agregado Exitosamente')
            self.frame_nuevo_usuario.destroy()
            self.buscar_usuarios('')
        except Exception as e:
            messagebox.showerror('Guardando Usuarios', f'Ocurrió un Error Inesperado: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()

    def ventana_modificar_usuario(self):
        self.usuario_seleccionado = self.tree_lista_usuarios.focus()
        self.valor_usuario_seleccionado = self.tree_lista_usuarios.item(self.usuario_seleccionado, 'values')

        if self.valor_usuario_seleccionado != '':
            self.frame_modificar_usuario = Toplevel(master=self)
            self.frame_modificar_usuario.title("Modificar Usuario")
            self.frame_modificar_usuario.resizable(False, False)
            self.centrar_vetana_mod(400,250)
            self.frame_modificar_usuario.grab_set()
            
            ruta_icono = os.path.join("static", "images", "Admin.ico")
            if os.path.exists(ruta_icono):
                self.frame_modificar_usuario.iconbitmap(ruta_icono)
            else:
                print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

            lblframe_modificar_usuario = tb.LabelFrame(master=self.frame_modificar_usuario, text="Editar Usuario")
            lblframe_modificar_usuario.pack(padx=15, pady=15)
            
            lbl_codigo_modificar_usuario = Label(master=lblframe_modificar_usuario, text='Codigo')
            lbl_codigo_modificar_usuario.grid(row=0, column=0, padx=10, pady=10)
            self.ent_codigo_modificar_usuario = tb.Entry(master=lblframe_modificar_usuario, width=40)
            self.ent_codigo_modificar_usuario.grid(row=0, column=1, padx=10, pady=10)
            lbl_codigo_modificar_usuario.grid_forget()
            self.ent_codigo_modificar_usuario.grid_forget()

            lbl_nombre_modificar_usuario = Label(master=lblframe_modificar_usuario, text='Nombre')
            lbl_nombre_modificar_usuario.grid(row=1, column=0, padx=10, pady=10)
            self.ent_nombre_modificar_usuario = tb.Entry(master=lblframe_modificar_usuario, width=40)
            self.ent_nombre_modificar_usuario.grid(row=1, column=1, padx=10, pady=10)

            lbl_clave_modificar_usuario = Label(master=lblframe_modificar_usuario, text='Clave')
            lbl_clave_modificar_usuario.grid(row=2, column=0, padx=10, pady=10)
            self.ent_clave_modificar_usuario = tb.Entry(master=lblframe_modificar_usuario, width=40)
            self.ent_clave_modificar_usuario.grid(row=2, column=1, padx=10, pady=10)
            self.ent_clave_modificar_usuario.config(show='*')

            lbl_rol_modificar_usuario = Label(master=lblframe_modificar_usuario, text='Rol')
            lbl_rol_modificar_usuario.grid(row=3, column=0, padx=10, pady=10)
            self.cbo_rol_modificar_usuario = tb.Combobox(master=lblframe_modificar_usuario, width=38, values=['Administrador'])
            self.cbo_rol_modificar_usuario.grid(row=3, column=1, padx=10, pady=10)
            self.cbo_rol_modificar_usuario.config(state='readonly')

            btn_modificar_usuario = tb.Button(master=lblframe_modificar_usuario, text='Guardar', width=36, command=self.modificar_usuario)
            btn_modificar_usuario.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entry_modificar_usuarios()
            
            self.ent_nombre_modificar_usuario.focus_set()
            self.frame_modificar_usuario.bind('<Return>', lambda event: self.modificar_usuario())
        else:
            messagebox.showwarning('Modificar Usuario', 'Ningun Usuario Seleccionado')

    def llenar_entry_modificar_usuarios(self):
        self.ent_codigo_modificar_usuario.delete(0, END)
        self.ent_nombre_modificar_usuario.delete(0, END)
        self.ent_clave_modificar_usuario.delete(0, END)
        self.cbo_rol_modificar_usuario.delete(0, END)

        self.ent_codigo_modificar_usuario.insert(0, self.valor_usuario_seleccionado[0])
        self.ent_codigo_modificar_usuario.config(state='readonly')
        self.ent_nombre_modificar_usuario.insert(0, self.valor_usuario_seleccionado[1])
        self.ent_clave_modificar_usuario.insert(0, self.valor_usuario_seleccionado[2])
        self.cbo_rol_modificar_usuario.insert(0, self.valor_usuario_seleccionado[3])
        self.cbo_rol_modificar_usuario.config(state='readonly')

    def modificar_usuario(self):
        if (self.ent_codigo_modificar_usuario.get() == '' or 
            self.ent_nombre_modificar_usuario.get() == '' or 
            self.ent_clave_modificar_usuario.get() == '' or 
            self.cbo_rol_modificar_usuario.get() == ''):
            messagebox.showerror('Modificando Usuarios', 'Los campos a llenar no pueden estar vacios')
            return
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            modificar_datos_usuarios = (self.ent_nombre_modificar_usuario.get(), self.ent_clave_modificar_usuario.get(), self.cbo_rol_modificar_usuario.get(), self.ent_codigo_modificar_usuario.get())
            cursor.execute("UPDATE usuarios SET nombre=?, clave=?, rol=? WHERE codigo=?", modificar_datos_usuarios)

            conn.commit()

            messagebox.showinfo('Modificar Usuario', 'Usuario Modificado Exitosamente')
            self.valor_usuario_seleccionado = self.tree_lista_usuarios.item(self.usuario_seleccionado, text='', values=(int(self.ent_codigo_modificar_usuario.get()), str(self.ent_nombre_modificar_usuario.get()), str(self.ent_clave_modificar_usuario.get()), str(self.cbo_rol_modificar_usuario.get())))

            self.frame_modificar_usuario.destroy()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Modificando Usuarios', f'Ocurrió un Error Inesperado al Modificar: {str(e)}')

    def eliminar_usuario(self):
        usuario_seleccionado_eliminar = self.tree_lista_usuarios.focus()
        valor_usuario_selecionado_eliminar = self.tree_lista_usuarios.item(usuario_seleccionado_eliminar, 'values')

        if not valor_usuario_selecionado_eliminar:
            messagebox.showerror('Error', 'Ningún usuario seleccionado')
            return

        usuario_a_borrar = valor_usuario_selecionado_eliminar[1]
        usuario_logueado = self.nombre_usuario

        if usuario_a_borrar == usuario_logueado:
            messagebox.showerror('Error', 'No puedes eliminar tu propio usuario mientras estás logueado')
            return

        respuesta = messagebox.askquestion('Eliminando usuario', '¿Está seguro de eliminar el usuario seleccionado?')
        if respuesta == 'yes':
            try:
                conn = sqlite3.connect(self.DB_PATH)
                cursor = conn.cursor()
                fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Tipo = "Eliminar"
                Tabla = "Usuarios"
                datos = (Tipo, Tabla, usuario_a_borrar, fecha_actual, usuario_logueado)
                cursor.execute("INSERT INTO datos_eliminados(Tipo,Tabla,Nombre,Fecha,Usuario) VALUES (?,?,?,?,?)", datos)
                cursor.execute("DELETE FROM usuarios WHERE codigo=?", (valor_usuario_selecionado_eliminar[0],))
                conn.commit()
                messagebox.showinfo('Éxito', 'Usuario eliminado correctamente')
                self.buscar_usuarios('')
            except Exception as e:
                messagebox.showerror('Error', f'Ocurrió un error al eliminar: {str(e)}')
            finally:
                if 'conn' in locals():
                    conn.close()

    def centrar_vetana_new(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_nuevo_usuario.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def centrar_vetana_mod(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_modificar_usuario.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

# Intenciones apartado
    def ventana_lista_intents(self):
        self.geometry("725x540")
        self.resaltar_boton("btn_intent")
        self.frame_lista_intents = tb.Frame(master=self)
        self.frame_lista_intents.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        lblframe_botones_lista_intents = tb.LabelFrame(master=self.frame_lista_intents)
        lblframe_botones_lista_intents.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        btn_nuevo_lista_intents = tb.Button(master=lblframe_botones_lista_intents, text="Nuevo", width=15, bootstyle="success", command=self.ventana_nueva_intencion)
        btn_nuevo_lista_intents.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_lista_intents = tb.Button(master=lblframe_botones_lista_intents, text="Modificar", width=15, bootstyle="secondary", command=self.ventana_modificar_intencion)
        btn_modificar_lista_intents.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_lista_intents = tb.Button(master=lblframe_botones_lista_intents, text="Eliminar", width=15, bootstyle="danger", command=self.eliminar_intents)
        btn_eliminar_lista_intents.grid(row=0, column=2, padx=10, pady=10)

        lblframe_busqueda_lista_intents = tb.LabelFrame(master=self.frame_lista_intents, text="Filtro de Datos")
        lblframe_busqueda_lista_intents.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.ent_buscar_lista_intents = tb.Entry(master=lblframe_busqueda_lista_intents, width=90)
        self.ent_buscar_lista_intents.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_intents.bind('<Key>', self.buscar_intents)

        lblframe_tree_lista_intents = tb.LabelFrame(master=self.frame_lista_intents)
        lblframe_tree_lista_intents.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Id", "Tag", "creacion","usuario")

        # Tabla
        self.tree_lista_intents = tb.Treeview(master=lblframe_tree_lista_intents, height=17, columns=columnas, show='headings', bootstyle='info')
        self.tree_lista_intents.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        lblframe_tree_lista_intents.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_intents.grid_rowconfigure(0, weight=1)

        # Encabezados
        self.tree_lista_intents.heading('Id', text='Codigo', anchor=W)
        self.tree_lista_intents.heading('Tag', text='Nombre de la intencion', anchor=W)
        self.tree_lista_intents.heading('creacion', text='fecha de Creacion', anchor=W)
        self.tree_lista_intents.heading('usuario', text='Usuario', anchor=W)

        self.tree_lista_intents['displaycolumns'] = ('Tag', 'creacion','usuario')

        # Tamaño columnas
        self.tree_lista_intents.column("Id", width=100)
        self.tree_lista_intents.column("Tag", width=200)
        self.tree_lista_intents.column("creacion", width=150)
        self.tree_lista_intents.column("usuario", width=100)

        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_intents, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)

        tree_scroll.config(command=self.tree_lista_intents.yview)
        self.buscar_intents('')
        self.centrar_ventana()

    def buscar_intents(self, event):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        registro = self.tree_lista_intents.get_children()
        for elementos in registro:
            self.tree_lista_intents.delete(elementos)

        cursor.execute("SELECT * FROM Intents WHERE Tag LIKE ?", (self.ent_buscar_lista_intents.get() + '%',))
        datos_intents = cursor.fetchall()
        
        for fila in datos_intents:
            self.tree_lista_intents.insert('', 0, fila[0], values=(fila[0], fila[1], fila[2],fila[3]))

        conn.commit()
        cursor.close()
        conn.close()

    def ventana_nueva_intencion(self):
        self.frame_nuevo_intents = Toplevel(master=self)
        self.frame_nuevo_intents.title("Nueva Intencion")
        self.centrar_new_int(400,150)
        self.frame_nuevo_intents.resizable(False, False)
        self.frame_nuevo_intents.grab_set()
        
        ruta_icono = os.path.join("static", "images", "Admin.ico")
        if os.path.exists(ruta_icono):
            self.frame_nuevo_intents.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

        lblframe_nuevo_intents = tb.LabelFrame(master=self.frame_nuevo_intents, text="Nueva Intención")
        lblframe_nuevo_intents.pack(padx=15, pady=15)

        lbl_nombre_nuevo_intents = Label(master=lblframe_nuevo_intents, text='Intencion')
        lbl_nombre_nuevo_intents.grid(row=1, column=0, padx=10, pady=10)
        self.ent_nombre_nuevo_intents = tb.Entry(master=lblframe_nuevo_intents, width=40)
        self.ent_nombre_nuevo_intents.grid(row=1, column=1, padx=10, pady=10)

        btn_Guardar_nuevo_intents = Button(master=lblframe_nuevo_intents, text='Guardar', width=36, command=self.guardar_intents)
        btn_Guardar_nuevo_intents.grid(row=4, column=1, padx=10, pady=10)
        
        self.ent_nombre_nuevo_intents.focus_set()
        self.frame_nuevo_intents.bind('<Return>', lambda event: self.guardar_intents())

    def guardar_intents(self):
        if self.ent_nombre_nuevo_intents.get() == '':
            messagebox.showerror('Guardando Intención', 'Los campos a llenar no pueden estar vacios')
            return
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            intent_name = self.ent_nombre_nuevo_intents.get().strip().lower()
            cursor.execute("SELECT Tag FROM Intents WHERE LOWER(Tag) = ?", (intent_name,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Esta intención ya existe')
                return
                    
            nombre_usuario = self.nombre_usuario
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            guardar_datos_intents = (str(self.ent_nombre_nuevo_intents.get()), fecha_actual, nombre_usuario)
            
            cursor.execute("INSERT INTO Intents (Tag, creacion, usuario) VALUES (?, ?, ?)", guardar_datos_intents)

            conn.commit()
            messagebox.showinfo('Guardando Intencion', 'Intención Agregada Exitosamente')
            self.frame_nuevo_intents.destroy()
            self.buscar_intents('')
        except Exception as e:
            messagebox.showerror('Guardando Intención', f'Ocurrió un Error Inesperado: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()

    def ventana_modificar_intencion(self):
        self.intencion_seleccionado = self.tree_lista_intents.focus()
        self.valor_intencion_seleccionado = self.tree_lista_intents.item(self.intencion_seleccionado, 'values')

        if self.valor_intencion_seleccionado != '':
            self.frame_modificar_intents = Toplevel(master=self)
            self.frame_modificar_intents.title("Modificar Intención")
            self.frame_modificar_intents.resizable(False, False)
            self.centrar_mod_int(400,150)
            self.frame_modificar_intents.grab_set()
            
            ruta_icono = os.path.join("static", "images", "Admin.ico")
            if os.path.exists(ruta_icono):
                self.frame_modificar_intents.iconbitmap(ruta_icono)
            else:
                print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

            lblframe_modificar_intents = tb.LabelFrame(master=self.frame_modificar_intents, text="Editar Intención")
            lblframe_modificar_intents.pack(padx=15, pady=15)
            
            lbl_codigo_modificar_intencion = Label(master=lblframe_modificar_intents, text='Codigo')
            lbl_codigo_modificar_intencion.grid(row=0, column=0, padx=10, pady=10)
            self.ent_codigo_modificar_intencion = tb.Entry(master=lblframe_modificar_intents, width=40)
            self.ent_codigo_modificar_intencion.grid(row=0, column=1, padx=10, pady=10)
            lbl_codigo_modificar_intencion.grid_forget()
            self.ent_codigo_modificar_intencion.grid_forget()

            lbl_nombre_modificar_intents = Label(master=lblframe_modificar_intents, text='Intención')
            lbl_nombre_modificar_intents.grid(row=1, column=0, padx=10, pady=10)
            self.ent_nombre_modificar_intents = tb.Entry(master=lblframe_modificar_intents, width=40)
            self.ent_nombre_modificar_intents.grid(row=1, column=1, padx=10, pady=10)

            btn_modificar_intents = tb.Button(master=lblframe_modificar_intents, text='Guardar', width=36, command=self.modificar_intents)
            btn_modificar_intents.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_entry_intencion()
            
            self.ent_nombre_modificar_intents.focus_set()
            self.frame_modificar_intents.bind('<Return>', lambda event: self.modificar_intents())
        else:
            messagebox.showwarning('Modificar Intención', 'Ninguna Intención Seleccionada')

    def llenar_entry_intencion(self):
        self.ent_codigo_modificar_intencion.delete(0, END)
        self.ent_nombre_modificar_intents.delete(0, END)
        
        self.ent_codigo_modificar_intencion.insert(0, self.valor_intencion_seleccionado[0])
        self.ent_codigo_modificar_intencion.config(state='readonly')
        self.ent_nombre_modificar_intents.insert(0, self.valor_intencion_seleccionado[1])

    def modificar_intents(self):
        if self.ent_codigo_modificar_intencion.get() == '' or self.ent_nombre_modificar_intents.get() == '':
            messagebox.showerror('Modificando Intencion', 'Los campos a llenar no pueden estar vacios')
            return
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            intent_name = self.ent_nombre_modificar_intents.get().strip().lower()
            cursor.execute("SELECT Id FROM Intents WHERE LOWER(Tag) = ? AND Id != ?", 
                          (intent_name, self.ent_codigo_modificar_intencion.get()))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Ya existe otra intención con este nombre')
                return
                
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_usuario = self.nombre_usuario
            modificar_datos_intencion = (self.ent_nombre_modificar_intents.get(), fecha_actual, nombre_usuario, self.ent_codigo_modificar_intencion.get())
            cursor.execute("UPDATE Intents SET Tag=?, creacion=?, usuario=? WHERE Id=?", modificar_datos_intencion)

            conn.commit()
            messagebox.showinfo('Modificar Intención', 'Intención Modificada Exitosamente')
            self.valor_intencion_seleccionado = self.tree_lista_intents.item(self.intencion_seleccionado, text='', values=(int(self.ent_codigo_modificar_intencion.get()), str(self.ent_nombre_modificar_intents.get())))
            self.frame_modificar_intents.destroy()
            self.buscar_intents('')
        except Exception as e:
            messagebox.showerror('Modificando Intención', f'Ocurrió un Error Inesperado al Modificar: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()
            
    def centrar_mod_int(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_modificar_intents.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def centrar_new_int(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_nuevo_intents.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def eliminar_intents(self):
        intencion_seleccionado_eliminar = self.tree_lista_intents.focus()
        valor_intencion_selecionado_eliminar = self.tree_lista_intents.item(intencion_seleccionado_eliminar, 'values')

        if not valor_intencion_selecionado_eliminar:
            messagebox.showwarning('Error', 'Ninguna intención seleccionada')
            return

        respuesta = messagebox.askquestion('Eliminando Intención', 
                                        '¿Está seguro de eliminar esta intención?')
        
        if respuesta == 'yes':
            conn = None
            try:
                conn = sqlite3.connect(self.DB_PATH)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM Patterns WHERE IntentId=?", (valor_intencion_selecionado_eliminar[0],))
                if cursor.fetchone()[0] > 0:
                    messagebox.showwarning('Error', 'Esta intención tiene patrones asociados')
                    return
                    
                cursor.execute("SELECT COUNT(*) FROM Responses WHERE IntentId=?", (valor_intencion_selecionado_eliminar[0],))
                if cursor.fetchone()[0] > 0:
                    messagebox.showwarning('Error', 'Esta intención tiene respuestas asociadas')
                    return

                fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Tipo = "Eliminar"
                Tabla = "Intenciones"
                nombre_usuario = self.nombre_usuario
                datos = (Tipo, Tabla,valor_intencion_selecionado_eliminar[1],fecha_actual,nombre_usuario)
                cursor.execute("INSERT INTO datos_eliminados(Tipo,Tabla,Nombre,Fecha,Usuario) VALUES (?,?,?,?,?)", datos)
                cursor.execute("DELETE FROM Intents WHERE Id=?", (valor_intencion_selecionado_eliminar[0],))
                conn.commit()
                messagebox.showinfo('Éxito', 'Intención eliminada correctamente')
                self.buscar_intents('')
                
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'Ocurrió un error: {str(e)}')
                if conn:
                    conn.rollback()
            finally:
                if conn:
                    conn.close()

# Patrones apartado
    def ventana_lista_patterns(self):
        self.geometry("725x540")
        self.resaltar_boton("btn_patterns")
        self.frame_lista_patterns = tb.Frame(master=self)
        self.frame_lista_patterns.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        lblframe_botones_lista_patterns = tb.LabelFrame(master=self.frame_lista_patterns)
        lblframe_botones_lista_patterns.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        btn_nuevo_lista_patterns = tb.Button(master=lblframe_botones_lista_patterns, text="Nuevo", width=15, bootstyle="success", command=self.ventana_nuevo_pattern)
        btn_nuevo_lista_patterns.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_lista_patterns = tb.Button(master=lblframe_botones_lista_patterns, text="Modificar", width=15, bootstyle="secondary", command=self.ventana_modificar_patron)
        btn_modificar_lista_patterns.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_lista_patterns = tb.Button(master=lblframe_botones_lista_patterns, text="Eliminar", width=15, bootstyle="danger", command=self.eliminar_patrones)
        btn_eliminar_lista_patterns.grid(row=0, column=2, padx=10, pady=10)

        lblframe_busqueda_lista_patterns = tb.LabelFrame(master=self.frame_lista_patterns, text="Filtro de Datos")
        lblframe_busqueda_lista_patterns.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.ent_buscar_lista_patterns = tb.Entry(master=lblframe_busqueda_lista_patterns, width=90)
        self.ent_buscar_lista_patterns.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_patterns.bind('<Key>', self.buscar_patterns)

        lblframe_tree_lista_patterns = tb.LabelFrame(master=self.frame_lista_patterns)
        lblframe_tree_lista_patterns.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Id", "IntentId", "Pattern", "creacion","usuario")

        # Tabla
        self.tree_lista_patterns = tb.Treeview(master=lblframe_tree_lista_patterns, height=17, columns=columnas, show='headings', bootstyle='info')
        self.tree_lista_patterns.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        lblframe_tree_lista_patterns.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_patterns.grid_rowconfigure(0, weight=1)

        # Encabezados
        self.tree_lista_patterns.heading('IntentId', text='Intencion relacionada', anchor=W)
        self.tree_lista_patterns.heading('Pattern', text='Patron', anchor=W)
        self.tree_lista_patterns.heading('creacion', text='Fecha de Creacion', anchor=W)
        self.tree_lista_patterns.heading('usuario', text='usuario', anchor=W)

        self.tree_lista_patterns['displaycolumns'] = ('IntentId','Pattern', 'creacion','usuario')

        # Tamaño columnas
        self.tree_lista_patterns.column("IntentId", width=120)
        self.tree_lista_patterns.column("Pattern", width=150)
        self.tree_lista_patterns.column("creacion", width=100)
        self.tree_lista_patterns.column("usuario", width=100)

        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_patterns, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)
      
        tree_scroll.config(command=self.tree_lista_patterns.yview)
        self.buscar_patterns('')
        self.centrar_ventana()

    def buscar_patterns(self, event):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        registro = self.tree_lista_patterns.get_children()
        for elementos in registro:
            self.tree_lista_patterns.delete(elementos)

        cursor.execute("""
            SELECT 
                Patterns.Id AS PatternId, 
                Patterns.Pattern, 
                Intents.Tag AS IntentTag, 
                Patterns.creacion, 
                Patterns.usuario
            FROM 
                Patterns
            JOIN 
                Intents ON Patterns.IntentId = Intents.Id
            WHERE Patterns.Pattern LIKE ?
        """, (self.ent_buscar_lista_patterns.get() + '%',))

        datos_patterns = cursor.fetchall()

        for fila in datos_patterns:
            self.tree_lista_patterns.insert('', 0, fila[0], values=(fila[0], fila[2], fila[1], fila[3], fila[4]))

        conn.commit()
        cursor.close()
        conn.close()

    def ventana_nuevo_pattern(self):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Intents")
            resultados = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Ocurrió un error en la conexión: {e}")

        self.frame_nuevo_pattern = Toplevel(master=self)
        self.frame_nuevo_pattern.title("Nuevo Patrón")
        self.frame_nuevo_pattern.resizable(False, False)
        self.centrar_new_patron(500, 200)
        self.frame_nuevo_pattern.grab_set()
        
        ruta_icono = os.path.join("static", "images", "Admin.ico")
        if os.path.exists(ruta_icono):
            self.frame_nuevo_pattern.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

        lblframe_nuevo_pattern = tb.LabelFrame(master=self.frame_nuevo_pattern, text="Nuevo Patrón")
        lblframe_nuevo_pattern.pack(padx=15, pady=15)

        lbl_nombre_nuevo_pattern = Label(master=lblframe_nuevo_pattern, text='Patrones (separados por comas)')
        lbl_nombre_nuevo_pattern.grid(row=1, column=0, padx=10, pady=10)
        self.ent_nombre_nuevo_pattern = tb.Entry(master=lblframe_nuevo_pattern, width=40)
        self.ent_nombre_nuevo_pattern.grid(row=1, column=1, padx=10, pady=10)

        lbl_rol_nuevo_pattern = Label(master=lblframe_nuevo_pattern, text='Intencion')
        lbl_rol_nuevo_pattern.grid(row=2, column=0, padx=10, pady=10)
        self.cbo_rol_nuevo_pattern = tb.Combobox(master=lblframe_nuevo_pattern, width=38, values=[row[1] for row in resultados])
        self.cbo_rol_nuevo_pattern.grid(row=2, column=1, padx=10, pady=10)
        self.cbo_rol_nuevo_pattern.current(0)
        self.cbo_rol_nuevo_pattern.config(state='readonly')

        btn_Guardar_nuevo_pattern = Button(master=lblframe_nuevo_pattern, text='Guardar', width=36, command=self.guardar_patron)
        btn_Guardar_nuevo_pattern.grid(row=4, column=1, padx=10, pady=10)
        
        self.ent_nombre_nuevo_pattern.focus_set()
        self.frame_nuevo_pattern.bind('<Return>', lambda event: self.guardar_patron())

    def guardar_patron(self):
        if self.ent_nombre_nuevo_pattern.get() == '' or self.cbo_rol_nuevo_pattern.get() == '':
            messagebox.showerror('Guardando Patrones', 'Los campos a llenar no pueden estar vacios')
            return

        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            usuario = self.nombre_usuario
            guardarrol = self.cbo_rol_nuevo_pattern.get()
            cursor.execute("SELECT Id FROM Intents WHERE Tag = ?", (guardarrol,))
            codigotag = cursor.fetchone()
            
            if not codigotag:
                messagebox.showerror('Guardando Patrón', 'No se encontró el tag relacionado.')
                return
                
            patrones = [patron.strip() for patron in self.ent_nombre_nuevo_pattern.get().split(',')]
            
            # Verificar si los patrones ya existen para esta intención
            for patron in patrones:
                cursor.execute("SELECT Pattern FROM Patterns WHERE IntentId = ? AND Pattern = ?", 
                              (codigotag[0], patron))
                if cursor.fetchone():
                    messagebox.showerror('Error', f'El patrón "{patron}" ya existe para esta intención')
                    return
            
            for patron in patrones:
                fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO Patterns (IntentId, Pattern, creacion, usuario) VALUES (?, ?, ?, ?)", 
                            (codigotag[0], patron, fecha_actual, usuario))
                
            conn.commit()
            messagebox.showinfo('Guardando Patrones', 'Patrones agregados exitosamente')
            self.frame_nuevo_pattern.destroy()
            self.buscar_patterns('')
        except Exception as e:
            messagebox.showerror('Guardando Patrones', f'Ocurrió un error inesperado: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()
            
    def ventana_modificar_patron(self):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Intents")
            resultados = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Ocurrió un error en la conexión: {e}")
            
        self.patron_seleccionado = self.tree_lista_patterns.focus()
        self.valor_patron_seleccionado = self.tree_lista_patterns.item(self.patron_seleccionado, 'values')
        if self.valor_patron_seleccionado != '':
            self.frame_modificar_patron = Toplevel(master=self)
            self.frame_modificar_patron.title("Modificar Patrón")
            self.frame_modificar_patron.resizable(False, False)
            self.centrar_mod_patron(400,200)
            self.frame_modificar_patron.grab_set()
            
            ruta_icono = os.path.join("static", "images", "Admin.ico")
            if os.path.exists(ruta_icono):
                self.frame_modificar_patron.iconbitmap(ruta_icono)
            else:
                print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

            lblframe_modificar_patron = tb.LabelFrame(master=self.frame_modificar_patron, text="Editar Patrones")
            lblframe_modificar_patron.pack(padx=15, pady=15)
            
            lbl_codigo_modificar_patron = Label(master=lblframe_modificar_patron, text='Codigo')
            lbl_codigo_modificar_patron.grid(row=0, column=0, padx=10, pady=10)
            self.ent_codigo_modificar_patron = tb.Entry(master=lblframe_modificar_patron, width=40)
            self.ent_codigo_modificar_patron.grid(row=0, column=1, padx=10, pady=10)
            lbl_codigo_modificar_patron.grid_forget()
            self.ent_codigo_modificar_patron.grid_forget()

            lbl_nombre_modificar_patron = Label(master=lblframe_modificar_patron, text='Patron')
            lbl_nombre_modificar_patron.grid(row=1, column=0, padx=10, pady=10)
            self.ent_nombre_modificar_patron = tb.Entry(master=lblframe_modificar_patron, width=40)
            self.ent_nombre_modificar_patron.grid(row=1, column=1, padx=10, pady=10)

            lbl_rol_modificar_patron = Label(master=lblframe_modificar_patron, text='Intencion')
            lbl_rol_modificar_patron.grid(row=3, column=0, padx=10, pady=10)
            self.cbo_rol_modificar_patron = tb.Combobox(master=lblframe_modificar_patron, width=38, values=[row[1] for row in resultados])
            self.cbo_rol_modificar_patron.grid(row=3, column=1, padx=10, pady=10)
            self.cbo_rol_modificar_patron.config(state='readonly')

            btn_modificar_patron = tb.Button(master=lblframe_modificar_patron, text='Guardar', width=36, command=self.modificar_patrones)
            btn_modificar_patron.grid(row=4, column=1, padx=10, pady=10)
            self.llenar_modificar_patron()
            
            self.ent_nombre_modificar_patron.focus_set()
            self.frame_modificar_patron.bind('<Return>', lambda event: self.modificar_patrones())
        else:
            messagebox.showwarning('Modificar Patrones', 'Ningun Patron Seleccionado')

    def llenar_modificar_patron(self):
        self.ent_codigo_modificar_patron.delete(0, END)
        self.ent_nombre_modificar_patron.delete(0, END)
        self.cbo_rol_modificar_patron.delete(0, END)
        self.ent_codigo_modificar_patron.insert(0, self.valor_patron_seleccionado[0])
        self.ent_codigo_modificar_patron.config(state='readonly')
        self.ent_nombre_modificar_patron.insert(0, self.valor_patron_seleccionado[2])
        self.cbo_rol_modificar_patron.insert(0, self.valor_patron_seleccionado[1])
        self.cbo_rol_modificar_patron.config(state='readonly')

    def centrar_mod_patron(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_modificar_patron.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def centrar_new_patron(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_nuevo_pattern.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def modificar_patrones(self):
        if self.ent_nombre_modificar_patron.get() == '' or self.cbo_rol_modificar_patron.get() == '':
            messagebox.showerror('Modificando Patrones', 'Los campos a llenar no pueden estar vacios')
            return
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            guardarrol = self.cbo_rol_modificar_patron.get()
            cursor.execute("SELECT Id FROM Intents WHERE Tag = ?", (guardarrol,))
            codigotag = cursor.fetchone()
            verftag = self.ent_nombre_modificar_patron.get()
            nombre_usuario=self.nombre_usuario
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            modificar_datos_patron = (codigotag[0], verftag,fecha_actual,nombre_usuario,self.ent_codigo_modificar_patron.get())
            cursor.execute("UPDATE Patterns SET IntentId=?, Pattern=?, creacion=?, usuario=? WHERE Id=?", modificar_datos_patron)
            conn.commit()
            messagebox.showinfo('Modificar Patron', 'Patron Modificado Exitosamente')
            self.valor_patron_seleccionado = self.tree_lista_patterns.item(self.patron_seleccionado, text='', values=(int(self.ent_codigo_modificar_patron.get()), codigotag[0], str(self.ent_nombre_modificar_patron.get())))
            self.frame_modificar_patron.destroy()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Modificando Patron', f'Ocurrió un Error Inesperado al Modificar: {str(e)}')

    def eliminar_patrones(self):
        patron_seleccionado_eliminar = self.tree_lista_patterns.focus()
        valor_patron_selecionado_eliminar = self.tree_lista_patterns.item(patron_seleccionado_eliminar, 'values')

        if valor_patron_selecionado_eliminar != '':
            respuesta = messagebox.askquestion('Eliminando Patron', '¿Esta seguro de eliminar el Patron seleccionado?')
            if respuesta == 'yes':
                try:
                    conn = sqlite3.connect(self.DB_PATH)
                    cursor = conn.cursor()
                    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    nombre_usuario=self.nombre_usuario
                    Tipo="Eliminar"
                    Tabla="Patrones"
                    datos=(Tipo,Tabla,valor_patron_selecionado_eliminar[2],fecha_actual,nombre_usuario)
                    cursor.execute("INSERT INTO datos_eliminados(Tipo,Tabla,Nombre,Fecha,Usuario) VALUES (?,?,?,?,?)",datos)
                    cursor.execute("DELETE FROM Patterns WHERE Id=?", (valor_patron_selecionado_eliminar[0],))

                    conn.commit()
                    messagebox.showinfo('Eliminando Patron', 'Registro eliminado correctamente')
                    self.buscar_patterns('')
                    cursor.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror('Eliminando Patron', f'Ocurrió un Error Inesperado: {str(e)}')
            else:
                messagebox.showerror('Eliminando Patron', 'Eliminacion Cancelada')
        else:
            messagebox.showerror('Error', 'Ningún Patron Seleccinado')

# Respuestas apartado
    def ventana_lista_responses(self):
        self.geometry("805x540")
        self.resaltar_boton("btn_responses")
        self.frame_lista_respuestas = tb.Frame(master=self)
        self.frame_lista_respuestas.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        lblframe_botones_lista_respuestas = tb.LabelFrame(master=self.frame_lista_respuestas)
        lblframe_botones_lista_respuestas.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        btn_nuevo_lista_respuestas = tb.Button(master=lblframe_botones_lista_respuestas, text="Nuevo", width=15, bootstyle="success", command=self.ventana_nueva_respuesta)
        btn_nuevo_lista_respuestas.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_lista_respuestas = tb.Button(master=lblframe_botones_lista_respuestas, text="Modificar", width=15, bootstyle="secondary", command=self.ventana_modificar_respuesta)
        btn_modificar_lista_respuestas.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_lista_respuestas = tb.Button(master=lblframe_botones_lista_respuestas, text="Eliminar", width=15, bootstyle="danger", command=self.eliminar_respuesta)
        btn_eliminar_lista_respuestas.grid(row=0, column=2, padx=10, pady=10)

        lblframe_busqueda_lista_respuestas = tb.LabelFrame(master=self.frame_lista_respuestas, text="Filtro de Datos")
        lblframe_busqueda_lista_respuestas.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.ent_buscar_lista_respuestas = tb.Entry(master=lblframe_busqueda_lista_respuestas, width=90)
        self.ent_buscar_lista_respuestas.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_respuestas.bind('<Key>', self.buscar_respuestas)

        lblframe_tree_lista_respuestas = tb.LabelFrame(master=self.frame_lista_respuestas)
        lblframe_tree_lista_respuestas.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Id", "IntentId", "Response", "creacion","usuario")

        # Tabla
        self.tree_lista_respuestas = tb.Treeview(master=lblframe_tree_lista_respuestas, height=17, columns=columnas, show='headings', bootstyle='info')
        self.tree_lista_respuestas.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        lblframe_tree_lista_respuestas.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_respuestas.grid_rowconfigure(0, weight=1)

        # Encabezados
        self.tree_lista_respuestas.heading('IntentId', text='Intención', anchor=W)
        self.tree_lista_respuestas.heading('Response', text='Respuesta', anchor=W)
        self.tree_lista_respuestas.heading('creacion', text='Fecha de creación', anchor=W)
        self.tree_lista_respuestas.heading('usuario', text='Usuario', anchor=W)

        self.tree_lista_respuestas['displaycolumns'] = ('IntentId','Response', 'creacion','usuario')

        # Tamaño columnas
        self.tree_lista_respuestas.column("IntentId", width=100)
        self.tree_lista_respuestas.column("Response", width=300)
        self.tree_lista_respuestas.column("creacion", width=115)
        self.tree_lista_respuestas.column("usuario", width=80)

        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_respuestas, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)

        tree_scroll.config(command=self.tree_lista_respuestas.yview)
        self.buscar_respuestas('')
        self.centrar_ventana()

    def buscar_respuestas(self, event):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        registro = self.tree_lista_respuestas.get_children()
        for elementos in registro:
            self.tree_lista_respuestas.delete(elementos)

        cursor.execute("""
            SELECT 
                Responses.Id AS ResponseId, 
                Responses.Response, 
                Intents.Tag AS IntentTag, 
                Responses.creacion, 
                Responses.usuario
            FROM 
                Responses
            JOIN 
                Intents ON Responses.IntentId = Intents.Id
            WHERE Responses.Response LIKE ?
        """, (self.ent_buscar_lista_respuestas.get() + '%',))

        datos_responses = cursor.fetchall()

        for fila in datos_responses:
            self.tree_lista_respuestas.insert('', 0, fila[0], values=(fila[0], fila[2], fila[1], fila[3], fila[4]))

        conn.commit()
        cursor.close()
        conn.close()

    def ventana_nueva_respuesta(self):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Intents")
            resultados = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Ocurrió un error en la conexión: {e}")

        self.frame_nuevo_respuesta = Toplevel(master=self)
        self.frame_nuevo_respuesta.title("Nueva Respuesta")
        self.frame_nuevo_respuesta.resizable(False, False)
        self.centrar_new_respuesta(500, 400)
        self.frame_nuevo_respuesta.grab_set()
        
        ruta_icono = os.path.join("static", "images", "Admin.ico")
        if os.path.exists(ruta_icono):
            self.frame_nuevo_respuesta.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

        lblframe_nuevo_respuesta = tb.LabelFrame(master=self.frame_nuevo_respuesta, text="Nueva Respuesta")
        lblframe_nuevo_respuesta.pack(padx=15, pady=15, fill='both', expand=True)
        
        frame_controles = Frame(lblframe_nuevo_respuesta)
        frame_controles.pack(fill='x', pady=5)
        
        self.btn_negrita = tb.Button(frame_controles, text="Negrita", width=8, command=lambda: self.aplicar_formato("bold"))
        self.btn_negrita.pack(side='left', padx=2)
        
        self.btn_cursiva = tb.Button(frame_controles, text="Cursiva", width=8,command=lambda: self.aplicar_formato("italic"))
        self.btn_cursiva.pack(side='left', padx=2)
        
        self.btn_subrayado = tb.Button(frame_controles, text="Subrayado", width=10, command=lambda: self.aplicar_formato("underline"))
        self.btn_subrayado.pack(side='left', padx=2)
        
        frame_texto = Frame(lblframe_nuevo_respuesta)
        frame_texto.pack(fill='both', expand=True, pady=5)
        
        scrollbar = Scrollbar(frame_texto)
        scrollbar.pack(side='right', fill='y')
        
        self.ent_nombre_nuevo_respuesta = Text(frame_texto, wrap='word', yscrollcommand=scrollbar.set, height=10, width=50)
        self.ent_nombre_nuevo_respuesta.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.ent_nombre_nuevo_respuesta.yview)
        
        self.ent_nombre_nuevo_respuesta.tag_configure("bold", font=('Arial', 10, 'bold'))
        self.ent_nombre_nuevo_respuesta.tag_configure("italic", font=('Arial', 10, 'italic'))
        self.ent_nombre_nuevo_respuesta.tag_configure("underline", font=('Arial', 10, 'underline'))
        
        frame_inferior = Frame(lblframe_nuevo_respuesta)
        frame_inferior.pack(fill='x', pady=5)
        
        lbl_rol_nuevo_respuesta = Label(frame_inferior, text='Intención')
        lbl_rol_nuevo_respuesta.pack(side='left', padx=10, pady=10)
        self.cbo_rol_nuevo_respuesta = tb.Combobox(frame_inferior, width=38, values=[row[1] for row in resultados])
        self.cbo_rol_nuevo_respuesta.pack(side='left', padx=10, pady=10)
        self.cbo_rol_nuevo_respuesta.current(0)
        self.cbo_rol_nuevo_respuesta.config(state='readonly')

        btn_Guardar_nuevo_respuesta = tb.Button(lblframe_nuevo_respuesta, text='Guardar', width=36, command=self.guardar_respuesta)
        btn_Guardar_nuevo_respuesta.pack(pady=10)
        
        self.ent_nombre_nuevo_respuesta.focus_set()
        #self.frame_nuevo_respuesta.bind('<Return>', lambda event: self.guardar_respuesta())
        
    def aplicar_formato(self, formato):
        try:
            sel_start = self.ent_nombre_nuevo_respuesta.index("sel.first")
            sel_end = self.ent_nombre_nuevo_respuesta.index("sel.last")
            
            if sel_start and sel_end:
                for tag in self.ent_nombre_nuevo_respuesta.tag_names():
                    self.ent_nombre_nuevo_respuesta.tag_remove(tag, sel_start, sel_end)
                
                self.ent_nombre_nuevo_respuesta.tag_add(formato, sel_start, sel_end)
                
                current_tags = self.ent_nombre_nuevo_respuesta.tag_names(sel_start)
                for tag in current_tags:
                    if tag != formato:
                        self.ent_nombre_nuevo_respuesta.tag_add(tag, sel_start, sel_end)
        except:
            pass
          
    def guardar_respuesta(self):
        texto_respuesta = self.ent_nombre_nuevo_respuesta.get("1.0", "end-1c")
        if not texto_respuesta.strip() or self.cbo_rol_nuevo_respuesta.get() == '':
            messagebox.showerror('Guardando Respuestas', 'Los campos a llenar no pueden estar vacíos')
            return
        
        try:
            texto_con_formato = self.obtener_texto_con_formato()
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            guardarrol = self.cbo_rol_nuevo_respuesta.get()
            
            cursor.execute("SELECT Response FROM Responses WHERE IntentId = (SELECT Id FROM Intents WHERE Tag = ?) AND Response = ?", 
                          (guardarrol, texto_con_formato))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Ya existe una respuesta idéntica para esta intención')
                return
                
            cursor.execute("SELECT Id FROM Intents WHERE Tag = ?", (guardarrol,))
            codigotag = cursor.fetchone()
            usuario = self.nombre_usuario
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("INSERT INTO Responses (IntentId, Response, creacion, usuario) VALUES (?, ?, ?, ?)", 
                          (codigotag[0], texto_con_formato, fecha_actual, usuario))
            conn.commit()

            messagebox.showinfo('Guardando Respuestas', 'Respuesta Agregada Exitosamente')
            self.frame_nuevo_respuesta.destroy()
            self.buscar_respuestas('')
        except Exception as e:
            messagebox.showerror('Guardando Respuesta', f'Ocurrió un Error Inesperado: {str(e)}')
        finally:
            if 'conn' in locals():
                conn.close()

    def obtener_texto_con_formato(self):
        texto = self.ent_nombre_nuevo_respuesta.get("1.0", "end-1c")
        texto_formateado = texto
        
        texto = texto.replace('\n', '<br>')
        texto = texto.replace('  ', ' &nbsp;')
        
        for tag in self.ent_nombre_nuevo_respuesta.tag_names():
            ranges = self.ent_nombre_nuevo_respuesta.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                end = ranges[i+1]
                texto_seleccionado = self.ent_nombre_nuevo_respuesta.get(start, end)
                
                if tag == "bold":
                    texto_formateado = texto_formateado.replace(
                        texto_seleccionado, 
                        f"<b>{texto_seleccionado}</b>"
                    )
                elif tag == "italic":
                    texto_formateado = texto_formateado.replace(
                        texto_seleccionado, 
                        f"<i>{texto_seleccionado}</i>"
                    )
                elif tag == "underline":
                    texto_formateado = texto_formateado.replace(
                        texto_seleccionado, 
                        f"<u>{texto_seleccionado}</u>"
                    )
        
        return texto_formateado

    def ventana_modificar_respuesta(self):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Intents")
            resultados = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Ocurrió un error en la conexión: {e}")

        self.respuesta_seleccionado = self.tree_lista_respuestas.focus()
        self.valor_respuesta_seleccionado = self.tree_lista_respuestas.item(self.respuesta_seleccionado, 'values')
        
        if self.valor_respuesta_seleccionado != '':
            self.frame_modificar_respuesta = Toplevel(master=self)
            self.frame_modificar_respuesta.title("Modificar Respuesta")
            self.frame_modificar_respuesta.resizable(False, False)
            self.centrar_mod_respuesta(500, 400)
            self.frame_modificar_respuesta.grab_set()
            
            ruta_icono = os.path.join("static", "images", "Admin.ico")
            if os.path.exists(ruta_icono):
                self.frame_modificar_respuesta.iconbitmap(ruta_icono)
            else:
                print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")

            lblframe_modificar_respuesta = tb.LabelFrame(master=self.frame_modificar_respuesta, text="Editar Respuesta")
            lblframe_modificar_respuesta.pack(padx=15, pady=15, fill='both', expand=True)
            
            frame_controles = Frame(lblframe_modificar_respuesta)
            frame_controles.pack(fill='x', pady=5)
            
            self.btn_negrita = tb.Button(frame_controles, text="Negrita", width=8, command=lambda: self.aplicar_formato_mod("bold"))
            self.btn_negrita.pack(side='left', padx=2)
            
            self.btn_cursiva = tb.Button(frame_controles, text="Cursiva", width=8, command=lambda: self.aplicar_formato_mod("italic"))
            self.btn_cursiva.pack(side='left', padx=2)
            
            self.btn_subrayado = tb.Button(frame_controles, text="Subrayado", width=10, command=lambda: self.aplicar_formato_mod("underline"))
            self.btn_subrayado.pack(side='left', padx=2)
            
            frame_texto = Frame(lblframe_modificar_respuesta)
            frame_texto.pack(fill='both', expand=True, pady=5)
            
            scrollbar = Scrollbar(frame_texto)
            scrollbar.pack(side='right', fill='y')
            
            self.ent_nombre_modificar_respuesta = Text(frame_texto, wrap='word', yscrollcommand=scrollbar.set, height=10, width=50)
            self.ent_nombre_modificar_respuesta.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=self.ent_nombre_modificar_respuesta.yview)
            
            self.ent_nombre_modificar_respuesta.tag_configure("bold", font=('Arial', 10, 'bold'))
            self.ent_nombre_modificar_respuesta.tag_configure("italic", font=('Arial', 10, 'italic'))
            self.ent_nombre_modificar_respuesta.tag_configure("underline", font=('Arial', 10, 'underline'))
            
            frame_inferior = Frame(lblframe_modificar_respuesta)
            frame_inferior.pack(fill='x', pady=5)
            
            lbl_rol_modificar_respuesta = Label(frame_inferior, text='Intención')
            lbl_rol_modificar_respuesta.pack(side='left', padx=10, pady=10)
            self.cbo_rol_modificar_respuesta = tb.Combobox(frame_inferior, width=38, values=[row[1] for row in resultados])
            self.cbo_rol_modificar_respuesta.pack(side='left', padx=10, pady=10)
            self.cbo_rol_modificar_respuesta.config(state='readonly')

            btn_modificar_respuesta = tb.Button(lblframe_modificar_respuesta, text='Guardar', width=36, command=self.modificar_respuesta)
            btn_modificar_respuesta.pack(pady=10)
            
            self.llenar_modificar_respuesta()
            self.ent_nombre_modificar_respuesta.focus_set()
            #self.frame_modificar_respuesta.bind('<Return>', lambda event: self.modificar_respuesta())
        else:
            messagebox.showwarning('Modificar Respuesta', 'Ninguna Respuesta Seleccionada para modificar')

    def aplicar_formato_mod(self, formato):
        try:
            sel_start = self.ent_nombre_modificar_respuesta.index("sel.first")
            sel_end = self.ent_nombre_modificar_respuesta.index("sel.last")
            
            if sel_start and sel_end:
                for tag in self.ent_nombre_modificar_respuesta.tag_names():
                    self.ent_nombre_modificar_respuesta.tag_remove(tag, sel_start, sel_end)
                
                self.ent_nombre_modificar_respuesta.tag_add(formato, sel_start, sel_end)
                
                current_tags = self.ent_nombre_modificar_respuesta.tag_names(sel_start)
                for tag in current_tags:
                    if tag != formato:
                        self.ent_nombre_modificar_respuesta.tag_add(tag, sel_start, sel_end)
        except:
            pass

    def llenar_modificar_respuesta(self):
        self.ent_codigo_modificar_respuesta = tb.Entry()
        self.ent_codigo_modificar_respuesta.delete(0, END)
        self.ent_nombre_modificar_respuesta.delete("1.0", END)
        self.cbo_rol_modificar_respuesta.delete(0, END)
        
        self.ent_codigo_modificar_respuesta.insert(0, self.valor_respuesta_seleccionado[0])
        self.cbo_rol_modificar_respuesta.insert(0, self.valor_respuesta_seleccionado[1])
        self.cbo_rol_modificar_respuesta.config(state='readonly')
        
        respuesta = self.valor_respuesta_seleccionado[2]
        self.cargar_texto_con_formato(respuesta)

    def cargar_texto_con_formato(self, texto_html):
        self.ent_nombre_modificar_respuesta.delete("1.0", END)
        
        texto_html = texto_html.replace('<br>', '\n').replace('&nbsp;', ' ')
        
        import re
        tag_pattern = re.compile(r'(<([biu])>(.*?)</\2>)', re.DOTALL)
        
        tag_map = {'b': 'bold', 'i': 'italic', 'u': 'underline'}
        
        current_pos = "1.0"
        
        matches = list(tag_pattern.finditer(texto_html))
        
        if not matches:
            self.ent_nombre_modificar_respuesta.insert("1.0", texto_html)
            return
        
        if matches[0].start() > 0:
            self.ent_nombre_modificar_respuesta.insert("1.0", texto_html[:matches[0].start()])
            current_pos = self.ent_nombre_modificar_respuesta.index("end-1c")
        
        for i, match in enumerate(matches):
            tag_type = match.group(2)
            tag_content = match.group(3)
            
            start_pos = current_pos
            self.ent_nombre_modificar_respuesta.insert(current_pos, tag_content)
            end_pos = self.ent_nombre_modificar_respuesta.index(f"{start_pos}+{len(tag_content)}c")
            
            self.ent_nombre_modificar_respuesta.tag_add(tag_map[tag_type], start_pos, end_pos)
            
            if i < len(matches) - 1:
                next_match = matches[i+1]
                between_text = texto_html[match.end():next_match.start()]
                if between_text:
                    self.ent_nombre_modificar_respuesta.insert(end_pos, between_text)
                    current_pos = self.ent_nombre_modificar_respuesta.index("end-1c")
            else:
                remaining_text = texto_html[match.end():]
                if remaining_text:
                    self.ent_nombre_modificar_respuesta.insert(end_pos, remaining_text)

    def modificar_respuesta(self):
        texto_respuesta = self.ent_nombre_modificar_respuesta.get("1.0", "end-1c")
        if not texto_respuesta.strip() or self.cbo_rol_modificar_respuesta.get() == '':
            messagebox.showerror('Modificando Respuesta', 'Los campos a llenar no pueden estar vacíos')
            return
        
        try:
            texto_con_formato = self.obtener_texto_con_formato_mod()
            
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            guardarrol = self.cbo_rol_modificar_respuesta.get()
            cursor.execute("SELECT Id FROM Intents WHERE Tag = ?", (guardarrol,))
            codigotag = cursor.fetchone()
            usuario = self.nombre_usuario
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("UPDATE Responses SET IntentId=?, Response=?, creacion=?, usuario=? WHERE Id=?", (codigotag[0], texto_con_formato, fecha_actual, usuario, self.ent_codigo_modificar_respuesta.get()))
            conn.commit()
            
            messagebox.showinfo('Modificar Respuesta', 'Respuesta Modificada Exitosamente')
            self.frame_modificar_respuesta.destroy()
            self.buscar_respuestas('')
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Modificando Respuesta', f'Ocurrió un Error Inesperado al Modificar: {str(e)}')

    def obtener_texto_con_formato_mod(self):
        texto = self.ent_nombre_modificar_respuesta.get("1.0", "end-1c")
        texto_formateado = texto
        
        # Procesar saltos de linea
        texto_formateado = texto_formateado.replace('\n', '<br>')
        
        # Procesar negritas
        ranges = self.ent_nombre_modificar_respuesta.tag_ranges("bold")
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            end = ranges[i+1]
            texto_seleccionado = self.ent_nombre_modificar_respuesta.get(start, end)
            texto_formateado = texto_formateado.replace(
                texto_seleccionado, 
                f"<b>{texto_seleccionado}</b>"
            )
        
        # Procesar cursivas
        ranges = self.ent_nombre_modificar_respuesta.tag_ranges("italic")
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            end = ranges[i+1]
            texto_seleccionado = self.ent_nombre_modificar_respuesta.get(start, end)
            texto_formateado = texto_formateado.replace(
                texto_seleccionado, 
                f"<i>{texto_seleccionado}</i>"
            )
        
        # Procesar subrayado
        ranges = self.ent_nombre_modificar_respuesta.tag_ranges("underline")
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            end = ranges[i+1]
            texto_seleccionado = self.ent_nombre_modificar_respuesta.get(start, end)
            texto_formateado = texto_formateado.replace(
                texto_seleccionado, 
                f"<u>{texto_seleccionado}</u>"
            )
        
        return texto_formateado

    def centrar_mod_respuesta(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_modificar_respuesta.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def centrar_new_respuesta(self, ancho, altura):
        Ventana_ancho = ancho
        Ventana_altura = altura

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        cordenadas_x = int((pantalla_ancho / 2) - (Ventana_ancho / 2))
        cordenadas_y = int((pantalla_alto / 2) - (Ventana_altura / 2))

        self.frame_nuevo_respuesta.geometry('{}x{}+{}+{}'.format(Ventana_ancho, Ventana_altura, cordenadas_x, cordenadas_y))

    def eliminar_respuesta(self):
        respuesta_seleccionado_eliminar = self.tree_lista_respuestas.focus()
        valor_respuesta_selecionado_eliminar = self.tree_lista_respuestas.item(respuesta_seleccionado_eliminar, 'values')

        if valor_respuesta_selecionado_eliminar != '':
            respuesta = messagebox.askquestion('Eliminando Respuesta', '¿Esta seguro de eliminar la Respuesta seleccionada?')
            if respuesta == 'yes':
                try:
                    conn = sqlite3.connect(self.DB_PATH)
                    cursor = conn.cursor()
                    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    nombre_usuario=self.nombre_usuario
                    Tipo="Eliminar"
                    Tabla="Respuestas"
                    datos=(Tipo,Tabla,valor_respuesta_selecionado_eliminar[2],fecha_actual,nombre_usuario)
                    cursor.execute("INSERT INTO datos_eliminados(Tipo,Tabla,Nombre,Fecha,Usuario) VALUES (?,?,?,?,?)",datos)
                    cursor.execute("DELETE FROM Responses WHERE Id=?", (valor_respuesta_selecionado_eliminar[0],))

                    conn.commit()
                    messagebox.showinfo('Eliminando Respuesta', 'Registro eliminado correctamente')
                    self.buscar_respuestas('')
                    cursor.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror('Eliminando Respuesta', f'Ocurrió un Error Inesperado: {str(e)}')
            else:
                messagebox.showerror('Eliminando Respuestas', 'Eliminacion Cancelada')
        else:
            messagebox.showerror('Error', 'Ninguna Respuesta seleccionada')

# Botones apartado
    def ventana_lista_buttons(self):
        self.geometry("815x540")
        self.resaltar_boton("btn_buttons")
        self.frame_lista_buttons = tb.Frame(master=self)
        self.frame_lista_buttons.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        lblframe_botones_lista_buttons = tb.LabelFrame(master=self.frame_lista_buttons)
        lblframe_botones_lista_buttons.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        btn_nuevo_lista_buttons = tb.Button(master=lblframe_botones_lista_buttons, text="Nuevo", width=15, bootstyle="success", command=self.ventana_nuevo_button)
        btn_nuevo_lista_buttons.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_lista_buttons = tb.Button(master=lblframe_botones_lista_buttons, text="Modificar", width=15, bootstyle="secondary", command=self.ventana_modificar_button)
        btn_modificar_lista_buttons.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_lista_buttons = tb.Button(master=lblframe_botones_lista_buttons, text="Eliminar", width=15, bootstyle="danger", command=self.eliminar_button)
        btn_eliminar_lista_buttons.grid(row=0, column=2, padx=10, pady=10)

        lblframe_busqueda_lista_buttons = tb.LabelFrame(master=self.frame_lista_buttons, text="Filtro de Datos")
        lblframe_busqueda_lista_buttons.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.ent_buscar_lista_buttons = tb.Entry(master=lblframe_busqueda_lista_buttons, width=104)
        self.ent_buscar_lista_buttons.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_buttons.bind('<Key>', self.buscar_buttons)

        lblframe_tree_lista_buttons = tb.LabelFrame(master=self.frame_lista_buttons)
        lblframe_tree_lista_buttons.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Id", "IntentId", "Text", "Value","creacion","usuario")

        # Tabla
        self.tree_lista_buttons = tb.Treeview(master=lblframe_tree_lista_buttons, height=17, columns=columnas, show='headings', bootstyle='info')
        self.tree_lista_buttons.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        lblframe_tree_lista_buttons.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_buttons.grid_rowconfigure(0, weight=1)

        # Encabezados
        #self.tree_lista_buttons.heading('Id', text='Codigo', anchor=W)
        self.tree_lista_buttons.heading('IntentId', text='Tag relacionado', anchor=W)
        self.tree_lista_buttons.heading('Text', text='Texto del botón', anchor=W)
        self.tree_lista_buttons.heading('Value', text='Valor del botón', anchor=W)
        self.tree_lista_buttons.heading('creacion', text='Fecha', anchor=W)
        self.tree_lista_buttons.heading('usuario', text='usuario', anchor=W)

        self.tree_lista_buttons['displaycolumns'] = ('IntentId','Text', 'Value','creacion','usuario')

        # Tamaño columnas
        self.tree_lista_buttons.column("Id", width=100)
        self.tree_lista_buttons.column("IntentId", width=100)
        self.tree_lista_buttons.column("Text", width=100)
        self.tree_lista_buttons.column("Value", width=100)
        self.tree_lista_buttons.column("creacion", width=100)
        self.tree_lista_buttons.column("usuario", width=100)

        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_buttons, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)

        tree_scroll.config(command=self.tree_lista_buttons.yview)
        self.buscar_buttons('')
        self.centrar_ventana()

    def buscar_buttons(self, event):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            registro = self.tree_lista_buttons.get_children()
            for elementos in registro:
                self.tree_lista_buttons.delete(elementos)

            cursor.execute("""
                SELECT 
                    Buttons.Id AS ButtonId, 
                    Buttons.Text, 
                    Buttons.Value, 
                    Intents.Tag AS IntentTag, 
                    Buttons.creacion, 
                    Buttons.usuario
                FROM 
                    Buttons
                JOIN 
                    Intents ON Buttons.IntentId = Intents.Id
                WHERE Buttons.Text LIKE ?
            """, (self.ent_buscar_lista_buttons.get() + '%',))

            datos_buttons = cursor.fetchall()

            for fila in datos_buttons:
                self.tree_lista_buttons.insert('', 0, fila[0], values=(fila[0], fila[3], fila[1], fila[2], fila[4], fila[5]))

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en buscar_buttons: {e}")

    def ventana_nuevo_button(self):
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Intents")
            resultados = cursor.fetchall()
            self.id_dict = {row[1]: row[0] for row in resultados}
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {str(e)}")
            return
        
        self.frame_nuevo_button = Toplevel(master=self)
        self.frame_nuevo_button.title("Nuevo Botón")
        self.frame_nuevo_button.resizable(False, False)
        self.centrar_new_button(450, 300)
        self.frame_nuevo_button.grab_set()

        lblframe_nuevo_button = tb.LabelFrame(master=self.frame_nuevo_button, text="Agregar Nuevo Botón")
        lblframe_nuevo_button.pack(padx=15, pady=15)

        lbl_codigo_nuevo_button = Label(master=lblframe_nuevo_button, text='Código')
        lbl_codigo_nuevo_button.grid(row=0, column=0, padx=10, pady=10)
        self.ent_codigo_nuevo_button = tb.Entry(master=lblframe_nuevo_button, width=40)
        self.ent_codigo_nuevo_button.grid(row=0, column=1, padx=10, pady=10)
        self.ent_codigo_nuevo_button.config(state='readonly')
        lbl_codigo_nuevo_button.grid_forget()
        self.ent_codigo_nuevo_button.grid_forget()


        lbl_tag_nuevo_button = Label(master=lblframe_nuevo_button, text='Inteción donde \nse muestra el botón')
        lbl_tag_nuevo_button.grid(row=1, column=0, padx=10, pady=10)
        self.cbo_tag_nuevo_button = tb.Combobox(master=lblframe_nuevo_button, width=38, values=list(self.id_dict.keys()),)
        self.cbo_tag_nuevo_button.grid(row=1, column=1, padx=10, pady=10)
        self.cbo_tag_nuevo_button.bind("<<ComboboxSelected>>", self.actualizar_comboboxN)
        self.cbo_tag_nuevo_button.config(state='readonly')


        lbl_texto_nuevo_button = Label(master=lblframe_nuevo_button, text='Texto del botón')
        lbl_texto_nuevo_button.grid(row=2, column=0, padx=10, pady=10)
        self.ent_texto_nuevo_button = tb.Entry(master=lblframe_nuevo_button, width=40)
        self.ent_texto_nuevo_button.grid(row=2, column=1, padx=10, pady=10)

        lbl_rel_nuevo_button = Label(master=lblframe_nuevo_button, text='Dirigido a')
        lbl_rel_nuevo_button.grid(row=3, column=0, padx=10, pady=10)
        self.cbo_rel_nuevo_button = tb.Combobox(master=lblframe_nuevo_button, width=38, values=list(self.id_dict.keys()),)
        self.cbo_rel_nuevo_button.grid(row=3, column=1, padx=10, pady=10)
        self.cbo_rel_nuevo_button.bind("<<ComboboxSelected>>", self.actualizar_comboboxN)
        self.cbo_rel_nuevo_button.config(state='readonly')

        lbl_valor_nuevo_button = Label(master=lblframe_nuevo_button, text='Valor del botón')
        lbl_valor_nuevo_button.grid(row=4, column=0, padx=10, pady=10)
        self.cbo_valor_nuevo_button = tb.Combobox(master=lblframe_nuevo_button, width=40)
        self.cbo_valor_nuevo_button.grid(row=4, column=1, padx=10, pady=10)
        self.cbo_valor_nuevo_button.config(state='readonly')

        btn_guardar_nuevo_button = tb.Button(master=lblframe_nuevo_button, text='Guardar', width=36, bootstyle="success", command=self.guardar_button)
        btn_guardar_nuevo_button.grid(row=5, column=1, padx=10, pady=10)
        

    def actualizar_comboboxN(self, event):
        seleccionado = self.cbo_rel_nuevo_button.get()

        if seleccionado in self.id_dict:
            id_seleccionado = self.id_dict[seleccionado]

            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT Pattern FROM Patterns WHERE IntentId = ?", (id_seleccionado,))
            datos = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            self.cbo_valor_nuevo_button['values'] = [row[0] for row in datos]


    def guardar_button(self):
        if (self.ent_texto_nuevo_button.get() == '' or 
            self.cbo_valor_nuevo_button.get() == '' or 
            self.cbo_tag_nuevo_button.get() == ''):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT Id FROM Intents WHERE Tag = ?", (self.cbo_tag_nuevo_button.get(),))
            intent_id = cursor.fetchone()[0]

            cursor.execute("SELECT Text FROM Buttons WHERE IntentId = ? AND Text = ?", (intent_id, self.ent_texto_nuevo_button.get()))
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe un botón con este texto para esta intención")
                return
                
            cursor.execute("SELECT Value FROM Buttons WHERE IntentId = ? AND Value = ?", (intent_id, self.cbo_valor_nuevo_button.get()))
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe un botón con este valor para esta intención")
                return

            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            usuario = self.nombre_usuario
            
            cursor.execute("INSERT INTO Buttons (IntentId, Text, Value, creacion, usuario) VALUES (?, ?, ?, ?, ?)", (intent_id, self.ent_texto_nuevo_button.get(), self.cbo_valor_nuevo_button.get(), fecha_actual, usuario))
            conn.commit()

            messagebox.showinfo("Éxito", "Botón agregado correctamente")
            self.frame_nuevo_button.destroy()
            self.buscar_buttons('')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el botón: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def ventana_modificar_button(self):
        self.button_seleccionado = self.tree_lista_buttons.focus()
        self.valor_button_seleccionado = self.tree_lista_buttons.item(self.button_seleccionado, 'values')

        if self.valor_button_seleccionado:
            try:
                conn = sqlite3.connect(self.DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Intents")
                resultados = cursor.fetchall()
                self.id_dict = {row[1]: row[0] for row in resultados}
                conn.commit()
                cursor.close()
                conn.close()
            except:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return

            self.frame_modificar_button = Toplevel(master=self)
            self.frame_modificar_button.title("Modificar Botón")
            self.frame_modificar_button.resizable(False, False)
            self.centrar_mod_button(450, 300)
            self.frame_modificar_button.grab_set()

            lblframe_modificar_button = tb.LabelFrame(master=self.frame_modificar_button, text="Editar Botón")
            lblframe_modificar_button.pack(padx=15, pady=15)

            lbl_codigo_modificar_button = Label(master=lblframe_modificar_button, text='Código')
            lbl_codigo_modificar_button.grid(row=0, column=0, padx=10, pady=10)
            self.ent_codigo_modificar_button = tb.Entry(master=lblframe_modificar_button, width=40)
            self.ent_codigo_modificar_button.grid(row=0, column=1, padx=10, pady=10)
            lbl_codigo_modificar_button.grid_forget()
            self.ent_codigo_modificar_button.grid_forget()


            lbl_texto_modificar_button = Label(master=lblframe_modificar_button, text='Texto del botón')
            lbl_texto_modificar_button.grid(row=2, column=0, padx=10, pady=10)
            self.ent_texto_modificar_button = tb.Entry(master=lblframe_modificar_button, width=40)
            self.ent_texto_modificar_button.grid(row=2, column=1, padx=10, pady=10)

            lbl_rel_modificar_button = Label(master=lblframe_modificar_button, text='Dirigido a')
            lbl_rel_modificar_button.grid(row=3, column=0, padx=10, pady=10)
            self.cbo_rel_modificar_button = tb.Combobox(master=lblframe_modificar_button, width=38, values=list(self.id_dict.keys()),)
            self.cbo_rel_modificar_button.grid(row=3, column=1, padx=10, pady=10)
            self.cbo_rel_modificar_button.bind("<<ComboboxSelected>>", self.actualizar_combobox)
            self.cbo_rel_modificar_button.config(state='readonly')

            lbl_valor_modificar_button = Label(master=lblframe_modificar_button, text='Valor del botón')
            lbl_valor_modificar_button.grid(row=4, column=0, padx=10, pady=10)
            self.cbo_valor_modificar_button = tb.Combobox(master=lblframe_modificar_button, width=40)
            self.cbo_valor_modificar_button.grid(row=4, column=1, padx=10, pady=10)
            self.cbo_valor_modificar_button.config(state='readonly')

            lbl_tag_modificar_button = Label(master=lblframe_modificar_button, text='Inteción donde \nse muestra el botón')
            lbl_tag_modificar_button.grid(row=1, column=0, padx=10, pady=10)
            self.cbo_tag_modificar_button = tb.Combobox(master=lblframe_modificar_button, width=38, values=list(self.id_dict.keys()),)
            self.cbo_tag_modificar_button.grid(row=1, column=1, padx=10, pady=10)
            self.cbo_tag_modificar_button.bind("<<ComboboxSelected>>", self.actualizar_combobox)
            self.cbo_tag_modificar_button.config(state='readonly')

            btn_guardar_modificar_button = tb.Button(master=lblframe_modificar_button, text='Guardar', width=36, command=self.modificar_button)
            btn_guardar_modificar_button.grid(row=5, column=1, padx=10, pady=10)
            self.llenar_entry_modificar_button()
            
            self.ent_texto_modificar_button.focus_set()
            self.frame_modificar_button.bind('<Return>', lambda event: self.modificar_button())
        else:
            messagebox.showwarning("Advertencia", "Ningún botón seleccionado")

    def actualizar_combobox(self, event):
        seleccionado = self.cbo_rel_modificar_button.get()

        if seleccionado in self.id_dict:
            id_seleccionado = self.id_dict[seleccionado]

            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT Pattern FROM Patterns WHERE IntentId = ?", (id_seleccionado,))
            datos = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            self.cbo_valor_modificar_button['values'] = [row[0] for row in datos]

    def llenar_entry_modificar_button(self):
        self.ent_codigo_modificar_button.delete(0, END)
        self.ent_texto_modificar_button.delete(0, END)
        self.cbo_valor_modificar_button.delete(0, END)
        self.cbo_tag_modificar_button.delete(0, END)

        self.ent_codigo_modificar_button.insert(0, self.valor_button_seleccionado[0])
        self.ent_texto_modificar_button.insert(0, self.valor_button_seleccionado[2])
        self.cbo_valor_modificar_button.insert(0, self.valor_button_seleccionado[3])
        self.cbo_tag_modificar_button.insert(0, self.valor_button_seleccionado[1])

    def modificar_button(self):
        if self.ent_texto_modificar_button.get() == '' or self.cbo_valor_modificar_button.get() == '' or self.cbo_tag_modificar_button.get() == '':
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT Id FROM Intents WHERE Tag = ?", (self.cbo_tag_modificar_button.get(),))
            intent_id = cursor.fetchone()[0]

            cursor.execute("UPDATE Buttons SET IntentId=?, Text=?, Value=? WHERE Id=?", 
                          (intent_id,self.ent_texto_modificar_button.get(), self.cbo_valor_modificar_button.get(),self.ent_codigo_modificar_button.get()))
            conn.commit()

            messagebox.showinfo("Éxito", "Botón modificado correctamente")
            self.frame_modificar_button.destroy()
            self.buscar_buttons('')
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el botón: {str(e)}")

    def eliminar_button(self):
        button_seleccionado = self.tree_lista_buttons.focus()
        valor_button_seleccionado = self.tree_lista_buttons.item(button_seleccionado, 'values')

        if valor_button_seleccionado:
            respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este botón?")
            if respuesta:
                try:
                    conn = sqlite3.connect(self.DB_PATH)
                    cursor = conn.cursor()
                    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    nombre_usuario=self.nombre_usuario
                    Tipo="Eliminar"
                    Tabla="Botones"
                    datos=(Tipo,Tabla,valor_button_seleccionado[2],fecha_actual,nombre_usuario)
                    cursor.execute("INSERT INTO datos_eliminados(Tipo,Tabla,Nombre,Fecha,Usuario) VALUES (?,?,?,?,?)",datos)
                    cursor.execute("DELETE FROM Buttons WHERE Id=?", (valor_button_seleccionado[0],))
                    conn.commit()

                    messagebox.showinfo("Éxito", "Botón eliminado correctamente")
                    self.buscar_buttons('')
                    cursor.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el botón: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Ningún botón seleccionado")
    
    def centrar_mod_button(self, ancho, altura):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (altura // 2)

        self.frame_modificar_button.geometry(f'{ancho}x{altura}+{x}+{y}')
    
    def centrar_new_button(self, ancho, altura):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (altura // 2)

        self.frame_nuevo_button.geometry(f'{ancho}x{altura}+{x}+{y}')
        
   # Movimientos apartado
    def ventana_lista_movimientos(self):
        self.geometry("725x540")
        self.resaltar_boton("btn_movimientos")
        self.frame_lista_movimientos = tb.Frame(master=self)
        self.frame_lista_movimientos.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        lblframe_busqueda_lista_movimientos = tb.LabelFrame(master=self.frame_lista_movimientos, text="Filtro de Datos")
        lblframe_busqueda_lista_movimientos.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.ent_buscar_lista_movimientos = tb.Entry(master=lblframe_busqueda_lista_movimientos, width=90)
        self.ent_buscar_lista_movimientos.grid(row=0, column=0, padx=10, pady=10)
        
        self.ent_buscar_lista_movimientos.bind('<Key>', self.buscar_movimiento)

        lblframe_tree_lista_movimientos = tb.LabelFrame(master=self.frame_lista_movimientos)
        lblframe_tree_lista_movimientos.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Id", "Tipo", "Tabla","Nombre","Fecha","Usuario")

        # Tabla
        self.tree_lista_movimientos = tb.Treeview(master=lblframe_tree_lista_movimientos, height=17, columns=columnas, show='headings', bootstyle='info')
        self.tree_lista_movimientos.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        lblframe_tree_lista_movimientos.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_movimientos.grid_rowconfigure(0, weight=1)

        # Encabezados
       # self.tree_lista_movimientos.heading('Id', text='Codigo', anchor=W)
        self.tree_lista_movimientos.heading('Tipo', text='Operacion', anchor=W)
        self.tree_lista_movimientos.heading('Tabla', text='Tabla', anchor=W)
        self.tree_lista_movimientos.heading('Nombre', text='Nombre', anchor=W)
        self.tree_lista_movimientos.heading('Fecha', text='Fecha', anchor=W)
        self.tree_lista_movimientos.heading('Usuario', text='Usuario', anchor=W)

        self.tree_lista_movimientos['displaycolumns'] = ('Tipo', 'Tabla','Nombre','Fecha','Usuario')

        # Tamaño columnas
        self.tree_lista_movimientos.column("Id", width=100)
        self.tree_lista_movimientos.column("Tipo", width=100)
        self.tree_lista_movimientos.column("Tabla", width=100)
        self.tree_lista_movimientos.column("Nombre", width=100)
        self.tree_lista_movimientos.column("Fecha", width=150)
        self.tree_lista_movimientos.column("Usuario", width=70)

        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_movimientos, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)

        tree_scroll.config(command=self.tree_lista_movimientos.yview)
        self.buscar_movimiento('')
        self.centrar_ventana()

    def buscar_movimiento(self, event):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        registro = self.tree_lista_movimientos.get_children()
        for elementos in registro:
            self.tree_lista_intents.delete(elementos)

        cursor.execute("SELECT * FROM datos_eliminados WHERE Nombre LIKE ?", (self.ent_buscar_lista_movimientos.get() + '%',))
        datos_eliminados = cursor.fetchall()
        
        for fila in datos_eliminados:
            self.tree_lista_movimientos.insert('', 0, fila[0], values=(fila[0], fila[1], fila[2],fila[3],fila[4],fila[5]))

        conn.commit()
        cursor.close()
        conn.close()
    
#Recomendaciones Apartado
    def ventana_lista_reco(self):
        self.geometry("815x575")
        self.resaltar_boton("btn_reco")
        self.frame_lista_reco = tb.Frame(master=self)
        self.frame_lista_reco.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        lblframe_botones_lista_reco = tb.LabelFrame(master=self.frame_lista_reco)
        lblframe_botones_lista_reco.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        btn_eliminar_lista_reco = tb.Button(master=lblframe_botones_lista_reco, text="Eliminar", width=15,bootstyle="danger", command=self.eliminar_recomendacion)
        btn_eliminar_lista_reco.grid(row=0, column=0, padx=10, pady=10)

        lblframe_busqueda_lista_reco = tb.LabelFrame(master=self.frame_lista_reco, text="Filtro de Datos")
        lblframe_busqueda_lista_reco.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.ent_buscar_lista_reco = tb.Entry(master=lblframe_busqueda_lista_reco, width=90)
        self.ent_buscar_lista_reco.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_reco.bind('<Key>', self.buscar_reco)

        lblframe_tree_lista_reco = tb.LabelFrame(master=self.frame_lista_reco)
        lblframe_tree_lista_reco.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        # Columnas
        columnas = ("Id", "Mensaje", "Fecha", "Correo")

        # Tabla
        self.tree_lista_reco = tb.Treeview(master=lblframe_tree_lista_reco, height=17, columns=columnas, 
        show='headings', bootstyle='info')
        self.tree_lista_reco.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        lblframe_tree_lista_reco.grid_columnconfigure(0, weight=1)
        lblframe_tree_lista_reco.grid_rowconfigure(0, weight=1)

        # Encabezados
        self.tree_lista_reco.heading('Mensaje', text='Mensaje', anchor=W)
        self.tree_lista_reco.heading('Fecha', text='Fecha', anchor=W)
        self.tree_lista_reco.heading('Correo', text='Correo', anchor=W)

        self.tree_lista_reco['displaycolumns'] = ('Mensaje', 'Fecha', 'Correo')

        # Tamaño columnas
        self.tree_lista_reco.column("Id", width=0, stretch=NO)
        self.tree_lista_reco.column("Mensaje", width=320)
        self.tree_lista_reco.column("Fecha", width=80)
        self.tree_lista_reco.column("Correo", width=200)

        # Scroll
        tree_scroll = tb.Scrollbar(master=lblframe_tree_lista_reco, bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)
        tree_scroll.config(command=self.tree_lista_reco.yview)

        self.buscar_reco('')
        self.centrar_ventana()

    def eliminar_recomendacion(self):
        recomendacion_seleccionada = self.tree_lista_reco.focus()
        valor_recomendacion_seleccionada = self.tree_lista_reco.item(recomendacion_seleccionada, 'values')

        if not valor_recomendacion_seleccionada:
            messagebox.showwarning("Advertencia", "Ninguna recomendación seleccionada")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta recomendación?")
        if respuesta:
            try:
                conn = sqlite3.connect(self.DB_PATH)
                cursor = conn.cursor()
                
                id_recomendacion = valor_recomendacion_seleccionada[0]
                
                cursor.execute("DELETE FROM Recomendaciones WHERE Id=?", (id_recomendacion,))
                conn.commit()
                
                messagebox.showinfo("Éxito", "Recomendación eliminada correctamente")
                self.buscar_reco('')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la recomendación: {str(e)}")
            finally:
                if 'conn' in locals():
                    conn.close()

    def buscar_reco(self, event):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        registro = self.tree_lista_reco.get_children()
        for elementos in registro:
            self.tree_lista_reco.delete(elementos)

        cursor.execute("SELECT * FROM Recomendaciones WHERE Mensaje LIKE ? ORDER BY Fecha DESC", 
                      (f"%{self.ent_buscar_lista_reco.get()}%",))
        datos_reco = cursor.fetchall()
        
        for fila in datos_reco:
            fecha_sin_hora = fila[2].split()[0] if fila[2] else ""
            self.tree_lista_reco.insert('', 0, fila[0], values=(fila[0], fila[1], fecha_sin_hora, fila[3]))

        conn.commit()
        cursor.close()
        conn.close()
        
# Entrenar apartado
    def entrenar_bot(self):
        self.ventana_entrenamiento = Toplevel(self)
        self.ventana_entrenamiento.title("Entrenando Bot")
        self.ventana_entrenamiento.geometry("300x100")
        self.ventana_entrenamiento.resizable(False, False)
        self.ventana_entrenamiento.overrideredirect(True)
        self.centrar_ventana_emergente(self.ventana_entrenamiento)
        self.ventana_entrenamiento.grab_set()

        self.progress = ttk.Progressbar(self.ventana_entrenamiento, orient="horizontal", length=250, mode="indeterminate")
        self.progress.pack(pady=20)
        self.progress.start(10)
        
        self.label_estado = Label(self.ventana_entrenamiento, text="Entrenando Bot...")
        self.label_estado.pack()
        
        def ejecutar_entrenamiento():
          try:
            for i in range(100):
                time.sleep(0.05)  # tiempo de entrenamiento simulado
                self.progress['value'] += 1
                self.ventana_entrenamiento.update_idletasks()
                
            if entrenar.entrenamiento():
                self.ventana_entrenamiento.destroy()
                messagebox.showinfo("Éxito", "Entrenamiento Completado con Éxito.")
          except IndexError as e:
              self.ventana_entrenamiento.destroy()
              messagebox.showerror("Error", str(e))
          except Exception as e:
              self.ventana_entrenamiento.destroy()
              messagebox.showerror("Error", str(e))
        
        threading.Thread(target=ejecutar_entrenamiento).start()
        
# Ejecutar bot
    def ejecutar_bot(self):
        confirmacion = messagebox.askyesno("Confirmar", "¿Esta seguro de ejecutar el bot? Se cerrará la sesión actual")
        if not confirmacion:
            return
          
        self.withdraw()
        self.proceso_bot = subprocess.Popen(["python", "app.py"])
        self.ventana_control = Toplevel()
        self.ventana_control.title("Control del Bot")
        self.ventana_control.geometry("350x150")
        self.ventana_control.resizable(False, False)
        self.centrar_ventana_emergente(self.ventana_control)
        self.ventana_control.overrideredirect(True)
        
        ruta_icono = os.path.join("static", "images", "Admin.ico")
        if os.path.exists(ruta_icono):
            self.ventana_control.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el archivo de icono en {ruta_icono}")
        
        ruta_bot = "http://localhost"
        lbl_ruta = Label(self.ventana_control, text=f"Bot ejecutándose en: {ruta_bot}", fg="blue", cursor="hand2")
        lbl_ruta.pack(pady=25)
        lbl_ruta.bind("<Button-1>", lambda e: webbrowser.open(ruta_bot))
        
        """ruta_bot = "http://127.0.0.1:5731"
        lbl_ruta = Label(self.ventana_control, text=f"Bot ejecutándose en: {ruta_bot}", fg="blue", cursor="hand2")
        lbl_ruta.pack(pady=8)
        lbl_ruta.bind("<Button-1>", lambda e: webbrowser.open(ruta_bot))
        
        ruta_bot2 = "http://192.168.31.88:5731"
        lbl_ruta2 = Label(self.ventana_control, text=f"Tambien puede probar con: {ruta_bot2}", fg="blue", cursor="hand2")
        lbl_ruta2.pack(pady=20)
        lbl_ruta2.bind("<Button-1>", lambda e: webbrowser.open(ruta_bot))"""
        
        btn_detener = tb.Button(self.ventana_control, text="Detener Bot", width=15, bootstyle="danger", command=self.detener_bot)
        btn_detener.pack(pady=20)
        
    def detener_bot(self):
        if hasattr(self, 'proceso_bot') and self.proceso_bot:
            try:
                self.proceso_bot.terminate()
                self.proceso_bot.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proceso_bot.kill()
                self.proceso_bot.wait()
            finally:
                self.proceso_bot = None
                
        self.ventana_control.destroy()
        self.quit()
            
    def centrar_ventana_emergente(self, ventana):
        ventana.update_idletasks()
        
        ancho_ventana = ventana.winfo_width()
        alto_ventana = ventana.winfo_height()
        
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        
        x = (pantalla_ancho // 2) - (ancho_ventana // 2)
        y = (pantalla_alto // 2) - (alto_ventana // 2)
        ventana.geometry(f"+{x}+{y}")
            
def main():
    app = Ventana()
    app.title('Sistema de Administrador')
    tb.Style('superhero')
    app.mainloop()
    
if __name__ == '__main__':
    main()