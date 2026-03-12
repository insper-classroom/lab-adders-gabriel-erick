#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        if a and b:
            soma.next = 0
            carry.next = 1
        elif not a and not b:
            soma.next = 0
            carry.next = 0
        else:
            soma.next = 1
            carry.next = 0
        
    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(4)]

    half_1 = halfAdder(a, b, s[1], s[2]) 
    half_2 = halfAdder(c, s[1], soma, s[3])

    @always_comb
    def comb():
        carry.next = s[2] | s[3]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    """Somador de 2 bits.

    Implementacao esperada com dois full adders, gerando
    uma soma de 2 bits e carry final.

    Args:
        x: Vetor de entrada de 2 bits.
        y: Vetor de entrada de 2 bits.
        soma: Vetor de saida de 2 bits.
        carry: Carry de saida.
    """
    s1 = Signal(bool(0))
    s2 = Signal(bool(0))
    
    fa1 = fullAdder(x[0], y[0], s2, soma[0], s1)
    fa2 = fullAdder(x[1], y[1], s1, soma[1], carry)

    return instances()


@block
def adder(x, y, soma, carry):
    s = [Signal(bool(0)) for i in range(len(x) - 1)]
    hallist = [None for i in range(len(x))]
    hallist[0] = halfAdder(x[0], y[0], soma[0], s[0]),

    for e in range(1, len(x)- 1):
        hallist[e] = fullAdder(x[e], y[e], s[e-1], soma[e], s[e])
    hallist[-1] = fullAdder(x[-1], y[-1], s[-1], soma[-1], carry)
    return instances()


@block
def addervb(x, y, soma, carry):

    @always_comb
    def comb():
        total = int(x) + int(y)
        soma.next = total & ((1 << len(x)) - 1)
        carry.next = (total >> len(x)) & 1

    return instances()