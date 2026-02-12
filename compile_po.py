#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script per compilare file .po in .mo usando polib
"""

import polib

if __name__ == '__main__':
    po_file = 'locale/en/LC_MESSAGES/django.po'
    mo_file = 'locale/en/LC_MESSAGES/django.mo'
    
    print(f"Compilazione {po_file} -> {mo_file}")
    
    # Carica il file .po
    po = polib.pofile(po_file)
    
    print(f"Trovati {len(po)} messaggi")
    
    # Salva come .mo
    po.save_as_mofile(mo_file)
    
    print(f"File .mo creato: {mo_file}")
    print("Completato!")
