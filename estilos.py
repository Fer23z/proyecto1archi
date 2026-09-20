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


# --- LÓGICA---

def cargar_configuracion(ruta_archivo):
    ruta = ruta_archivo

    if not os.path.exists(ruta):
        messagebox.showinfo("Archivo Ausente",
                            f"No se encontró el archivo '{ruta}'.\nSe iniciará con los valores por defecto.")
        return DEFAULT_CONFIG.copy()

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in DEFAULT_CONFIG:
                if key not in data:
                    data[key] = DEFAULT_CONFIG[key]
            return data

    except json.JSONDecodeError:
        messagebox.showerror("Error de Formato",
                             f"El archivo '{ruta}' está corrupto o tiene un formato inválido.\nSe usarán los valores por defecto para evitar caídas.")
        return DEFAULT_CONFIG.copy()

    except PermissionError:
        messagebox.showerror("Error de Permisos",
                             f"No tienes permisos de lectura para el archivo '{ruta}'.\nSe usarán valores por defecto.")
        return DEFAULT_CONFIG.copy()

    except Exception as e:
        messagebox.showerror("Error Inesperado",
                             f"Ocurrió un error al cargar: {str(e)}\nSe usarán valores por defecto.")
        return DEFAULT_CONFIG.copy()


def guardar_configuracion(nueva_config):

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as original, \
                    open(BACKUP_FILE, "w", encoding="utf-8") as backup:
                for linea in original:
                    backup.write(linea)
        except PermissionError:
            messagebox.showerror("Error de Permisos",
                                 f"No hay permisos para modificar el archivo de respaldo en '{BACKUP_FILE}'.")
            return False
        except Exception as e:
            messagebox.showerror("Error de Respaldo", f"Error al actualizar respaldo: {str(e)}")
            return False

    try:
        with open(TEMP_FILE, "w", encoding="utf-8") as temporal:
            json.dump(nueva_config, temporal, indent=4, ensure_ascii=False)
    except PermissionError:
        messagebox.showerror("Error de Permisos", f"No hay permisos para escribir el archivo temporal '{TEMP_FILE}'.")
        return False
    except Exception as e:
        messagebox.showerror("Error de Escritura", f"Error durante la escritura del temporal: {str(e)}")
        return False

    try:
        os.replace(TEMP_FILE, CONFIG_FILE)
        return True
    except PermissionError:
        messagebox.showerror("Error de Permisos", f"No hay permisos para reemplazar el archivo final '{CONFIG_FILE}'.")
        return False
    except Exception as e:
        messagebox.showerror("Error al Reemplazar", f"Error al guardar el archivo final: {str(e)}")
        return False


