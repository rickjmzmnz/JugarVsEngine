import chess
import chess.uci
import chess.svg
import cairo
import rsvg
import types

def inicializaTablero():
    board = chess.Board()
    return board

def cargaEngine(nombre):
    engine = chess.uci.popen_engine(nombre)
    engine.uci()
    return engine

def juegaEngine(tablero,engine):
    engine.position(tablero)
    command = engine.go(movetime=2000,async_callback=True)
    mejor, reflexionar = command.result()
    return mejor

def siguienteJugadaEng(tablero,mov):
    tablero.push(mov)

def siguienteJugadaPer(tablero,mov):
    move = chess.Move.from_uci(mov)
    tablero.push(move)

def verificaJaque(tablero):
    return tablero.is_check()
    
def verificaJaqueMate(tablero):
    return tablero.is_checkmate()

def verificaTablas(tablero):
    return tablero.is_stalemate()

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
