# -*- coding: utf-8 -*- 

import chess
import chess.uci
import chess.svg
import cairo
import rsvg
import types

"""
Función para crear un tablero con una partida inicial
"""
def inicializaTablero():
    board = chess.Board()
    return board

"""
Función para inicializar el engine
"""
def cargaEngine(nombre):
    engine = chess.uci.popen_engine(nombre)
    engine.uci()
    return engine

"""
Dado un tablero y un engine
El engine revisa el tablera y realiza la mejor jugada
"""
def juegaEngine(tablero,engine):
    engine.position(tablero)
    command = engine.go(movetime=2000,async_callback=True)
    mejor, reflexionar = command.result()
    return mejor

"""
Dado un tablero y el movimiento del engine
Coloca en el tablero la jugada realizada por el engine 
"""
def siguienteJugadaEng(tablero,mov):
    tablero.push(mov)

"""
Dado un tablero y el movimiento del jugador
Coloca en el tablero la jugada realizada por el jugador 
"""
def siguienteJugadaPer(tablero,mov):
    move = chess.Move.from_uci(mov)
    tablero.push(move)

"""
Dado un tablero se verifica si hay jaque
"""
def verificaJaque(tablero):
    return tablero.is_check()

"""
Dado un tablero se verifica si hay jaquemate
"""
def verificaJaqueMate(tablero):
    return tablero.is_checkmate()

"""
Dado un tablero se verifica si hay tablas
"""
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