# --- INTERFAZ GRÁFICA ---

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, current_config, callback_guardado):
        super().__init__(parent)
        self.geometry("500x600")
        self.current_config = current_config.copy()
        self.callback_guardado = callback_guardado

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.lbl_name = ctk.CTkLabel(self)
        self.lbl_name.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.insert(0, self.current_config["nombre_usuario"])
        self.entry_nombre.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_theme = ctk.CTkLabel(self)
        self.lbl_theme.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.combo_tema = ctk.CTkComboBox(self, values=["claro", "oscuro"])
        self.combo_tema.set(self.current_config["tema"])
        self.combo_tema.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_lang = ctk.CTkLabel(self)
        self.lbl_lang.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.combo_idioma = ctk.CTkComboBox(self, values=["es/es-ES", "en/en-US"], command=self.actualizar_textos)
        self.combo_idioma.set(self.current_config["idioma"])
        self.combo_idioma.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_font = ctk.CTkLabel(self)
        self.lbl_font.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.entry_fuente = ctk.CTkEntry(self)
        self.entry_fuente.insert(0, str(self.current_config["tamano_fuente"]))
        self.entry_fuente.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_menu_color = ctk.CTkLabel(self)
        self.lbl_menu_color.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.btn_color_menu = ctk.CTkButton(self, fg_color=self.current_config["color_menu"],
                                            command=self.elegir_color_menu)
        self.btn_color_menu.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_text_color = ctk.CTkLabel(self)
        self.lbl_text_color.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.btn_color_letra = ctk.CTkButton(self, fg_color=self.current_config["color_letra"],
                                             command=self.elegir_color_letra)
        self.btn_color_letra.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_pic = ctk.CTkLabel(self)
        self.lbl_pic.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.btn_foto = ctk.CTkButton(self, command=self.elegir_foto_perfil)
        self.btn_foto.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.lbl_ruta_foto = ctk.CTkLabel(self, text=self.current_config["foto_perfil"] or "Ninguna",
                                          font=("Arial", 10))
        self.lbl_ruta_foto.grid(row=7, column=1, padx=20, pady=0, sticky="ew")

        self.btn_guardar = ctk.CTkButton(self, command=self.guardar_ajustes, fg_color="green", hover_color="darkgreen")
        self.btn_guardar.grid(row=8, column=0, columnspan=2, padx=20, pady=30, sticky="ew")

        self.actualizar_textos()

        self.transient(parent)
        self.grab_set()

    def actualizar_textos(self, event=None):
        lang = self.combo_idioma.get()
        t = TRANSLATIONS.get(lang, TRANSLATIONS["es/es-ES"])

        self.title(t["title_settings"])
        self.lbl_name.configure(text=t["lbl_name"])
        self.lbl_theme.configure(text=t["lbl_theme"])
        self.lbl_lang.configure(text=t["lbl_lang"])
        self.lbl_font.configure(text=t["lbl_font"])
        self.lbl_menu_color.configure(text=t["lbl_menu_color"])
        self.lbl_text_color.configure(text=t["lbl_text_color"])
        self.lbl_pic.configure(text=t["lbl_pic"])
        self.btn_color_menu.configure(text=t["btn_color"])
        self.btn_color_letra.configure(text=t["btn_color"])
        self.btn_foto.configure(text=t["btn_img"])
        self.btn_guardar.configure(text=t["btn_save"])

        # Traducir el texto de "Ninguna" o "None" si no hay foto
        if self.lbl_ruta_foto.cget("text") in ["Ninguna", "None"]:
            self.lbl_ruta_foto.configure(text=t["lbl_none"])

    def elegir_color_menu(self):
        color_code = colorchooser.askcolor(title="Elige color de menú", initialcolor=self.current_config["color_menu"])[
            1]
        if color_code:
            self.current_config["color_menu"] = color_code
            self.btn_color_menu.configure(fg_color=color_code)

    def elegir_color_letra(self):
        color_code = \
        colorchooser.askcolor(title="Elige color de letra", initialcolor=self.current_config["color_letra"])[1]
        if color_code:
            self.current_config["color_letra"] = color_code
            self.btn_color_letra.configure(fg_color=color_code)

    def elegir_foto_perfil(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Foto de Perfil",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.current_config["foto_perfil"] = file_path
            self.lbl_ruta_foto.configure(text=file_path)

    def guardar_ajustes(self):
        try:
            fuente_int = int(self.entry_fuente.get())
            if fuente_int <= 0: raise ValueError
            self.current_config["tamano_fuente"] = fuente_int
        except ValueError:
            messagebox.showerror("Error de Formato", "El tamaño de fuente debe ser un número entero positivo.")
            return

        self.current_config["nombre_usuario"] = self.entry_nombre.get()
        self.current_config["tema"] = self.combo_tema.get()
        self.current_config["idioma"] = self.combo_idioma.get()

        if guardar_configuracion(self.current_config):
            messagebox.showinfo("Éxito",
                                f"Configuración guardada exitosamente en:\n{CONFIG_FILE}\n\nRespaldo (.bak) actualizado en la carpeta del programa.")
            self.callback_guardado(self.current_config)
            self.destroy()
