from tkinter import *
from tkinter import messagebox 
import sqlite3
import qrcode

#-------------funciones-----------------------------------------
#conexion
def conexionbdd():
    miconexion=sqlite3.connect("usuarios")
    micursor=miconexion.cursor()
    
    try:
        micursor.execute('''
             CREATE TABLE DATOSUSUARIOS(
             ID INTEGER PRIMARY KEY AUTOINCREMENT,
             NOMBRE_USUARIO VARCHAR(50),
             APELLIDO_USUARIO VARCHAR(50),
             CORREO VARCHAR(50),
             CONTRASEÑA VARCHAR(50),
             NOTAS VARCHAR(59))
             ''')
        messagebox.showinfo("bdd","base de datos creada")
        
    except:
        messagebox.showwarning("ATENCION","la base de datos ya ha sido creada")


def salirbdd():
    
    valor=messagebox.askquestion("salir","¿desea salir de la aplicacion")
    if valor =="yes":
        root.destroy()
  
def camposlimpios():
    miID.set("")
    minombre.set("")
    miapellido.set("")
    micorreo.set("")
    mipassword.set("")
    textoadicional.delete(1.0,END)   

    
def crear(): #con esta funcion se puede hacer el qr (creo),se inserta en los parametros del qr
    miconexion=sqlite3.connect("usuarios")
    micursor=miconexion.cursor()
    micursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL, '" +minombre.get() +
                     "','"+ miapellido.get() +
                     "','"+ micorreo.get() +
                     "','"+ mipassword.get() +
                     "','"+ textoadicional.get("1.0",END) + "')")
    miconexion.commit()
    messagebox.showinfo("bdd","registro con exito")
    
def leer():
    miconexion=sqlite3.connect("usuarios")
    micursor=miconexion.cursor()
      
    micursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" + miID.get())
    elusuario=micursor.fetchall()
      
    for usuario in elusuario:
          miID.set(usuario[0])
          minombre.set(usuario[1])
          miapellido.set(usuario[2])
          micorreo.set(usuario[3])
          mipassword.set(usuario[4])
          textoadicional.insert(1.0,usuario[5])
     
    miconexion.commit()

def actualizar():
    miconexion=sqlite3.connect("usuarios")
    micursor=miconexion.cursor()
    micursor.execute(" UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='" + minombre.get() +
                     "', APELLIDO'" + miapellido.get() +
                     "', CORREO'" + micorreo.get() +
                     "', CONTRASEÑA'" + mipassword.get() +
                     "', COMENTARIOS'" + textoadicional.get(1.0,END) +
                     "' WHERE ID=" + miID.get())
    
    miconexion.commit()
    messagebox.showinfo("bdd","registro actualizado con exito")

def eliminar():
    miconexion=sqlite3.connect("usuarios")
    micursor=miconexion.cursor()
    micursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" + miID.get())
    miconexion.commit()
    messagebox.showinfo("ATENCION", "Registro borrado con exito")
    

def QR():
    miconexion=sqlite3.connect("usuarios")
    micursor=miconexion.cursor()
    
    qr= qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,
                  box_size=10,border=4)
    
    datosenelqr=minombre.get(),miapellido.get(),textoadicional.get("1.0",END)
    
    qr.add_data(datosenelqr)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black",back_color="white")
    
    img.save( "miID.png")
    messagebox.showinfo("CODIGO QR", "Codigo qr creado exitosamente")


#----------------------------interfa----------------------------------------
root=Tk()

#se crea la interfaz de la bdd
barraMenu=Menu(root)
root.config(menu=barraMenu,width=300,height=300)


#bdd=base de datos
bddMenu=Menu(barraMenu, tearoff=0)
#conectar la base de datos 
bddMenu.add_command(label="conectar",command=conexionbdd )
bddMenu.add_command(label="salir", command=salirbdd )
bddMenu.add_command(label="CREAR QR" )

#borrar campos
borrarMenu=Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="borrar campos", command=camposlimpios )

crudMenu=Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="crear" ,command=crear)
crudMenu.add_command(label="leer", command=leer )
crudMenu.add_command(label="actualizar", command=actualizar  )
crudMenu.add_command(label="borrar", command=eliminar )

ayudaMenu=Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="licencia" )

barraMenu.add_cascade(label="bdd", menu=bddMenu)
barraMenu.add_cascade(label="borrar",menu=borrarMenu)
barraMenu.add_cascade(label="crud",menu=crudMenu)
barraMenu.add_cascade(label="ayuda",menu=ayudaMenu)

#-------------------------------creamos los campos -------------------------

miframe=Frame(root)
miframe.pack()

miID=StringVar()
minombre=StringVar()
miapellido=StringVar()
micorreo=StringVar()
mipassword=StringVar()

#espacio para texto
cuadroID=Entry(miframe, textvariable=miID)
cuadroID.grid(row=0, column=1,padx=10, pady=10 )
cuadroID.config(fg="red",justify="right") 

#espacio para el nombre del campo
cuadronombre=Entry(miframe,textvariable=minombre)
cuadronombre.grid(row=1, column=1,padx=10, pady=10 )

#capo de apellidos
cuadroapellidos=Entry(miframe,textvariable=miapellido)
cuadroapellidos.grid(row=2, column=1,padx=10, pady=10 )

#correo
cuadrocorreo=Entry(miframe,textvariable=micorreo)
cuadrocorreo.grid(row=3, column=1,padx=10, pady=10 )

#contraseña 
cuadropassword=Entry(miframe,textvariable=mipassword)
cuadropassword.grid(row=4, column=1,padx=10, pady=10 )
cuadropassword.config(show="*")

textoadicional=Text(miframe, width=16, height=5 )
textoadicional.grid(row=5, column=1, padx=10, pady=10)
scrollvert=Scrollbar(miframe, command=textoadicional.yview)
scrollvert.grid(row=5, column=2, sticky="new")

textoadicional.config(yscrollcommand=scrollvert.set)

#------------------------etiquetas de los campos----------------------------
#ID
ID=Label(miframe, text="ID")
ID.grid(row=0, column=0,sticky="e", padx=10, pady=10)

#nombre
nombre=Label(miframe, text="Nombre")
nombre.grid(row=1, column=0,sticky="e", padx=10, pady=10)

#apellido
apellido=Label(miframe, text="Apellido")
apellido.grid(row=2, column=0,sticky="e", padx=10, pady=10)

#correo
correo=Label(miframe, text="Correo")
correo.grid(row=3, column=0,sticky="e", padx=10, pady=10)
#contraseña
password=Label(miframe, text="Contraseña")
password.grid(row=4, column=0,sticky="e", padx=10, pady=10)

#texto
tex=Label(miframe, text="numeros de emergenicia")
tex.grid(row=5, column=0,sticky="e", padx=10, pady=10)

#--------------Botones extras-------------------------------------------

botones=Frame(root)
botones.pack()

#boton de crear
crear=Button(botones, text="crear",command=crear)
crear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

#boton de actualizar
crear=Button(botones, text="update", command=actualizar )
crear.grid(row=1, column=3, sticky="e", padx=10, pady=10)

#boton qr
crear=Button(botones, text="QR", command=QR)
crear.grid(row=1, column=4, sticky="e", padx=10, pady=10)

#borrar
crear=Button(botones, text="Borrar", command=eliminar)
crear.grid(row=1, column=5, sticky="e", padx=10, pady=10)
root.mainloop()

