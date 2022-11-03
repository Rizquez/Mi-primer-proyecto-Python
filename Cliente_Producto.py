from tkinter import LabelFrame, ttk, Toplevel, Entry, Label, W, E, END, CENTER, messagebox
import matplotlib.pylab as plt
import sqlite3

# Clase principal (padre)
class Usuario:

    # Base de datos relacional entre cliente-producto-proveedor-admin
    db = "database/Producto_Usuario.db"

    # Constructor de la clase
    def __init__(self,root):
        # Construccion de la ventana principal
        self.ventana = root
        self.ventana.title("Compras y algo más")
        self.ventana.configure(background = "SlateBlue3")
        # Dimension que quiero que tenga la ventana principal
        ancho_ventana = 350
        alto_ventana = 350
        # En las siguientes lineas se obtendran el alto total y ancho total de la pantalla con los metodos abajo señalados
        # Los valores obtenidos los dividire entre dos para obtener la parte entera
        # Luego le restare la mitad del alto o ancho de la ventana que quiero crear para obtener la posicion en X e Y de la ventada
        x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2 # root.winfo_screenwidth() = 1280
        y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2 # root.winfo_screenheight() = 720
        # Los valores obtenidos se los concatenare mediante la linea de abajo para centrar el frame segun el tamaño que yo quiero
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        # Luego la posicion conseguida la paso como parametro del metodo geometry para darle posicion final
        self.ventana.geometry(posicion) # Definiendo las dimensiones de la ventana
        self.ventana.resizable(False, False)
        self.ventana.wm_iconbitmap("recursos/store_icono.ico") # Debe colocarse el .ico al final para que no genere error
        # Definicion del contenedor
        frame = LabelFrame(self.ventana, text = "Bienvenido a Compras y Algo más\n\nIndentifiquese por favor\n", font = ('Calibri', 16, 'bold'))
        # En este caso pady nos da el margen superior en pixeles del frame, si aumento el tamaño del mismo en las lineas de codigo de arriba se mantendra igual el margen definido
        frame.grid(row=0,column=0,columnspan=3,pady=30,padx=15) # Dimensiono el Frame para poder escribir e imprimir sobre el
        # Creando y centrando botones
        # En los botones para ingresar en vez de llamar a un metodo en especifico se llama con la funcion command a la clase que contenga los metodos a los que quiero acceder
        # Boton ingreso de cliente
        self.boton_cliente = ttk.Button(frame, text="Ingresar como Cliente", style="usuario.TButton", width=30, command=Cliente)
        self.boton_cliente.grid(padx=5,pady=10,row=1)
        # Boton ingreso de proveedor
        self.boton_proveedor = ttk.Button(frame, text="Ingresar como Proveedor", style="usuario.TButton", width=30, command=Proveedor)
        self.boton_proveedor.grid(padx=0,pady=5,row=2)
        # Boton ingreso de administrador
        # Creo un pequeño Frame para el boton solo para darle algo de profundidad y que no se vea solo pegado en la ventana
        frame_admin = LabelFrame(self.ventana)
        frame_admin.grid(row=1,column=1)
        self.boton_admin = ttk.Button(frame_admin, text="Administrador", style="usuario.TButton", command=Administrador)
        self.boton_admin.grid(row=1,column=1)

        # Estilo de tablas y botones
        # Configurando el estilo para todos los botones
        estilo_usuario = ttk.Style()
        estilo_usuario.configure("usuario.TButton", font=('Calibri', 14, 'bold'), background='blue')
        # Configurando el estilo para todas las tablas
        style = ttk.Style()
        # Modificando las fuentes
        style.configure('mystyle.Treeview', highlightthickness=0, background='white', font=('Calibri', 11))
        # Modificando la fuente de las cabeceras
        style.configure('mystyle.Treeview.Heading', font=('Calibri', 13, 'bold'))
        style.layout('mystyle.Treeview', [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Definiendo metodo de conexion a la base de datos
    def db_consulta(self, query, parametros=()):
        with sqlite3.connect(self.db) as conexion:
            cursor = conexion.cursor()
            resultado = cursor.execute(query, parametros)
            conexion.commit()
        return resultado

    # Funciones para validar que los Entry no esten vacios
    def validacion_usuario(self):
        input_usuario = self.input_nombre_ingresar.get()
        return len(input_usuario) != 0
    def validacion_clave(self):
        input_clave = self.input_clave_ingresar.get()
        return len(input_clave) != 0

    # Se define una funcion para obtener el registro de los productos actuales de la BBDD
    # Metodo empleado por la clase Cliente y Proveedor
    def obtener_productos(self):
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            # Eliminando los regristros para luego (en las siguientes lineas) actualizarlos a medida que se editen o agreguen datos
            self.tabla.delete(fila)
        # Se realiza una consulta en la BBDD de forma descendente
        query = "SELECT * FROM producto ORDER BY descripcion DESC"
        registros = cursor.execute(query)
        # Se itera sobre los registros obtenidos para introducirlos en la tabla
        for fila in registros:
            self.tabla.insert("", 0, text=(fila[1]), values=(fila[2], fila[3]))
        cursor.close()
        self.db.close()


class Cliente(Usuario):
    # El constructor sera el Frame del login para el cliente
    def __init__(self):
        # Construyendo ventana
        self.ventana_ingresar = Toplevel()
        self.ventana_ingresar.title("Login")
        self.ventana_ingresar.configure(background="SlateBlue3")
        self.ventana_ingresar.resizable(False, False)
        self.ventana_ingresar.wm_iconbitmap("recursos/store_icono.ico")
        frame_ventana_ingresar = LabelFrame(self.ventana_ingresar)
        frame_ventana_ingresar.grid(row=0, column=0, columnspan=3, pady=20)
        self.mensaje = Label(frame_ventana_ingresar, text="", fg="Red")
        self.mensaje.grid(row=7, column=0, columnspan=2, sticky=W + E)
        self.mensaje['text'] = ''
        # Creando las etiquetas e input de los usuarios
        # Nombre
        self.etiqueta_nombre_ingresar = Label(frame_ventana_ingresar, text="Nombre usuario:", font=('Calibri', 14, 'bold'))
        self.etiqueta_nombre_ingresar.grid(row=1, column=0, pady=5)
        self.input_nombre_ingresar = Entry(frame_ventana_ingresar, font=('Calibri', 14))
        self.input_nombre_ingresar.grid(row=2, column=0)
        self.input_nombre_ingresar.focus()
        # Clave
        self.etiqueta_clave = Label(frame_ventana_ingresar, text="Clave de acceso:", font=('Calibri', 14, 'bold'))
        self.etiqueta_clave.grid(row=3, column=0, pady=5)
        self.input_clave_ingresar = Entry(frame_ventana_ingresar, font=('Calibri', 14))
        self.input_clave_ingresar.grid(row=4, column=0)
        # Ingresar y registrar
        self.ingresar = ttk.Button(frame_ventana_ingresar, text="Login", style="usuario.TButton", command=self.verificar_cliente)
        self.ingresar.grid(row=5, column=0, pady=5)
        # En la siguiente linea implementare lambda junto a comand y la funcion destoy para que cuando le de al boton para "registrar" un nuevo usuario se cierre de forma automatica la ventana de login
        # En este caso si sera necesario colocar los parentesis en las funciones que integraran los parametros del lambda
        self.registrar = ttk.Button(frame_ventana_ingresar, text="Registrarse", style="usuario.TButton", command=lambda: [self.frame_registrar(), self.ventana_ingresar.destroy()])
        self.registrar.grid(row=6, column=0, pady=20)

    # Funciones para verificar que los Entry en el registro de usuario nuevo no esten vacios
    def validacion_nombre_registrar(self):
        input_nombre_registrar = self.nombre_registrar.get()
        return len(input_nombre_registrar) != 0
    def validacion_clave_registrar(self):
        input_clave_registrar = self.clave_registrar.get()
        return len(input_clave_registrar) != 0
    def validacion_direccion_registrar(self):
        input_direccion_registrar = self.direccion_registrar.get()
        return len(input_direccion_registrar) != 0
    def validacion_contacto_registrar(self):
        input_contacto_registrar = self.contacto_registrar.get()
        return len(input_contacto_registrar) != 0

    # Funcion para generar la grafica
    def grafica_ventas(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0] # Se selecionar el producto en pantalla
            self.mensaje_grafico['text'] = ''
        except IndexError as e: # Si el usuario no marca ningun producto se imprimira este mensaje
            self.mensaje_grafico['text'] = "Error! Seleccione un producto para visualizar su grafico"
            return
        descripcion = self.tabla.item(self.tabla.selection())['text'] # Se guarda en una varible el producto señalado por el usuario
        query = "SELECT total_ventas FROM producto WHERE descripcion = ?" # Consulta que se pasara a la BBDD
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        cursor.execute(query, (descripcion, )) # Se envia como tupla los parametros (es importante señalar esto)
        filas = cursor.fetchall() # Se obtienen todos los resultados
        for columna in filas: # Se itera sobre los resultados obtenidos para poder trabajar con ellos
            # Al haber enviado la consulta en formato de tupla se obtiene una tupla al hacer la iteracion
            # Se accede al primer parametro de la tupla que es un string
            total_ventas = columna[0]
            # El string obtenido con anterioridad se le aplica casting para pasarlo de formato string a dict iterando sobre la propia lista que contiene el string
            # Se almacenan los datos obtenidos en una nueva variable
            diccionario = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in total_ventas.split(',')))
            # En las siguientes lineas de codigo se configura la grafica
            del diccionario['anyo'] # Elimino el par de valores de la clave anyo ya que no interesa en el grafico
            claves = diccionario.keys()
            valores = diccionario.values()
            # Asignamos las claves y valores a las coordenadas x-y no es necesario pero entiendo mejor el codigo asi
            x, y = claves, valores
            # Desde aca comienzo a trabajar sobre el grafico
            plt.plot(x,y, color = 'blue') # Asignacion de valores a las coordenadas
            plt.grid(b=True) # El parametro b funciona para colocar lineas de indicacion en el fondo de la grafica
            plt.xlabel('Meses') # Leyenda en X
            plt.ylabel('Unidades vendidas') # Leyenda en Y
            plt.title('Ventas durante el año 2021: ' + descripcion) # Titulo del grafico, concateno el articulo sobre el que se esta graficando
            plt.show() # Impresion del grafico
        cursor.close()
        self.db.close()

    # Funcion para verificar la existencia del cliente y en caso de ser positiva crear una interfaz para él
    def verificar_cliente(self):
        # Creando conexion a la BBDD para verificar el acceso de los clientes
        if self.validacion_usuario() and self.validacion_clave():
            self.db = sqlite3.connect('database/Producto_Usuario.db')
            cursor = self.db.cursor()
            query = "SELECT nombre, clave FROM clientes WHERE nombre = ? AND clave = ?"
            parametros = (self.input_nombre_ingresar.get(), self.input_clave_ingresar.get())
            cursor.execute(query, parametros)
            # Condicion en caso de obtener acceso autorizado
            if cursor.fetchall():
                # Creando la interfaz de cada usuario
                self.ventana_usuario = Toplevel()
                self.ventana_usuario.title("Compras y algo más")
                self.ventana_usuario.configure(background="SlateBlue3")
                self.ventana_usuario.resizable(False,False)
                self.ventana_usuario.wm_iconbitmap("recursos/usuario_icono.ico")
                # Destruyendo la ventana de inicio de sesion
                self.ventana_ingresar.destroy()
                # Crando el Frame de la ventana de los usuarios
                frame_cliente = LabelFrame(self.ventana_usuario, text="Listado de productos", font=('Calibri', 16, 'bold'), labelanchor="n")
                frame_cliente.grid(row=0,column=0,columnspan=3,pady=20)
                # Mensaje a utilizar la funcion de graficar
                self.mensaje_grafico = Label(frame_cliente, text="", fg="Red")
                self.mensaje_grafico.grid(row=8, column=1, columnspan=2, sticky=W + E)
                self.mensaje_grafico['text'] = ''
                # Se configura las cabecera de la tabla señalando la cantidad de tablas que habra
                self.tabla = ttk.Treeview(frame_cliente, height=20, columns=[f"#{n}" for n in range(1, 3)], style = 'mystyle.Treeview')
                self.tabla.grid(row=7, column=0, columnspan=4)
                # Cabeceras de las tablas
                self.tabla.heading("#0", text='Descripción', anchor=CENTER)
                self.tabla.heading("#1", text='Precio', anchor=CENTER)
                self.tabla.heading("#2", text='Categoria', anchor=CENTER)
                # Posicionando los datos dentro de las tablas
                self.tabla.column("#0", anchor=W)
                self.tabla.column("#1", anchor=CENTER)
                self.tabla.column("#2", anchor=CENTER)
                # Creando boton para ver las graficas de ventas
                boton_ventas = ttk.Button(self.ventana_usuario, text="Grafico de ventas", style="usuario.TButton", command=self.grafica_ventas)
                boton_ventas.grid(row=1, column=1, sticky=W + E, pady=15)
                # Se llama a la funcino para obtener los datos de la BBDD
                self.obtener_productos()
            else:
                self.mensaje['text'] = "Los datos ingresados no estan registrados"
            # Cerrando BBDD
            cursor.close()
            self.db.close()
        elif self.validacion_usuario() and self.validacion_clave() == False:
            self.mensaje['text'] = "Debe ingresar la contraseña de acceso"
        elif self.validacion_usuario() == False and self.validacion_clave():
            self.mensaje['text'] = "Debe ingresar el nombre de usuario"
        else:
            self.mensaje['text'] = "Ingrese sus datos de acceso"

    # Creacion del frame para el registro de nuevos clientes
    def frame_registrar(self):
        # Construyendo ventana
        self.ventana_registrar = Toplevel()
        self.ventana_registrar.title("Nuevo Usuario")
        self.ventana_registrar.configure(background="SlateBlue3")
        self.ventana_registrar.resizable(False, False)
        self.ventana_registrar.wm_iconbitmap("recursos/store_icono.ico")
        frame_ventana_registrar = LabelFrame(self.ventana_registrar)
        frame_ventana_registrar.grid(row=0, column=0, columnspan=3, pady=20)
        self.mensaje = Label(frame_ventana_registrar, text = "",fg = "Red")
        self.mensaje.grid(row=6, column=0, columnspan=2, sticky=W + E)
        self.mensaje['text'] = ''
        # Nombre nuevo
        self.etiqueta_nombre_registrar = Label(frame_ventana_registrar, text="Nombre usuario:",font = ('Calibri', 14, 'bold'))
        self.etiqueta_nombre_registrar.grid(row=1,column=0, pady=5)
        self.nombre_registrar = Entry(frame_ventana_registrar, font=('Calibri',14))
        self.nombre_registrar.grid(row=1, column=1, pady=5)
        self.nombre_registrar.focus()
        # Clave nueva
        self.etiqueta_clave = Label(frame_ventana_registrar, text="Nueva contraseña:", font = ('Calibri', 14, 'bold'))
        self.etiqueta_clave.grid(row=2,column=0, pady=5)
        self.clave_registrar = Entry(frame_ventana_registrar, font=('Calibri',14))
        self.clave_registrar.grid(row=2, column=1, pady=5)
        # Direccion nueva
        self.etiqueta_direccion = Label(frame_ventana_registrar, text="Direccion de domicilio:", font=('Calibri', 14, 'bold'))
        self.etiqueta_direccion.grid(row=3, column=0, pady=5)
        self.direccion_registrar = Entry(frame_ventana_registrar, font=('Calibri', 14))
        self.direccion_registrar.grid(row=3, column=1, pady=5)
        # Numero de contacto nuevo
        self.etiqueta_contacto = Label(frame_ventana_registrar, text="Informacion de contacto:", font=('Calibri', 14, 'bold'))
        self.etiqueta_contacto.grid(row=4, column=0, pady=5)
        self.contacto_registrar = Entry(frame_ventana_registrar, font=('Calibri', 14))
        self.contacto_registrar.grid(row=4, column=1, pady=5)
        # Guardar datos
        self.registrar = ttk.Button(frame_ventana_registrar, text="Guardar datos", style="usuario.TButton", command=self.registrar_usuario)
        self.registrar.grid(row=5, column=0, pady=5, sticky=W+E, columnspan=2)

    # Funcion que registra los datos ingresado por los clientes
    def registrar_usuario(self):
        # Creando consulta para insertar valores en la tabla de clientes
        if self.validacion_nombre_registrar() and self.validacion_clave_registrar() and self.validacion_direccion_registrar() and self.validacion_contacto_registrar():
            query = "INSERT INTO clientes VALUES(NULL, ?, ?, ?, ?)"
            parametros = (self.nombre_registrar.get(), self.clave_registrar.get(), self.direccion_registrar.get(),self.contacto_registrar.get())
            self.db_consulta(query, parametros)
            # Limpiando registros agregados
            self.nombre_registrar.delete(0,END)
            self.clave_registrar.delete(0, END)
            self.direccion_registrar.delete(0, END)
            self.contacto_registrar.delete(0, END)
            self.mensaje['text'] = "Usuario creado exitosamente! Cierre esta ventana e inicie sesión"
        else:
            self.mensaje['text'] = "Todos los campos deben ser llenados"


