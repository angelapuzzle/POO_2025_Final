# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3

class Participantes:
    # nombre de la base de datos  y ruta 
    path = r'Resources'
    db_name = path + r'/Participantes.db'
    program_icon = path + r'/ico_registro.ico'
    actualiza = None
    def __init__(self, master=None):
        # Top Level - Ventana Principal
        self.win = tk.Tk() if master is None else tk.Toplevel()
        
             
        #Top Level - Configuración
        self.win.configure(background="#d9f0f9", height="480", relief="flat", width="1024")
        self.win.geometry("1024x480")
        self.win.iconbitmap(self.program_icon)
        self.win.resizable(False, False)
        self.win.title("Conferencia MACSS y la Ingeniería de Requerimientos")
        self.win.pack_propagate(0) 
        
        # Main widget
        self.mainwindow = self.win
        
        #Label Frame
        self.lblfrm_Datos = tk.LabelFrame(self.win, labelanchor="n", font=("Helvetica",13,"bold"))
        
        self.lblfrm_Datos.configure(height="370", relief="groove", text=" Inscripción ", width="280")
        self.lblfrm_Datos.place(anchor="nw", relx="0.01", rely="0.04", x="0", y="0")
        self.lblfrm_Datos.grid_propagate(0)
        
        #Label Id
        self.lblId = ttk.Label(self.lblfrm_Datos)
        self.lblId.configure(anchor="e", font="TkTextFont", justify="left", text="Identificación")
        self.lblId.configure(width="12")
        self.lblId.grid(column="0", padx="5", pady="15", row="0", sticky="w")
        
        ### En lugar de hacer un bind, se crea un StringVar el cual ejecute la función de validación al cambiar su contenido
        ### y este StringVar se asocia con el Entry
        #Entry Id
        self.entryIdText = tk.StringVar()
        self.entryIdText.trace_add('write', self.valida_Identificacion_Callback)
        self.entryId = tk.Entry(self.lblfrm_Datos, textvariable=self.entryIdText)
        self.entryId.configure(exportselection="false", justify="left", relief="groove", takefocus=True, width="30")
        self.entryId.grid(column="1", row="0", sticky="w")
        
        
        #Label Nombre
        self.lblNombre = ttk.Label(self.lblfrm_Datos)
        self.lblNombre.configure(anchor="e", font="TkTextFont", justify="left", text="Nombre")
        self.lblNombre.configure(width="12")
        self.lblNombre.grid(column="0", padx="5", pady="15", row="1", sticky="w")
        
        
        #Entry Nombre
        self.entryNombreText = tk.StringVar()
        self.entryNombre = tk.Entry(self.lblfrm_Datos, textvariable=self.entryNombreText)
        self.entryNombre.configure(exportselection="false", justify="left",relief="groove", takefocus=True, width="30")
        self.entryNombre.grid(column="1", row="1", sticky="w")
        
        #Label Ciudad
        self.lblCiudad = ttk.Label(self.lblfrm_Datos)
        self.lblCiudad.configure(anchor="e", font="TkTextFont", justify="left", text="Ciudad")
        self.lblCiudad.configure(width="12")
        self.lblCiudad.grid(column="0", padx="5", pady="15", row="2", sticky="w")
        
        
        #Entry Ciudad
        self.entryCiudadText = tk.StringVar()
        self.entryCiudad = tk.Entry(self.lblfrm_Datos, textvariable=self.entryCiudadText)
        self.entryCiudad.configure(exportselection="false", justify="left",relief="groove", takefocus=True, width="30")
        self.entryCiudad.grid(column="1", row="2", sticky="w")
        
        
        #Label Direccion
        self.lblDireccion = ttk.Label(self.lblfrm_Datos)
        self.lblDireccion.configure(anchor="e", font="TkTextFont", justify="left", text="Dirección")
        self.lblDireccion.configure(width="12")
        self.lblDireccion.grid(column="0", padx="5", pady="15", row="3", sticky="w")
        
        #Entry Direccion
        self.entryDireccionText = tk.StringVar()
        self.entryDireccion = tk.Entry(self.lblfrm_Datos, textvariable=self.entryDireccionText)
        self.entryDireccion.configure(exportselection="false", justify="left", relief="groove", takefocus=True, width="30")
        self.entryDireccion.grid(column="1", row="3", sticky="w")
        
        #Label Celular
        self.lblCelular = ttk.Label(self.lblfrm_Datos)
        self.lblCelular.configure(anchor="e", font="TkTextFont", justify="left", text="Celular")
        self.lblCelular.configure(width="12")
        self.lblCelular.grid(column="0", padx="5", pady="15", row="4", sticky="w")
        
        #Entry Celular
        self.entryCelularText = tk.StringVar()
        self.entryCelular = tk.Entry(self.lblfrm_Datos, textvariable=self.entryCelularText)
        self.entryCelular.configure(exportselection="false", justify="left", relief="groove", takefocus=True, width="30")
        self.entryCelular.grid(column="1", row="4", sticky="w")
        
        #Label Entidad
        self.lblEntidad = ttk.Label(self.lblfrm_Datos)
        self.lblEntidad.configure(anchor="e", font="TkTextFont", justify="left", text="Entidad")
        self.lblEntidad.configure(width="12")
        self.lblEntidad.grid(column="0", padx="5", pady="15", row="5", sticky="w")
        
        #Entry Entidad
        self.entryEntidadText = tk.StringVar()
        self.entryEntidad = tk.Entry(self.lblfrm_Datos, textvariable=self.entryEntidadText)
        self.entryEntidad.configure(exportselection="false", justify="left", relief="groove", takefocus=True, width="30")
        self.entryEntidad.grid(column="1", row="5", sticky="w")
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.lblfrm_Datos)
        self.lblFecha.configure(anchor="e", font="TkTextFont", justify="left", text="Fecha")
        self.lblFecha.configure(width="12")
        self.lblFecha.grid(column="0", padx="5", pady="15", row="6", sticky="w")
        
        #Entry Fecha
        self.entryFechaText = tk.StringVar()
        self.entryFecha = tk.Entry(self.lblfrm_Datos, textvariable=self.entryFechaText)
        self.entryFecha.configure(exportselection="false", justify="left", relief="groove", takefocus=True, width="30")
        self.entryFecha.grid(column="1", row="6", sticky="w")
        self.entryFecha.bind("<Key>", self.valida_Fecha)
        
        
        #Botón Grabar
        self.btnGrabar = ttk.Button(self.win)
        self.btnGrabar.configure(state="normal", text="Grabar", width="9")
        self.btnGrabar.place(anchor="nw", relx="0.01", rely="0.83", x="0", y="0")
        self.btnGrabar.bind("<1>", self.adiciona_Registro)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.win)        
        self.btnEditar.configure(text="Editar", width="9")
        self.btnEditar.place(anchor="nw", relx="0.01", rely="0.83", x="80", y="0")
        self.btnEditar.bind("<1>", self.edita_tablaTreeView) #REVISAR CADA UNA DE LAS FUNCIONES
        
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.win)
        self.btnEliminar.configure(text="Eliminar", width="9")
        self.btnEliminar.place(anchor="nw", relx="0.01", rely="0.83", x="152", y="0")
        self.btnEliminar.bind("<1>", self.elimina_Registro)
        
        #Botón Cancelar/Daniel
        self.btnCancelar = ttk.Button(self.win)
        self.btnCancelar.configure(text='Cancelar', width='9',command = self.limpia_Campos)
        self.btnCancelar.place(anchor='nw', relx="0.01", rely='0.83', x='225', y='0')
        
        #Botón Consultar
        self.btnConsultar = ttk.Button(self.win)
        self.btnConsultar.configure(text='Consultar', width='9') #,command = self.limpia_Campos
        self.btnConsultar.place(anchor='nw', relx="0.01", rely='0.83', x='115', y='29')
        #Agregar bind, 1 y la función
        
        
        #tablaTreeView
        self.style=ttk.Style()
        self.style.configure('estilo.Treeview', highlightthickness=0, bd=0, background='AliceBlue', font=('Calibri Light',10))
        self.style.configure('estilo.Treeview.Heading', background='Azure', font=('Calibri Light', 10,'bold')) 
        self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])

        self.treeDatos = ttk.Treeview(self.win, height = 10, style="estilo.Treeview")
        #self.treeDatos.place(x=380, y=10, height=340, width = 500) #REVISAR ESTO
        self.treeDatos.place(anchor="nw", height="400", rely="0.04", width="700", x="300", y="0")

       # Etiquetas de las columnas
        self.treeDatos["columns"]=("Nombre","Ciudad","Dirección","Celular","Entidad","Fecha")
        # Determina el espacio a mostrar que ocupa el código
        self.treeDatos.column('#0',         stretch="true", width=15) # #0 se refiere a que es la primera columna y no se puede cambiar.
        self.treeDatos.column('Nombre',     stretch="true",             width=60)
        self.treeDatos.column('Ciudad',      stretch="true",             width=12)#Revisar widths
        self.treeDatos.column('Dirección',  stretch="true",             width=60)
        self.treeDatos.column('Celular',    stretch="true",             width=16)
        self.treeDatos.column('Entidad',    stretch="true",             width=60)
        self.treeDatos.column('Fecha',      stretch="true",             width=12)
        

       #Encabezados de las columnas de la pantalla
        self.treeDatos.heading('#0',       text = 'Id')
        self.treeDatos.heading('Nombre',   text = 'Nombre')
        self.treeDatos.heading('Ciudad',   text = 'Ciudad')
        self.treeDatos.heading('Dirección',text = 'Dirección')
        self.treeDatos.heading('Celular',  text = 'Celular')
        self.treeDatos.heading('Entidad',  text = 'Entidad')
        self.treeDatos.heading('Fecha',    text = 'Fecha')

        #Scrollbar en el eje Y de treeDatos
        self.scrollbar=ttk.Scrollbar(self.win, orient='vertical', command=self.treeDatos.yview)
        self.treeDatos.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=1000, y=50, height=400)

        #Carga los datos en treeDatos
        self.lee_tablaTreeView()

    def valida(self):
        '''Valida que el Id no esté vacio, devuelve True si ok'''
        return (len(self.entryId.get()) != 0 )   

    def run(self):
        self.mainwindow.mainloop()

    def valida_Identificacion_Callback(self, var, index, mode):
        text = self.entryIdText.get()

        #Crea una copia filtrada del texto para solo mantener los carácteres númericos
        filtered_text = ""
        for char in text:
            if char in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
                filtered_text += char

        #Si el texto supera los 15 carácteres mostrar un mensaje
        if len(filtered_text) > 15:
            #Pone el Entry directamente en blanco temporalmente, para ocultar errores gráficos
            self.entryId.delete(0, "end")
            mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')

        #Pone en la StringVar el texto filtrado recortado a los primeros 15 caracteres
        self.entryIdText.set(filtered_text[0:15])

    def valida_Fecha(self, event=None):
      pass
    
    '''Función utilizada para el boón editar, trae desde el treeview el participante seleccionado
        y lo carga en los entry '''
    def carga_Datos(self): 
        ''' Carga los datos en los campos desde el treeView'''
        #   Nuevo
        self.entryIdText.set(self.treeDatos.item(self.treeDatos.selection())['text']) #Aca, todo lo que habia se reemplaza por el texto nuevom si coloco insert, se acumulan
        self.entryId.configure(state = 'readonly')#Deja id bloqueado para que no lo puedan editar
        #Carga los demás entrys
        self.entryNombreText.set(self.treeDatos.item(self.treeDatos.selection())['values'][0])
        self.entryCiudadText.set(self.treeDatos.item(self.treeDatos.selection())['values'][1])
        self.entryDireccionText.set(self.treeDatos.item(self.treeDatos.selection())['values'][2])
        self.entryCelularText.set(self.treeDatos.item(self.treeDatos.selection())['values'][3])
        self.entryEntidadText.set(self.treeDatos.item(self.treeDatos.selection())['values'][4])
        self.entryFechaText.set(self.treeDatos.item(self.treeDatos.selection())['values'][5])
        

    def limpia_Campos(self):
        # Limpia todas las entradas
        self.entryId.configure(state='normal')  # Aseguramos que se pueda editar antes de limpiar
        self.entryId.delete(0, 'end')
        self.entryNombre.delete(0, 'end')
        self.entryDireccion.delete(0, 'end')
        self.entryCelular.delete(0, 'end')
        self.entryEntidad.delete(0, 'end')
        self.entryFecha.delete(0, 'end')
    


    def run_Query(self, query, parametros = ()):
        ''' Función para ejecutar los Querys a la base de datos ''' #Query es una indicación que le digo a sql
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result

    def lee_tablaTreeView(self):
        ''' Carga los datos de la BD y Limpia la Tabla tablaTreeView '''
        tabla_TreeView = self.treeDatos.get_children()
        for linea in tabla_TreeView:
            self.treeDatos.delete(linea)
        # Seleccionando los datos de la BD
        query = 'SELECT * FROM t_participantes ORDER BY Id DESC'
        db_rows = self.run_Query(query)
        # Insertando los datos de la BD en la tabla de la pantalla
        for row in db_rows:
            self.treeDatos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
        
    def adiciona_Registro(self, event=None):
        '''Adiciona un producto a la BD si la validación es True'''
        if self.actualiza:
            self.actualiza = None #REVISION
            self.entryId.configure(state = 'readonly')
            query = 'UPDATE t_participantes SET Nombre = ?, Ciudad = ?, Direccion = ?, Celular = ?, Entidad = ?, Fecha = ? WHERE Id = ?'
            parametros = (self.entryNombre.get(), self.entryCiudad.get(), self.entryDireccion.get(),
                        self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get(),
                            self.entryId.get())
            self.run_Query(query, parametros)
            mssg.showinfo('Ok',f' Registro actualizado con éxito')
        else:
            query = 'INSERT INTO t_participantes VALUES(?, ?, ?, ?, ?, ?, ?)'
            parametros = (self.entryId.get(),self.entryNombre.get(), self.entryCiudad.get(), self.entryDireccion.get(),
                          self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get())
            if self.valida():
                self.run_Query(query, parametros)
                self.limpia_Campos()
                mssg.showinfo('',f'Registro: {self.entryId.get()} .. agregado')
            else:
                mssg.showerror("¡ Atención !","No puede dejar la identificación vacía")
        self.limpia_Campos()
        self.lee_tablaTreeView()

    def edita_tablaTreeView(self, event=None):
        try:
            # Carga los campos desde la tabla TreeView
            self.treeDatos.item(self.treeDatos.selection())['text']
            self.limpia_Campos()
            self.actualiza = True # Esta variable controla la actualización
            self.carga_Datos()
        except IndexError as error:
            self.actualiza = None
            mssg.showerror("¡ Atención !",'Por favor seleccione un ítem de la tabla')
            return
        
    def elimina_Registro(self, event=None):
        query = ('DELETE FROM t_participantes WHERE Id = ?')
        parametros = (self.entryId.get(), )
        self.run_Query(query, parametros)
        mssg.showinfo( 'Eliminado', f'El registro fue eliminado')
        self.lee_tablaTreeView() #REVISAR



if __name__ == "__main__":
    app = Participantes()
    app.run() 
