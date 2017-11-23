import chess
import chess.uci
import chess.svg
import cairo
import rsvg

def inicializaTablero():
    board = chess.Board()
    return board

def cargaEngine(nombre):
    engine = chess.uci.popen_engine(nombre)
    engine.uci()
    return engine

"""
Se obtiene la representacion del tablero en formato svg
"""
def obtenSvg(tablero):
    svg = chess.svg.board(board=tablero)
    return svg


"""
Convierte un archivo SVG a uno PNG
"""
def svgToImage(svg,nombre):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)
    ctx = cairo.Context(img)
    handle= rsvg.Handle(None, str(svg))
    handle.render_cairo(ctx)
    img.write_to_png(nombre+".png")