class Proveedor(Usuario):
    # El constructor sera el Frame del login para el proveedor
    def __init__(self):
        # Construyendo ventana
        self.ventana_ingresar = Toplevel()
        self.ventana_ingresar.title("Login")
        self.ventana_ingresar.configure(background="SpringGreen2")
        self.ventana_ingresar.resizable(False, False)
        self.ventana_ingresar.wm_iconbitmap("recursos/store_icono.ico")
        frame_ventana_ingresar = LabelFrame(self.ventana_ingresar)
        frame_ventana_ingresar.grid(row=0, column=0, columnspan=3, pady=20)
        self.mensaje = Label(frame_ventana_ingresar, text="", fg="Red")
        self.mensaje.grid(row=7, column=0, columnspan=2, sticky=W + E)
        self.mensaje['text'] = ''
        # Creando las etiquetas e input de los usuarios
        # Nombre
        self.etiqueta_nombre_ingresar = Label(frame_ventana_ingresar, text="Nombre de empresa:", font=('Calibri', 14, 'bold'))
        self.etiqueta_nombre_ingresar.grid(row=1, column=0, pady=5)
        self.input_nombre_ingresar = Entry(frame_ventana_ingresar, font=('Calibri', 14))
        self.input_nombre_ingresar.grid(row=2, column=0)
        self.input_nombre_ingresar.focus()
        # Clave
        self.etiqueta_clave = Label(frame_ventana_ingresar, text="Clave de acceso:", font=('Calibri', 14, 'bold'))
        self.etiqueta_clave.grid(row=3, column=0, pady=5)
        self.input_clave_ingresar = Entry(frame_ventana_ingresar, font=('Calibri', 14))
        self.input_clave_ingresar.grid(row=4, column=0)
        # Ingresar
        self.ingresar = ttk.Button(frame_ventana_ingresar, text="Login", style="usuario.TButton", command=self.verificar_proveedor)
        self.ingresar.grid(row=5, column=0, pady=5)

    # Funcion para generar la grafica
    def grafica_compras(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]  # Se selecionar el producto en pantalla
            self.mensaje_grafico['text'] = ''
        except IndexError as e:  # Si el usuario no marca ningun producto se imprimira este mensaje
            self.mensaje_grafico['text'] = "Error! Seleccione un producto para visualizar su grafico"
            return
        descripcion = self.tabla.item(self.tabla.selection())['text']  # Se guarda en una varible el producto señalado por el usuario
        query = "SELECT total_compras FROM producto WHERE descripcion = ?"  # Consulta que se pasara a la BBDD
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        cursor.execute(query, (descripcion,))  # Se envia como tupla los parametros (es importante señalar esto)
        filas = cursor.fetchall()  # Se obtienen todos los resultados
        for columna in filas:  # Se itera sobre los resultados obtenidos para poder trabajar con ellos
            # Al haber enviado la consulta en formato de tupla se obtiene una tupla al hacer la iteracion
            # Se accede al primer parametro de la tupla que es un string
            total_compras = columna[0]
            # El string obtenido con anterioridad se le aplica casting para pasarlo de formato string a dict
            # Se almacenan los datos obtenidos en una nueva variable
            diccionario = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in total_compras.split(',')))
            # En las siguientes lineas de codigo se configura la grafica
            del diccionario['anyo']  # Elimino el par de valores de la clave anyo ya que no interesa en el grafico
            claves = diccionario.keys()
            valores = diccionario.values()
            # Asignamos las claves y valores a las coordenadas x-y no es necesario pero entiendo mejor el codigo asi
            x, y = claves, valores
            # Desde aca comienzo a trabajar sobre el grafico
            plt.plot(x, y, color = 'orange')  # Asignacion de valores a las coordenadas
            plt.grid(b=True)  # El parametro b funciona para colocar lineas de indicacion en el fondo de la grafica
            plt.xlabel('Meses')  # Leyenda en X
            plt.ylabel('Unidades compradas')  # Leyenda en Y
            plt.title('Compras durante el año 2021: ' + descripcion)  # Titulo del grafico, concateno el articulo sobre el que se esta graficando
            plt.show()  # Impresion del grafico
        cursor.close()
        self.db.close()

    # Funcion para verificar la existencia del proveedor y en caso de ser positiva crear una interfaz para él
    def verificar_proveedor(self):
        # Creando conexion a la BBDD para verificar el acceso de los clientes
        if self.validacion_usuario() and self.validacion_clave():
            self.db = sqlite3.connect('database/Producto_Usuario.db')
            cursor = self.db.cursor()
            query = "SELECT nombre_empresa, clave FROM proveedores WHERE nombre_empresa = ? AND clave = ?"
            parametros = (self.input_nombre_ingresar.get(), self.input_clave_ingresar.get())
            cursor.execute(query, parametros)
            # Condicion en caso de obtener acceso autorizado
            if cursor.fetchall():
                # Creando la interfaz de cada usuario
                self.ventana_proveedor = Toplevel()
                self.ventana_proveedor.title("Compras y algo más (Acceso Proveedores)")
                self.ventana_proveedor.configure(background="SpringGreen2")
                self.ventana_proveedor.resizable(False,False)
                self.ventana_proveedor.wm_iconbitmap("recursos/proveedor_icono.ico")
                # Destruyendo la ventana de inicio de sesion
                self.ventana_ingresar.destroy()
                # Crando el Frame de la ventana de los usuarios
                frame_proveedor = LabelFrame(self.ventana_proveedor, text="Listado de productos", font=('Calibri', 16, 'bold'), labelanchor="n")
                frame_proveedor.grid(row=0,column=0,columnspan=3,pady=20)
                # Mensaje a utilizar la funcion de graficar
                self.mensaje_grafico = Label(frame_proveedor, text="", fg="Red")
                self.mensaje_grafico.grid(row=8, column=1, columnspan=2, sticky=W + E)
                self.mensaje_grafico['text'] = ''
                # Se configura las cabecera de la tabla señalando la cantidad de tablas que habra
                self.tabla = ttk.Treeview(frame_proveedor, height=20, columns=[f"#{n}" for n in range(1, 3)], style = 'mystyle.Treeview')
                self.tabla.grid(row=7, column=0, columnspan=4)
                # Cabeceras de las tablas
                self.tabla.heading("#0", text='Descripción', anchor=CENTER)
                self.tabla.heading("#1", text='Precio', anchor=CENTER)
                self.tabla.heading("#2", text='Categoria', anchor=CENTER)
                # Posicionando los datos dentro de las tablas
                self.tabla.column("#0", anchor=W)
                self.tabla.column("#1", anchor=CENTER)
                self.tabla.column("#2", anchor=CENTER)
                # Creando boton para ver las graficas de ventas
                boton_ventas = ttk.Button(self.ventana_proveedor, text="Grafico de compras", style="usuario.TButton", command=self.grafica_compras)
                boton_ventas.grid(row=1, column=1, sticky=W + E, pady=15)
                # Se llama al metodo para obtener el registro de los productos actuales de la BBDD
                self.obtener_productos()
            else:
                self.mensaje['text'] = "Los datos ingresados no estan registrados"
            # Cerrando BBDD
            cursor.close()
            self.db.close()
        elif self.validacion_usuario() and self.validacion_clave() == False:
            self.mensaje['text'] = "Debe ingresar la clave de acceso"
        elif self.validacion_usuario() == False and self.validacion_clave():
            self.mensaje['text'] = "Debe ingresar el nombre de la empresa"
        else:
            self.mensaje['text'] = "Ingrese sus datos de acceso"

