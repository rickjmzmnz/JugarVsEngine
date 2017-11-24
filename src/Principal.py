# -*- coding: utf-8 -*- 

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
        self.canvas.place(x=10,y=10)
        self.tablero = inicializaTablero()
        self.colocaTab()
        
    """
    Se crean los botones para las diferentes acciones de la interfaz
    """
    def creaBotones(self):
        botonAbrir = Button(self,text="Cargar engine",command=self.buscaEngine)
        botonAbrir.place(x=10,y=460)
        
        botonSalir = Button(self,text="Salir",command=self.salir)
        botonSalir.place(x=170,y=460)

        self.et = Label(self,text="Carga un engine para mostrar más opciones")
        self.et.place(x=80,y=430)

    """
    Busca el engine que será el rival a vencer en la partida
    """
    def buscaEngine(self):
        ruta = tkFileDialog.askopenfilename()
        self.engine = cargaEngine(ruta)

        self.et.config(text="Elige con cuales piezas jugará el engine")
        
        self.botonNegras = Button(self,text="Engine juega negras",command=self.juegaNegras)
        self.botonNegras.place(x=10,y=510)

        self.botonBlancas = Button(self,text="Engine juega blancas",command=self.juegaBlancas)
        self.botonBlancas.place(x=170,y=510)

    """
    Inicia la partida el engine
    """
    def juegaBlancas(self):
        self.botonBlancas.place_forget()
        self.botonNegras.place_forget()
        self.et.config(text="Empieza la partida")
        mov = juegaEngine(self.tablero,self.engine)
        siguienteJugadaEng(self.tablero,mov)
        self.colocaTab()
        self.juegaPersona()

    """
    Inicia la partida el jugador
    """
    def juegaNegras(self):
        self.botonBlancas.place_forget()
        self.botonNegras.place_forget()
        self.et.config(text="Empieza la partida")
        self.juegaPersona()
        self.colocaTab()

    """
    Coloca la caja de texto donde el jugador va a indicar su jugada
    """
    def juegaPersona(self):
        self.etPer = Label(self,text="Escoge tu jugada")
        self.etPer.place(x=10,y=510)
        self.entrytext = StringVar()
        self.entry = Entry(self,textvariable=self.entrytext)
        self.entry.place(x=120,y=510)
        self.botonPer = Button(self,text="Mover",command= lambda: self.aplicaJugadaPer(self.entrytext))
        self.botonPer.place(x=280,y=510)

    """
    Función para aplicar la jugada que el jugador colocó en la caja de texto
    """
    def aplicaJugadaPer(self,mov):
        mov = mov.get()
        self.etPer.place_forget()
        self.entry.place_forget()
        self.botonPer.place_forget()
        siguienteJugadaPer(self.tablero,mov)
        self.colocaTab()
        self.tocaEng()

    def tocaEng(self):
        self.botonMueveEng = Button(self,text="Te toca engine",command=self.mueveEng)
        self.botonMueveEng.place(x=10,y=510)

    """
    Función para que el engine realice una jugada
    """
    def mueveEng(self):
        mov = juegaEngine(self.tablero,self.engine)
        siguienteJugadaEng(self.tablero,mov)
        self.colocaTab()
        self.botonMueveEng.place_forget()
        self.juegaPersona()
        jaque = verificaJaque(self.tablero)
        jaquemate = verificaJaqueMate(self.tablero)
        tablas = verificaTablas(self.tablero)
        if(jaquemate == True):
            self.mensajeJaqueMate()
            return 
        if(jaque == True):
            self.mensajeJaque()
        if(tablas == True):
            self.mensajeTablas()

    """
    Dibuja el tablero en el canvas con el estado del juego actual
    """
    def colocaTab(self):
        svg = obtenSvg(self.tablero)
        svgToImage(svg,"tablero")
        imagen = Image.open("tablero.png")
        imagenTk = ImageTk.PhotoImage(imagen)
        self.canvas.image = imagenTk
        self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")

    """
    Ventana emergente para informar que hay jaque
    """
    def mensajeJaque(self):
        top = Toplevel()
        top.geometry("%dx%d%+d%+d" % (170, 80, 600, 300))
        label = Label(top,text="¡JAQUE!, Mueve el rey")
        label.place(x=20,y=20)

    """
    Ventana emergente para informar que hay jaquemate
    """
    def mensajeJaqueMate(self):
        top = Toplevel()
        top.geometry("%dx%d%+d%+d" % (170, 80, 600, 300))
        label = Label(top,text="¡JAQUEMATE!, Fin del juego")
        label.place(x=20,y=20)

    """
    Ventana emergente para informar que hay tablas
    """
    def mensajeTablas(self):
        top = Toplevel()
        top.geometry("%dx%d%+d%+d" % (170, 80, 600, 300))
        label = Label(top,text="¡TABLAS!, Es un empate")
        label.place(x=20,y=20)
        
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
    root.geometry("420x580")
    root.title("Jugar contra un Engine")
    root.wm_state("normal")
    app = Interfaz(root)
    root.mainloop()
