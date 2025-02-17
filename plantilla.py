# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from datetime import date, datetime

class Participantes:
    # nombre de la base de datos y ruta 
    path = r'Resources'
    db_name = path + r'/Participantes.db'
    program_icon = path + r'/ico_registro.ico'
    actualiza = None

    
    color_palette = {
        'window_bg': '#EFF1F5',
        'lblfrm_datos': '#E6E9EF',
        'entry': '#EFF1F5',
        'tabla_encabezado': '#7287FD',
        'tabla_fondo': '#E6E9EF'
    }

    # Variables usadas para guardar información digitada por el usuario
    cod_departamento = None
    cod_ciudad = None
    sel_fecha = None #si hay una fecha seleccionada esto será un objeto date

    def __init__(self, master=None):
        # Top Level - Ventana Principal
        self.win = tk.Tk() if master is None else tk.Toplevel()
        
             
        #Top Level - Configuración
        self.win.configure(background=self.color_palette['window_bg'], height='480', relief='flat', width='1024')
        self.win.geometry('1024x480')
        self.win.iconbitmap(self.program_icon)
        self.win.resizable(False, False)
        self.win.title('Conferencia MACSS y la Ingeniería de Requerimientos')
        self.win.pack_propagate(0) 

        self.win.tk.call("source", self.path + "/azure.tcl")
        self.win.tk.call("set_theme", "light")

        self.styleApp = ttk.Style()

        self.styleApp.configure(
            'main.TButton',
            background=self.color_palette['window_bg'],
        )

        self.styleApp.configure(
            'lblfrm_Datos.TLabel',
            background=self.color_palette['lblfrm_datos'],
            anchor='e',
            #font='TkTextFont',
            justify='left',
            font=('Calibri', 9)
        )
        self.styleApp.configure(
            'lblfrm_Datos.TButton',
            background=self.color_palette['lblfrm_datos'],
            
        )


        
        
        #Label Frame
        self.lblfrm_Datos = tk.LabelFrame(self.win, labelanchor='n', font=('Helvetica',13,'bold'))
        self.lblfrm_Datos.configure(background=self.color_palette['lblfrm_datos'], relief='groove')
        self.lblfrm_Datos.configure(height='370', width='280', text=' Inscripción ')
        self.lblfrm_Datos.place(anchor='nw', relx='0.01', rely='0.04', x='0', y='0')
        self.lblfrm_Datos.grid_propagate(0)
        for i in range(7):
            self.lblfrm_Datos.rowconfigure(i, weight = 1)

        # Como el Entry de ttk se ve raro, y el de tk no tiene la opción de usar estilos,
        # esto permite configurar los entry con las mismas opciones siempte
        config_entry_Datos = {
            'background': self.color_palette['entry'],
            'exportselection': 'false',
            'justify': 'left',
            'relief': 'groove',
            'takefocus': True
            }
        
        #Label Id
        self.lblId = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblId.configure(text='Identificación', width='12')
        self.lblId.grid(column='0', padx='5', row='0', sticky='w')
        
        ### En lugar de hacer un bind, se crea un StringVar el cual ejecute la función de validación al cambiar su contenido
        ### y este StringVar se asocia con el Entry
        #Entry Id
        self.entryIdText = tk.StringVar()
        self.entryIdText.trace_add('write', self.valida_Identificacion)
        self.entryId = tk.Entry(self.lblfrm_Datos, textvariable=self.entryIdText)
        self.entryId.configure(config_entry_Datos)
        self.entryId.configure(width=30)
        self.entryId.grid(column='1', row='0', sticky='w')
        
        
        #Label Nombre
        self.lblNombre = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblNombre.configure(text='Nombre', width='12')
        self.lblNombre.grid(column='0', padx='5', row='1', sticky='w')
        
        
        #Entry Nombre
        self.entryNombreText = tk.StringVar()
        self.entryNombre = tk.Entry(self.lblfrm_Datos, textvariable=self.entryNombreText)
        self.entryNombre.configure(config_entry_Datos)
        self.entryNombre.configure(width=30)
        self.entryNombre.grid(column='1', row='1', sticky='w')
        
        #Label Ciudad
        self.lblCiudad = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblCiudad.configure(text='Ciudad', width='12')
        self.lblCiudad.grid(column='0', padx='5', row='2', sticky='w')

        #Frame Entry Ciudad (background coincide con lblfrmDatos)
        self.frmCiudad = tk.Frame(self.lblfrm_Datos, background=self.color_palette['lblfrm_datos'])
        self.frmCiudad.grid(column='1', row='2', sticky='w')
        
        #Entry Ciudad
        self.entryCiudadText = tk.StringVar()
        self.entryCiudadText.set('[Seleccionar]')
        self.entryCiudad = tk.Entry(self.frmCiudad, textvariable=self.entryCiudadText)
        self.entryCiudad.configure(width=25, state='readonly', readonlybackground=self.color_palette['entry']) # Aunque simulemos que está habilitado, en realidad no lo está
        self.entryCiudad.grid(column='0', row='0', sticky='w')

        # Botón de selección
        self.btnSeleccionarCiudad = ttk.Button(self.frmCiudad, style='lblfrm_Datos.TButton')
        self.btnSeleccionarCiudad.configure(text='...', width=2, command=self.crear_Selector_Ciudad)
        self.btnSeleccionarCiudad.grid(column='1', row='0', padx=5)
        
        #Label Direccion
        self.lblDireccion = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblDireccion.configure(text='Dirección', width='12')
        self.lblDireccion.grid(column='0', padx='5', row='3', sticky='w')
        
        #Entry Direccion
        self.entryDireccionText = tk.StringVar()
        self.entryDireccion = tk.Entry(self.lblfrm_Datos, textvariable=self.entryDireccionText)
        self.entryDireccion.configure(config_entry_Datos)
        self.entryDireccion.configure(width=30)
        self.entryDireccion.grid(column='1', row='3', sticky='w')
        
        #Label Celular
        self.lblCelular = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblCelular.configure(text='Celular', width='12')
        self.lblCelular.grid(column='0', padx='5', row='4', sticky='w')
        
        #Entry Celular
        self.entryCelularText = tk.StringVar()
        self.entryCelular = tk.Entry(self.lblfrm_Datos, textvariable=self.entryCelularText)
        self.entryCelular.configure(config_entry_Datos)
        self.entryCelular.configure(width=30)
        self.entryCelular.grid(column='1', row='4', sticky='w')
        
        #Label Entidad
        self.lblEntidad = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblEntidad.configure(text='Entidad', width='12')
        self.lblEntidad.grid(column='0', padx='5', row='5', sticky='w')
        
        #Entry Entidad
        self.entryEntidadText = tk.StringVar()
        self.entryEntidad = tk.Entry(self.lblfrm_Datos, textvariable=self.entryEntidadText)
        self.entryEntidad.configure(config_entry_Datos)
        self.entryEntidad.configure(width=30)
        self.entryEntidad.grid(column='1', row='5', sticky='w')
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.lblfrm_Datos, style='lblfrm_Datos.TLabel')
        self.lblFecha.configure(text='Fecha', width='12')
        self.lblFecha.grid(column='0', padx='5', row='6', sticky='w')

        #Frame Entry Fecha (background coincide con lblfrmDatos)
        self.frmFecha = tk.Frame(self.lblfrm_Datos, background=self.color_palette['lblfrm_datos'])
        self.frmFecha.grid(column='1', row='6', sticky='w')
        
        #Entry Fecha
        self.entryFechaText = tk.StringVar()
        self.entryFechaText.set('[Seleccionar]')
        self.entryFecha = tk.Entry(self.frmFecha, textvariable=self.entryFechaText)
        self.entryFecha.configure(config_entry_Datos)
        self.entryFecha.configure(width=25)
        self.entryFecha.grid(column='0', row='0', sticky='w')

        # Botón de selección
        self.btnSeleccionarCiudad = ttk.Button(self.frmFecha, style='lblfrm_Datos.TButton')
        self.btnSeleccionarCiudad.configure(text='...', width=2, command=self.crear_Selector_Fecha)
        self.btnSeleccionarCiudad.grid(column='1', row='0', padx=5)
        
        #Frame Botones (background coincide con la ventana)
        self.frmBotones = tk.Frame(self.win, background=self.color_palette['window_bg'])
        self.frmBotones.place(anchor='nw', relx='0.005', rely='0.82', x='0', y='0')
        
        #Botón Grabar
        self.btnGrabar = ttk.Button(self.frmBotones, style='main.TButton')
        self.btnGrabar.configure(text='Grabar', width='9', command=self.adiciona_Registro)
        self.btnGrabar.grid(column='0', row='0', sticky='n', padx='4', pady='4')
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frmBotones, style='main.TButton')        
        self.btnEditar.configure(text='Editar', width='9', command=self.edita_tablaTreeView)
        self.btnEditar.grid(column='1', row='0', sticky='n', padx='4', pady='4')
        
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frmBotones, style='main.TButton')
        self.btnEliminar.configure(text='Eliminar', width='9', command=self.elimina_Registro)
        self.btnEliminar.grid(column='2', row='0', sticky='n', padx='4', pady='4')
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frmBotones, style='main.TButton')
        self.btnCancelar.configure(text='Cancelar', width='9', command=self.limpia_Campos)
        self.btnCancelar.grid(column='3', row='0', sticky='n', padx='4', pady='4')
        
        #Botón Consultar
        self.btnConsultar = ttk.Button(self.frmBotones, style='main.TButton')
        self.btnConsultar.configure(text='Consultar', width='9') #command = Función
        self.btnConsultar.grid(column='1', columnspan=2, row='1', sticky='n', padx='4', pady='4')
        
        
        #tablaTreeView
        self.style=ttk.Style()
        self.style.configure('estilo.Treeview', highlightthickness=0, bd=0, background=self.color_palette['tabla_fondo'], font=('Calibri Light',10))
        self.style.configure('estilo.Treeview.Heading', background=self.color_palette['tabla_encabezado'], font=('Calibri Light', 10,'bold')) 
        self.style.layout('estilo.Treeview', [('estilo.Treeview.treearea', {'sticky': 'nswe'})])

        self.treeDatos = ttk.Treeview(self.win, style='estilo.Treeview')
        self.treeDatos.place(anchor='nw', height='400', rely='0.04', width='700', x='300', y='0')

       # Etiquetas de las columnas
        self.treeDatos['columns']=('Nombre','Ciudad','Dirección','Celular','Entidad','Fecha')
        # Determina el espacio a mostrar que ocupa el código
        self.treeDatos.column('#0',         stretch='true',             width=15) # #0 se refiere a que es la primera columna y no se puede cambiar.
        self.treeDatos.column('Nombre',     stretch='true',             width=60)
        self.treeDatos.column('Ciudad',     stretch='true',             width=12) #Revisar widths
        self.treeDatos.column('Dirección',  stretch='true',             width=60)
        self.treeDatos.column('Celular',    stretch='true',             width=16)
        self.treeDatos.column('Entidad',    stretch='true',             width=60)
        self.treeDatos.column('Fecha',      stretch='true',             width=12)
        

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
        self.scrollbar.place(x=1000, rely='0.04', height=400)

        #Carga los datos en treeDatos
        self.lee_tablaTreeView()


    def run(self):
        self.win.mainloop()

    def reset_cursor(self, entry, index):
        entry.icursor(index)

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
        # Seleccionando los datos de la BD, esta query usa un join para obtener el nombre de la ciudad a partir del código guardado en esta
        query = 'SELECT Id, Nombre, Nombre_Ciudad, Direccion, Celular, Entidad, Fecha FROM t_participantes LEFT JOIN t_ciudades ON t_ciudades.Id_Ciudad = t_participantes.Id_Ciudad ORDER BY Id DESC'
        db_rows = self.run_Query(query)
        # Insertando los datos de la BD en la tabla de la pantalla
        for row in db_rows:
            ciudad = row[2]
            if ciudad is None:
                ciudad = ''
            fecha = row[6]
            if fecha is None:
                fecha = ''
            else:
                try:
                    # Si hay una fecha valida la convierte a DD/MM/AAAA
                    fecha = datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
                except ValueError:
                    # Si hay una fecha invalida pone el texto como 'Invalida'abs
                    fecha = 'Invalida'
            self.treeDatos.insert('',0, text = row[0], values = [row[1],ciudad,row[3],row[4],row[5],fecha])

    def valida_Grabar(self): #recordemos también borrar espacios para que no ocupe espacios en la memoría y validación celular
        '''Valida que el Id no esté vacio, devuelve True si ok''' #El cambio que hice en la validación es porque tiraba error en la terminal cuando se escribía un id en el entry que ya existía
        if (len(self.entryId.get()) == 0 ):
            return False
        else:
            tabla_TreeView = self.treeDatos.get_children()
            for linea in tabla_TreeView:
                if (int(self.entryId.get())) == self.treeDatos.item(linea)['text']:
                    return False
            return True


            

    def valida_Identificacion(self, var, index, mode):
        text = self.entryIdText.get()

        #Crea una copia filtrada del texto para solo mantener los carácteres númericos
        filtered_text = ''
        for char in text:
            if char in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
                filtered_text += char

        #Si el texto supera los 15 carácteres mostrar un mensaje
        if len(filtered_text) > 15:
            self.win.after(1, mssg.showerror, 'Atención!!','.. ¡Máximo 15 caracteres! ..')

        #Pone en la StringVar el texto filtrado recortado a los primeros 15 caracteres
        self.entryIdText.set(filtered_text[0:15])

    
    '''Función utilizada para el boón editar, trae desde el treeview el participante seleccionado
        y lo carga en los entry '''
    def carga_Datos(self): 
        ''' Carga los datos en los campos desde el treeView'''
        #   Nuevo
        self.entryIdText.set(self.treeDatos.item(self.treeDatos.selection())['text']) #Aca, todo lo que habia se reemplaza por el texto nuevom si coloco insert, se acumulan
        self.entryId.configure(state = 'readonly')#Deja id bloqueado para que no lo puedan editar
        #Carga los demás entries (para ciudad esto es meramente el texto mostrado)
        self.entryNombreText.set(self.treeDatos.item(self.treeDatos.selection())['values'][0])
        self.entryCiudadText.set(self.treeDatos.item(self.treeDatos.selection())['values'][1])
        self.entryDireccionText.set(self.treeDatos.item(self.treeDatos.selection())['values'][2])
        self.entryCelularText.set(self.treeDatos.item(self.treeDatos.selection())['values'][3])
        self.entryEntidadText.set(self.treeDatos.item(self.treeDatos.selection())['values'][4])

        # Carga los códigos del departamento y de la ciudad
        query = 'SELECT Id_Departamento, Id_Ciudad FROM t_participantes WHERE Id = ?'
        parametros = (self.treeDatos.item(self.treeDatos.selection())['text'],)
        codigos = self.run_Query(query, parametros).fetchone()
        self.cod_departamento = codigos[0]
        self.cod_ciudad = codigos[1]

        # Si la ciudad no está definida, dejar el campo "vacio"
        if self.cod_ciudad is None:
            self.entryCiudadText.set('[Seleccionar]')

        # Carga la fecha si no está vacia
        text_fecha = self.treeDatos.item(self.treeDatos.selection())['values'][5]
        try:
            # Si hay una fecha valida, la guarda en self.fecha y pone el texto del entry en la fecha correspondiente (recordar que en el treeview ya está en DD/MM/AAAA)
            self.sel_fecha = datetime.strptime(text_fecha, '%d/%m/%Y').date()
            self.entryFechaText.set(text_fecha)
        except ValueError:
            # Sino, pone el campo "vacio"
            self.fecha = None
            self.entryFechaText.set('[Seleccionar]')

        

    def limpia_Campos(self):
        # Limpia todas las entradas
        self.entryId.configure(state='normal')  # Aseguramos que se pueda editar antes de limpiar
        self.entryIdText.set('')
        self.entryNombreText.set('')
        self.entryCiudadText.set('[Seleccionar]')
        self.entryDireccionText.set('')
        self.entryCelularText.set('')
        self.entryEntidadText.set('')
        self.entryFechaText.set('[Seleccionar]')
        self.cod_departamento = None
        self.cod_ciudad = None
        self.sel_fecha = None
    

    def get_Departamentos(self):
        query = 'SELECT DISTINCT Nombre_Departamento FROM t_ciudades ORDER BY Nombre_Departamento'
        return [row[0] for row in self.run_Query(query)]

    def get_Ciudades_Por_Departamento(self, departamento):
        query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Nombre_Departamento = ? ORDER BY Nombre_Ciudad'
        parametros = (departamento,)
        return [row[0] for row in self.run_Query(query, parametros)]
        
    def crear_Selector_Ciudad(self):
        pre_cod_departamento = None
        pre_cod_departamento_text = None
        pre_cod_ciudad = None
        pre_cod_ciudad_text = None

        ventana = tk.Toplevel(self.win)
        ventana.title('Seleccionar Ciudad')
        ventana.geometry('420x320')
        ventana.transient(self.win) #Indica que la ventana depende de la principal

        #Label mostrando la selección actual
        lblSeleccion = ttk.Label(ventana, anchor='center', text='Ciudad seleccionada: ')
        lblSeleccion.pack(side='top', fill='x', padx=5, pady=5)
        
        #Frame para departamentos
        frmDepartamentos = ttk.Frame(ventana)
        frmDepartamentos.pack(side='left', fill='y', padx=5, pady=5)

        ttk.Label(frmDepartamentos, text='Departamentos').pack()
        listboxDepartamentos = tk.Listbox(frmDepartamentos, width=25)
        listboxDepartamentos.pack(fill='y', expand=True)

        # Frame para ciudades
        frmCiudades = ttk.Frame(ventana)
        frmCiudades.pack(side='right', fill='both', expand=True, padx=5, pady=5)
    
        ttk.Label(frmCiudades, text='Ciudades').pack()
        listboxCiudades = tk.Listbox(frmCiudades)
        listboxCiudades.pack(fill='both', expand=True)

        # Botón Cancelar
        btnCancelar = ttk.Button(ventana, text='Cancelar')
        btnCancelar.pack(side='bottom', pady=5)
        # Botón Seleccionar
        btnSeleccionar = ttk.Button(ventana, text='Seleccionar', state='disabled')
        btnSeleccionar.pack(side='bottom', pady=5)
    
    
        def cargar_Lista_Departamentos(seleccion_departamento = None):
            departamentos = self.get_Departamentos()
            for departamento in departamentos:
                listboxDepartamentos.insert('end', departamento)
            if seleccion_departamento is not None:
                index_departamento = departamentos.index(seleccion_departamento)
                listboxDepartamentos.focus_set()
                listboxDepartamentos.see(index_departamento)
                listboxDepartamentos.activate(index_departamento)

        def cargar_Lista_Ciudades(departamento, seleccion_ciudad = None):
            ciudades = self.get_Ciudades_Por_Departamento(departamento)
            listboxCiudades.delete(0, 'end')
            for ciudad in ciudades:
                listboxCiudades.insert('end', ciudad)
            if seleccion_ciudad is not None:
                index_ciudad = ciudades.index(seleccion_ciudad)
                listboxCiudades.focus_set()
                listboxCiudades.see(index_ciudad)
                listboxCiudades.activate(index_ciudad)

        # Si ya hay una ciudad seleccionada precargar todo, sino solo cargar la lista de departamentos sin tener ninguno seleccionado
        if self.cod_departamento is not None:
            pre_cod_departamento = self.cod_departamento
            pre_cod_ciudad = self.cod_ciudad

            query = 'SELECT DISTINCT Nombre_Departamento FROM t_ciudades WHERE Id_Departamento = ?'
            parametros = (self.cod_departamento, )
            departamento = self.run_Query(query, parametros).fetchone()[0]
            cargar_Lista_Departamentos(departamento)

            query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Id_Ciudad = ?'
            parametros = (self.cod_ciudad, )
            ciudad = self.run_Query(query, parametros).fetchone()[0]
            cargar_Lista_Ciudades(departamento, ciudad)

            pre_cod_departamento_text = departamento
            pre_cod_ciudad_text = ciudad

            lblSeleccion.configure(text='Ciudad seleccionada: ' + ciudad + ', ' + departamento)
        else:
            cargar_Lista_Departamentos()
            
    
        def seleccionar_Departamento(event):
            # permite modificar las variables definidas en crear_Selector_Ciudad
            nonlocal pre_cod_departamento, pre_cod_departamento_text, pre_cod_ciudad, pre_cod_ciudad_text
            seleccion_departamento = listboxDepartamentos.curselection()
            if seleccion_departamento:
                # Si se selecciona otro departamento se deselecciona la ciudad
                pre_cod_ciudad = None
                pre_cod_ciudad_text = None
                btnSeleccionar.configure(state='disabled')
                lblSeleccion.configure(text='Ciudad seleccionada: ')

                departamento = listboxDepartamentos.get(seleccion_departamento[0])

                query = 'SELECT DISTINCT Id_Departamento FROM t_ciudades WHERE Nombre_Departamento LIKE ?'
                parametros = (departamento, )
                pre_cod_departamento = self.run_Query(query, parametros).fetchone()[0]
                pre_cod_departamento_text = departamento

                cargar_Lista_Ciudades(departamento)

                
    
        def seleccionar_Ciudad(event):
            nonlocal pre_cod_ciudad, pre_cod_ciudad_text
            seleccion_ciudad = listboxCiudades.curselection()

            if seleccion_ciudad:
                ciudad = listboxCiudades.get(seleccion_ciudad[0])

                query = 'SELECT Id_Ciudad FROM t_ciudades WHERE Id_Departamento = ? AND Nombre_Ciudad LIKE ?'
                parametros = (pre_cod_departamento, ciudad)
                pre_cod_ciudad = self.run_Query(query, parametros).fetchone()[0]
                pre_cod_ciudad_text = ciudad

                btnSeleccionar.configure(state='normal')
                lblSeleccion.configure(text='Ciudad seleccionada: ' + pre_cod_ciudad_text + ', ' + pre_cod_departamento_text)
        
        def confirmar_Seleccion(event = None):
            if pre_cod_departamento is not None and pre_cod_ciudad is not None:
                self.entryCiudadText.set(pre_cod_ciudad_text)
                self.cod_ciudad = pre_cod_ciudad
                self.cod_departamento = pre_cod_departamento
                ventana.destroy()
    
        listboxDepartamentos.bind('<<ListboxSelect>>', seleccionar_Departamento)
        listboxCiudades.bind('<<ListboxSelect>>', seleccionar_Ciudad)
        listboxCiudades.bind('<Double-Button-1>', confirmar_Seleccion)

        btnCancelar.configure(command=ventana.destroy)
        btnSeleccionar.configure(command=confirmar_Seleccion)

    def num_Dias_Mes(self, anio, mes):
        '''Devuelve la cantidad de dias entre el primer dia del mes y el primer dia del mes siguiente'''
        sig_mes = mes + 1
        sig_anio = anio
        
        if mes == 12:
            sig_mes = 1
            sig_anio = sig_anio + 1

        time_difference = date(sig_anio, sig_mes, 1) - date(anio, mes, 1)
        print(time_difference.days)
        return time_difference.days

    def crear_Selector_Fecha(self):
        current_date = date.today()
        current_day = current_date.day
        current_month = current_date.month
        current_year = current_date.year

        # Colocar por defecto el día actual o el seleccionado
        if self.sel_fecha is not None:
            sel_dia = self.sel_fecha.day
            sel_mes = self.sel_fecha.month
            sel_anio = self.sel_fecha.year
        else:
            sel_dia = current_day
            sel_mes = current_month
            sel_anio = current_year

        ventana = tk.Toplevel(self.win)
        ventana.title('Seleccionar Fecha')
        ventana.transient(self.win)

        lblSeleccion = ttk.Label(ventana, anchor='center', text='Seleccione una fecha')
        lblSeleccion.pack(side='top', fill='x', padx=5, pady=5)

        frmBotones = tk.Frame(ventana)
        frmBotones.pack(side='bottom', pady=5)

        btnSeleccionar = ttk.Button(frmBotones, text='Seleccionar')
        btnSeleccionar.grid(row=0, column=0, padx=5)

        btnCancelar = ttk.Button(frmBotones, text='Cancelar')
        btnCancelar.grid(row=0, column=1, padx=5)


        # Crear frame con selectores de fecha
        frmFecha = tk.Frame(ventana)
        frmFecha.configure(height=50, pady=5, padx=5)
        frmFecha.pack(side='bottom', anchor='s')

        lblDia = tk.Label(frmFecha, text='Día')
        lblDia.grid(row=0, column=0, padx=5, pady=3)
        comboDia = ttk.Combobox(frmFecha, state='readonly', width=5)
        comboDia.grid(row=1, column=0, pady=5, padx=7)
        

        lblMes = tk.Label(frmFecha, text='Mes')
        lblMes.grid(row=0, column=1, padx=5, pady=3)
        comboMes = ttk.Combobox(frmFecha, state='readonly', width=7)
        comboMes.grid(row=1, column=1, pady=5, padx=7)
        

        lblAnio = tk.Label(frmFecha, text='Año')
        lblAnio.grid(row=0, column=2, padx=5, pady=3)
        comboAnio = ttk.Combobox(frmFecha, state='readonly', width=7)
        comboAnio.grid(row=1, column=2, pady=5, padx=7)
        
        def rellenar_Selectores_Fecha():
            num_dias_mes = self.num_Dias_Mes(sel_anio, sel_mes)
            
            comboAnio['values'] = tuple(range(1900, 2100 + 1)) #tupla del 1900 al 2100
            comboMes['values'] = ('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')
            comboDia['values'] = tuple(range(1, num_dias_mes + 1)) #tupla desde al 1 hasta el último dia del mes

        # Inicializar en el día actual/seleccionado (el index será el número correspondiente menos el primer número posible)
        rellenar_Selectores_Fecha()
        comboDia.set(sel_dia)
        comboMes.current(sel_mes - 1)
        comboAnio.set(sel_anio)

        def actualizar_Seleccion(event = None):
            nonlocal sel_anio, sel_mes, sel_dia
            sel_anio = int(comboAnio.get())
            sel_mes = comboMes.current() + 1
            sel_dia = int(comboDia.get())

            num_dias_mes = self.num_Dias_Mes(sel_anio, sel_mes)
            #Si el dia seleccionado es mayor al último día del mes, forzamos la selección al último día del mes
            if sel_dia > num_dias_mes:
                sel_dia = num_dias_mes 
                comboDia.set(num_dias_mes)
            rellenar_Selectores_Fecha()

        def confirmar_Seleccion():
            if date(sel_anio, sel_mes, sel_dia) > current_date:
                mssg.showerror('¡ Atención !', 'No se puede seleccionar una fecha posterior a hoy')
            elif date(sel_anio, sel_mes, sel_dia) < date(current_year, 1, 1):
                mssg.showerror('¡ Atención !', f'No se puede seleccionar una fecha antes de {current_year}')
            else:
                self.sel_fecha = datetime(sel_anio, sel_mes, sel_dia)
                self.entryFechaText.set(self.sel_fecha.strftime('%d/%m/%Y'))
                ventana.destroy()


        comboDia.bind('<<ComboboxSelected>>', actualizar_Seleccion)
        comboMes.bind('<<ComboboxSelected>>', actualizar_Seleccion)
        comboAnio.bind('<<ComboboxSelected>>', actualizar_Seleccion)
        btnSeleccionar.configure(command=confirmar_Seleccion)
        btnCancelar.configure(command=ventana.destroy)



    def adiciona_Registro(self):
        '''Adiciona un producto a la BD si la validación es True'''
        # Convierte la fecha de datetime a AAAA-MM-DD (así lo maneja sqlite)
        if self.sel_fecha is not None:
            fecha_sql = self.sel_fecha.strftime('%Y-%m-%d')
        else:
            fecha_sql = None
        
        if self.actualiza:
            self.actualiza = None #REVISION
            self.entryId.configure(state = 'readonly')
            query = 'UPDATE t_participantes SET Nombre = ?, Direccion = ?, Celular = ?, Entidad = ?, Fecha = ?, Id_Departamento = ?, Id_Ciudad = ? WHERE Id = ?'
            parametros = (self.entryNombre.get(), self.entryDireccion.get(), self.entryCelular.get(),
                          self.entryEntidad.get(), fecha_sql, self.cod_departamento,
                          self.cod_ciudad, self.entryId.get())
            self.run_Query(query, parametros)
            mssg.showinfo('Ok', 'Registro actualizado con éxito')
            self.limpia_Campos()
        else:
            if self.valida_Grabar(): #revisar reumen del commit
                query = 'INSERT INTO t_participantes(Id, Nombre, Direccion, Celular, Entidad, Fecha, Id_Departamento, Id_Ciudad) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
                parametros = (self.entryId.get(), self.entryNombre.get(), self.entryDireccion.get(),
                          self.entryCelular.get(), self.entryEntidad.get(), fecha_sql,
                          self.cod_departamento, self.cod_ciudad)
                self.run_Query(query, parametros)
                mssg.showinfo('',f'Registro con ID: {self.entryIdText.get()}, agregado')
                self.limpia_Campos()
            else:
                mssg.showerror('¡ Atención !','No puede crear una identificación existente o dejarla vacía')

        self.lee_tablaTreeView()

    def edita_tablaTreeView(self):
        if len(self.treeDatos.selection()) == 0:
            mssg.showerror('¡ Atención !', 'Por favor seleccione un ítem de la tabla')
        elif len(self.treeDatos.selection()) > 1:
            mssg.showerror('¡ Atención !', 'Solo puede seleccionar un ítem a editar')
        else:
            self.treeDatos.item(self.treeDatos.selection())['text']
            self.limpia_Campos()
            self.actualiza = True # Esta variable controla la actualización
            self.carga_Datos()
        
    def elimina_Registro(self):
        if not self.treeDatos.selection(): #Verifica si la selección de la tabla esta vacía, osea, no ha seleccionado nada
            mssg.showerror('¡ Atención !', 'Por favor seleccione los items a eliminar de la tabla')
            return
        
        confirmation_msg = mssg.askyesno('', '¿Desea borrar los datos seleccionados?')
        if confirmation_msg == True:
            query = ('DELETE FROM t_participantes WHERE Id = ?')
            for param in self.treeDatos.selection(): #Bucle para que pueda borrar cada selección
                parametros = (self.treeDatos.item(param)['text'], ) #Una selección que hace el usuario
                self.run_Query(query, parametros)
            
            mssg.showinfo('Eliminado', 'Los registros seleccionados fueron eliminados')
            self.lee_tablaTreeView() #Carga la tabla al treeview actualizada




if __name__ == '__main__':
    app = Participantes()
    app.run() 