# En este caso la clase Administrador heredara solo de la clase Cliente y Proveedor ya que de esa manera la clase Usuario vendria a ser su clase abuelo y las otras sus clases padre
class Administrador(Cliente, Proveedor):
    # El constructor sera el Frame del login para el administrador
    def __init__(self):
        # Construyendo ventana
        self.ventana_ingresar = Toplevel()
        self.ventana_ingresar.title("Login")
        self.ventana_ingresar.configure(background="purple")
        self.ventana_ingresar.resizable(False, False)
        self.ventana_ingresar.wm_iconbitmap("recursos/store_icono.ico")
        frame_ventana_ingresar = LabelFrame(self.ventana_ingresar)
        frame_ventana_ingresar.grid(row=0, column=0, columnspan=3, pady=20)
        self.mensaje = Label(frame_ventana_ingresar, text="", fg="Red")
        self.mensaje.grid(row=8, column=0, columnspan=2, sticky=W + E)
        self.mensaje['text'] = ''
        # Creando las etiquetas e input de los usuarios
        # Nombre
        self.etiqueta_nombre_ingresar = Label(frame_ventana_ingresar, text="Usuario Admin:", font=('Calibri', 14, 'bold'))
        self.etiqueta_nombre_ingresar.grid(row=1, column=0, pady=5)
        self.input_nombre_ingresar = Entry(frame_ventana_ingresar, font=('Calibri', 14))
        self.input_nombre_ingresar.grid(row=2, column=0)
        self.input_nombre_ingresar.focus()
        # Clave
        self.etiqueta_clave = Label(frame_ventana_ingresar, text="Clave de acceso:", font=('Calibri', 14, 'bold'))
        self.etiqueta_clave.grid(row=3, column=0, pady=5)
        self.input_clave_ingresar = Entry(frame_ventana_ingresar, font=('Calibri', 14))
        self.input_clave_ingresar.grid(row=4, column=0)
        # Ingresar
        self.ingresar = ttk.Button(frame_ventana_ingresar, text="Login", style="usuario.TButton", command=self.verificar_admin)
        self.ingresar.grid(row=5, column=0, pady=5)

    # Funcion que obtendra el registro completo de todos los productos y la informacion relacionada a ellso
    # La creo como metodo exclusivo de admin ya que solo ellos podran acceder a estos datos
    def obtener_productos_admin(self):
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            # Eliminando los regristros para luego (en las siguientes lineas) actualizarlos a medida que se editen o agreguen datos
            self.tabla.delete(fila)
        # Se realiza una consulta en la BBDD de forma descendente
        query = "SELECT * FROM producto ORDER BY descripcion DESC"
        registros = cursor.execute(query)
        # Se itera sobre los registros obtenidos para introducirlos en la tabla
        for fila in registros:
            self.tabla.insert("", 0, text=(fila[1]), values=(fila[2], fila[3], fila[4], fila[5], fila[6]))
        cursor.close()
        self.db.close()

    # Funcion encargada de verificar el estado del inventario y avisar si hace falta de comprar algun producto
    def avisar_comprar_producto(self, producto):
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        query = "SELECT stock FROM producto WHERE descripcion = ?"
        cursor.execute(query, producto)
        dato = cursor.fetchall()
        stock = dato[0][0] # Hago doble slicing ya que la consulta me regresa una lista con una tupla dentro
        cursor.close()
        self.db.close()
        # Se que es mas facil poner los numeros y ya, pero es mejor hacer un codigo mas legible
        almacen_full = 100
        porcentaje_senyalado = 90
        if stock < (almacen_full*porcentaje_senyalado)/100:
            messagebox.showinfo(message='Stock insuficiente\nContacte con Proveedor', title='Inventario actual')

    # Funcion encargada de obtener los beneficios
    def obtener_beneficios(self, producto):
        # Se inician las dos consultas
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        query1 = "SELECT producto_precio FROM proveedores"
        cursor.execute(query1)
        dato1 = cursor.fetchall()
        query2 = "SELECT precio, total_ventas FROM producto WHERE descripcion = ?"
        cursor.execute(query2, producto)
        dato2 = cursor.fetchall()
        cursor.close()
        self.db.close() # Se cierra tod0
        precio_venta = dato2[0][0]
        total_ventas = dato2[0][1]
        dic_total_ventas = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in total_ventas.split(',')))
        del dic_total_ventas['anyo']
        proveedor1 = dato1[0][0]
        proveedor2 = dato1[1][0]
        dic_proveedor1 = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in proveedor1.split(',')))
        dic_proveedor2 = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in proveedor2.split(',')))
        # En la siguente linea se unen los diccionarios para poder iterar sobre uno solo
        # De esta manera el dic_proveedor1 pasa ahora a contener a los dos diccionarios
        dic_proveedor1.update(dic_proveedor2)
        precio_compra = dic_proveedor1[producto[0]] # En esta linea se pasa como clave del dicionario el nombre del producto seleccionado y se obtiene el precio de compra
        ganancia_bruto = round(precio_venta * sum(dic_total_ventas.values()) - precio_compra * sum(dic_total_ventas.values()),2) # Se obtienen el margen de ganancia bruto
        # Obviamente esto es un calculo simple donde hace falta tomar en cuenta muchos otros aspectos para poder obtener las ganancias en bruto y neto de un negocio
        return ganancia_bruto

    # Funcion para generar la grafica
    def grafica_comparativa(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]  # Se selecionar el producto en pantalla
            self.mensaje_grafico['text'] = ''
        except IndexError as e:  # Si el usuario no marca ningun producto se imprimira este mensaje
            self.mensaje_grafico['text'] = "Error! Seleccione un producto para visualizar su grafico"
            return
        descripcion = self.tabla.item(self.tabla.selection())['text']  # Se guarda en una varible el producto señalado por el usuario
        self.obtener_beneficios((descripcion, ))
        self.avisar_comprar_producto((descripcion, ))
        query1 = "SELECT total_ventas, total_compras FROM producto WHERE descripcion = ?"  # Consulta que se pasara a la BBDD
        self.db = sqlite3.connect('database/Producto_Usuario.db')
        cursor = self.db.cursor()
        cursor.execute(query1, (descripcion, ))  # Se envia como tupla los parametros (es importante señalar esto)
        filas = cursor.fetchall()  # Se obtienen todos los resultados
        for columna in filas:  # Se itera sobre los resultados obtenidos para poder trabajar con ellos
            # De la consulta anterior obtengo una lista con dos parametros en fomato string
            # Almaceno cada parametro en una variable para poder graficarlos superpuestos
            ventas = columna[0]
            compras = columna[1]
            # Aplico casting a cada valor para convertirlos de string a dict
            dic_ventas = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in ventas.split(',')))
            dic_compras = dict(((lambda dato: (dato[0], float(dato[1])))(valor.split(':')) for valor in compras.split(',')))
            # Elimino el par de valores de la clave anyo ya que no interesa en el grafico
            del dic_ventas['anyo']
            del dic_compras['anyo']
            # Obtengo los valores y claves de cada diccionario
            # Al tener la misma clave ambos diccionarios con obtener solo las claves de uno para la grafica es suficiente
            claves_venta = dic_ventas.keys()
            valores_venta = dic_ventas.values()
            valores_compra = dic_compras.values()
            # Desde aca comienzo a trabajar sobre el grafico
            plt.plot(claves_venta, valores_venta, color = 'blue')  # Asignacion de valores a las coordenadas
            plt.plot(claves_venta, valores_compra, color = 'orange')
            plt.grid(b=True)  # El parametro b funciona para colocar lineas de indicacion en el fondo de la grafica
            plt.xlabel('Meses')  # Leyenda en X
            plt.ylabel('Unidades compradas-vendidas')  # Leyenda en Y
            plt.title('Compra vs Venta año 2021: ' + descripcion + ' -->Beneficio bruto obtenido: {}€'.format(self.obtener_beneficios((descripcion, ))))  # Titulo del grafico, concateno el articulo sobre el que se esta graficando
            plt.legend(['Ventas', 'Compras']) # Leyenda utilizada para señalar que grafico pertenece a que parametro
            plt.show()  # Impresion del grafico
        cursor.close()
        self.db.close()

    # Funcion para verificar el acceso de administrador y creacion de interfaz grafica
    def verificar_admin(self):
        #Creando conexion a la BBDD para verificar el acceso de los clientes
        if self.validacion_usuario() and self.validacion_clave():
            self.db = sqlite3.connect('database/Producto_Usuario.db')
            cursor = self.db.cursor()
            query = "SELECT nombre, clave FROM administradores WHERE nombre = ? AND clave = ?"
            parametros = (self.input_nombre_ingresar.get(), self.input_clave_ingresar.get())
            cursor.execute(query, parametros)
            # Condicion en caso de obtener acceso autorizado
            if cursor.fetchall():
                # Creando la interfaz de cada usuario
                self.ventana_admin = Toplevel()
                self.ventana_admin.title("Compras y algo más (Acceso Administrador)")
                self.ventana_admin.configure(background="purple")
                self.ventana_admin.resizable(False, False)
                self.ventana_admin.wm_iconbitmap("recursos/admin_icono.ico")
                # Destruyendo la ventana de inicio de sesion
                self.ventana_ingresar.destroy()
                # Crando el Frame de la ventana de los usuarios
                frame_admin = LabelFrame(self.ventana_admin, text="Listado de productos", font=('Calibri', 16, 'bold'), labelanchor="n")
                frame_admin.grid(row=0, column=0, columnspan=3, pady=20)
                # Mensaje a utilizar la funcion de graficar
                self.mensaje_grafico = Label(frame_admin, text="", fg="Red")
                self.mensaje_grafico.grid(row=8, column=1, columnspan=2, sticky=W + E)
                self.mensaje_grafico['text'] = ''
                # Se configura las cabecera de la tabla señalando la cantidad de tablas que habra
                self.tabla = ttk.Treeview(frame_admin, height=20, columns=[f"#{n}" for n in range(1, 6)], style='mystyle.Treeview')
                self.tabla.grid(row=7, column=0, columnspan=4)
                # Cabeceras de las tablas
                self.tabla.heading("#0", text='Descripción', anchor=CENTER)
                self.tabla.heading("#1", text='Precio', anchor=CENTER)
                self.tabla.heading("#2", text='Categoria', anchor=CENTER)
                self.tabla.heading("#3", text='Stock actual', anchor=CENTER)
                self.tabla.heading("#4", text='EAN', anchor=CENTER)
                self.tabla.heading("#5", text='Almacen actual', anchor=CENTER)
                # Posicionando los datos dentro de las tablas
                self.tabla.column("#0", anchor=W)
                self.tabla.column("#1", anchor=CENTER)
                self.tabla.column("#2", anchor=CENTER)
                self.tabla.column("#3", anchor=CENTER)
                self.tabla.column("#4", anchor=CENTER)
                self.tabla.column("#5", anchor=CENTER)
                # Creando boton para ver las graficas de comparativa venta-compra / ventas / compra
                boton_comparativa = ttk.Button(self.ventana_admin, text="Grafica comparativa", style="usuario.TButton", command=self.grafica_comparativa)
                boton_comparativa.grid(row=1, column=1, sticky=W + E, pady=10, padx=10)
                # Se llama al metodo para obtener el registro de los productos actuales de la BBDD
                self.obtener_productos_admin()
            else:
                self.mensaje['text'] = "Los datos ingresados no estan registrados"
            # Cerrando BBDD
            cursor.close()
            self.db.close()
        elif self.validacion_usuario() and self.validacion_clave() == False:
            self.mensaje['text'] = "Debe ingresar la clave de acceso"
        elif self.validacion_usuario() == False and self.validacion_clave():
            self.mensaje['text'] = "Debe ingresar el usuario admin"
        else:
            self.mensaje['text'] = "Ingrese sus datos de acceso"
