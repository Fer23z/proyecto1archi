import os
import json
from tkinter import filedialog, colorchooser, messagebox
import customtkinter as ctk
from PIL import Image, UnidentifiedImageError

PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(PROGRAM_DIR, "estilos.json")
TEMP_FILE = os.path.join(PROGRAM_DIR, "estilos.tmp")
BACKUP_FILE = os.path.join(PROGRAM_DIR, "estilos.bak")

DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario Estudiante",
    "tema": "oscuro",
    "idioma": "es/es-ES",
    "tamano_fuente": 14,
    "color_menu": "#1F6AA5",
    "color_letra": "#FFFFFF",
    "foto_perfil": ""
}

TRANSLATIONS = {
    "es/es-ES": {
        "title_main": "Aplicación de Gestión de Archivos",
        "menu_file": "Archivo",
        "menu_edit": "Edición",
        "menu_view": "Ver",
        "welcome": "¡Bienvenido(a), {name}!\nIdioma actual: {lang}",
        "no_pic": "[Sin Foto de Perfil]",
        "invalid_pic": "[Imagen Inválida]",
        "error_pic": "[Error al cargar imagen]",
        "title_settings": "Configuración (Settings)",
        "lbl_name": "Nombre de Usuario:",
        "lbl_theme": "Tema de Interfaz:",
        "lbl_lang": "Idioma:",
        "lbl_font": "Tamaño de Fuente:",
        "lbl_menu_color": "Color Barra de Menú:",
        "lbl_text_color": "Color de Letra:",
        "lbl_pic": "Foto de Perfil:",
        "btn_color": "Elegir Color",
        "btn_img": "Seleccionar Imagen",
        "btn_save": "Guardar Cambios",
        "lbl_none": "Ninguna",
        "sim_file": "Simulado: Archivo",
        "sim_edit": "Simulado: Edición",
        "sim_view": "Simulado: Ver"
    },
    "en/en-US": {
        "title_main": "File Management Application",
        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_view": "View",
        "welcome": "Welcome, {name}!\nCurrent language: {lang}",
        "no_pic": "[No Profile Picture]",
        "invalid_pic": "[Invalid Image]",
        "error_pic": "[Error loading image]",
        "title_settings": "Configuration (Settings)",
        "lbl_name": "Username:",
        "lbl_theme": "Interface Theme:",
        "lbl_lang": "Language:",
        "lbl_font": "Font Size:",
        "lbl_menu_color": "Menu Bar Color:",
        "lbl_text_color": "Text Color:",
        "lbl_pic": "Profile Picture:",
        "btn_color": "Choose Color",
        "btn_img": "Select Image",
        "btn_save": "Save Changes",
        "lbl_none": "None",
        "sim_file": "Simulated: File",
        "sim_edit": "Simulated: Edit",
        "sim_view": "Simulated: View"
    }
}
