from Tkinter import *
from PIL import ImageTk, Image
from Jugadas import *
import tkFileDialog
import tkMessageBox
import os
import io
import types

class Interfaz(Frame):

    """
    Constructor de la clase
    Se crea el canvas donde se pondra el tablero
    Se crean los botones y etiquetas de la interfaz
    """
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.pack(fill=BOTH,expand=True)
        self.tablero = None
        self.engine = None
        self.creaCanvas()
        self.creaBotones()

    """
    Dibuja el canvas donde se colocara el tablero
    """
    def creaCanvas(self):        
        self.canvas = Canvas(self, bg="white",width=400,height=400)
        self.canvas.place(x=500,y=10)
        self.tablero = inicializaTablero()
        svg = obtenSvg(self.tablero)
        svgToImage(svg,"tablero")
        imagen = Image.open("tablero.png")
        imagenTk = ImageTk.PhotoImage(imagen)
        self.canvas.image = imagenTk
        self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")

    """
    Se crean los botones para las diferentes acciones de la interfaz
    """
    def creaBotones(self):
        botonAbrir = Button(self,text="Cargar engine",command=self.buscaEngine)
        botonAbrir.place(x=10,y=10)
        
        botonSalir = Button(self,text="Salir",command=self.salir)
        botonSalir.place(x=150,y=10)

    def buscaEngine(self):
        ruta = tkFileDialog.askopenfilename()
        self.engine = cargaEngine(ruta)
        print (self.engine.name)

    """
    Borra el archivo png del tablero generado por el programa
    Y se sale del programa
    """
    def salir(self):
        try:
            os.remove("tablero.png")
            os._exit(0)
        except OSError:
            os._exit(0)

"""
Main del programa
Crea una ventana y manda a llamar al constructor de la clase
Para poder interactuar con las acciones que se puedan realizar
"""
if __name__=="__main__":
    root = Tk()
    root.geometry("920x500")
    root.title("Jugar contra un Engine")
    root.wm_state("normal")
    app = Interfaz(root)
    root.mainloop()
