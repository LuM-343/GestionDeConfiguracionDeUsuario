import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import os
from PIL import Image, ImageTk
import configManager as cm
# Voy a soñar con una interfaz, espero mañana este aqui.
# Salvame chusito
# No aparecio la condenada Interfaz, una tristeza.

# ==============================================================================
# Paleta de Colores y Fuentes
# ==============================================================================
AMARILLO_CHILLANTE = "#FFE600"         
FONDO = "#FFFFFF"    
CONTORNOS = "#000000"     
BOTONES = "#00E5FF"     
ROJAZO = "#FF2A2A"
GRIS_RESET = "#E0E0E0"     
FUENTE_TITULO = ("Courier New", 14, "bold")
FUENTE_NEGRITA = ("Arial Black", 10)
FUENTE_CUERPO = ("Courier New", 10, "bold")

# Diccionario multilingüe real
DICCIONARIO_IDIOMAS = {
    "es": {
        "menu_file": "[ARCHIVO]",
        "menu_edit": "[EDICION]",
        "menu_view": "[VER]",
        "menu_settings": "CONFIGURACIÓN",
        "sim_new": "> NUEVO",
        "sim_open": "> ABRIR",
        "sim_exit": "> SALIR",
        "sim_undo": "> DESHACER",
        "sim_cut": "> CORTAR",
        "sim_copy": "> COPIAR",
        "sim_paste": "> PEGAR",
        "sim_statusbar": "> BARRA DE ESTADO",
        "panel_title": "// ESTADO DEL SISTEMA",
        "welcome": "USUARIO: {usuario}",
        "theme_lbl": "TEMA: {tema}",
        "lang_lbl": "IDIOMA: {idioma}",
        "font_lbl": "TAMAÑO FUENTE: {tamano} PT",
        "photo_lbl": "AVATAR: {foto}",
        "saved_ok": "CONFIGURACIÓN PERSISTIDA CORRECTAMENTE (.BAK OK)",
        "saved_err": "ERROR CRÍTICO AL ESCRIBIR EN DISCO",
        "sim_msg": "SIMULACIÓN COORECTA DE: {opc}",
        "btn_default": "[POR DEFECTO]",
        # Textos de la ventana de configuración
        "cfg_win_title": "CONFIGURACIÓN DE INTERFAZ - PROYECTO 1",
        "cfg_banner": "[ PANEL DE CONTROL :: EDICIÓN ]",
        "cfg_lbl_user": "1. USUARIO [UTF-8]:",
        "cfg_lbl_theme": "2. TEMA UI:",
        "cfg_lbl_lang": "3. IDIOMA:",
        "cfg_lbl_font": "4. TAMAÑO FUENTE:",
        "cfg_lbl_menu_color": "5. COLOR BARRA:",
        "cfg_lbl_text_color": "6. COLOR TEXTO:",
        "cfg_lbl_photo": "7. FOTO PERFIL:",
        "cfg_btn_color": "ELEGIR COLOR",
        "cfg_btn_browse": "EXPLORAR...",
        "cfg_not_assigned": "NO ASIGNADA",
        "cfg_btn_cancel": "CANCELAR [X]",
        "cfg_btn_save": "GUARDAR [✔]",
        "cfg_err_font_title": "ERROR DE TIPO",
        "cfg_err_font_msg": "EL TAMAÑO DE FUENTE DEBE SER UN ENTERO.",
        "dlg_color_menu": "SELECCIONAR COLOR DE BARRA",
        "dlg_color_text": "SELECCIONAR COLOR DE LETRA",
        "dlg_photo": "SELECCIONAR FOTO DE PERFIL"
    },
    "en": {
        "menu_file": "[FILE]",
        "menu_edit": "[EDIT]",
        "menu_view": "[VIEW]",
        "menu_settings": "SETTINGS",
        "sim_new": "> NEW",
        "sim_open": "> OPEN",
        "sim_exit": "> EXIT",
        "sim_undo": "> UNDO",
        "sim_cut": "> CUT",
        "sim_copy": "> COPY",
        "sim_paste": "> PASTE",
        "sim_statusbar": "> STATUS BAR",
        "panel_title": "// SYSTEM STATUS",
        "welcome": "USER: {usuario}",
        "theme_lbl": "THEME: {tema}",
        "lang_lbl": "LANG: {idioma}",
        "font_lbl": "FONT SIZE: {tamano} PT",
        "photo_lbl": "AVATAR: {foto}",
        "saved_ok": "CONFIG PERSISTED SUCCESSFULLY (.BAK OK)",
        "saved_err": "CRITICAL ERROR SAVING CONFIGURATION",
        "sim_msg": "SUCCESS SIMULATION OF: {opc}",
        "btn_default": "[RESET / DEFAULTS]",
        # Textos de la ventana de configuración
        "cfg_win_title": "INTERFACE SETTINGS - PROJECT 1",
        "cfg_banner": "[ CONTROL PANEL :: EDITING ]",
        "cfg_lbl_user": "1. USER [UTF-8]:",
        "cfg_lbl_theme": "2. UI THEME:",
        "cfg_lbl_lang": "3. LANGUAGE:",
        "cfg_lbl_font": "4. FONT SIZE:",
        "cfg_lbl_menu_color": "5. BAR COLOR:",
        "cfg_lbl_text_color": "6. TEXT COLOR:",
        "cfg_lbl_photo": "7. PROFILE PIC:",
        "cfg_btn_color": "CHOOSE COLOR",
        "cfg_btn_browse": "BROWSE...",
        "cfg_not_assigned": "NOT ASSIGNED",
        "cfg_btn_cancel": "CANCEL [X]",
        "cfg_btn_save": "SAVE [✔]",
        "cfg_err_font_title": "TYPE ERROR",
        "cfg_err_font_msg": "FONT SIZE MUST BE AN INTEGER.",
        "dlg_color_menu": "SELECT BAR COLOR",
        "dlg_color_text": "SELECT TEXT COLOR",
        "dlg_photo": "SELECT PROFILE PICTURE"
    }
}

def obtener_textos(codigo_idioma):
    codigo = str(codigo_idioma).lower()
    if "en" in codigo:
        return DICCIONARIO_IDIOMAS["en"]
    return DICCIONARIO_IDIOMAS["es"]


# ==============================================================================
# VENTANA DE CONFIGURACIÓN
# ==============================================================================
class VentanaConfig(tk.Toplevel):
    def __init__(self, parent, config_actual, callback_guardado):
        super().__init__(parent)
        self.parent = parent
        self.config_actual = config_actual
        self.callback_guardado = callback_guardado

        self.idioma_activo = self.config_actual.get("idioma", "es")
        self.tema_activo = self.config_actual.get("tema_interfaz", "claro")
        self.t = obtener_textos(self.idioma_activo)

        # Paleta dinámica de la ventana de configuración según el tema
        if self.tema_activo == "oscuro":
            self.c_bg_base = "#121212"
            self.c_bg_panel = "#1E1E1E"
            self.c_fg = "#FFFFFF"
            self.c_borde = AMARILLO_CHILLANTE
            self.c_entry_bg = "#2A2A2A"
            self.c_btn_bg = "#2A2A2A"
        else:
            self.c_bg_base = AMARILLO_CHILLANTE
            self.c_bg_panel = FONDO
            self.c_fg = CONTORNOS
            self.c_borde = CONTORNOS
            self.c_entry_bg = "#FFFFFF"
            self.c_btn_bg = FONDO

        self.title(self.t["cfg_win_title"])
        self.geometry("500x560")
        self.resizable(False, False)
        self.configure(bg=self.c_bg_base)
        self.transient(parent)
        self.grab_set()

        # Variables vinculadas a campos requeridos
        self.var_usuario = tk.StringVar(value=self.config_actual.get("nombre_usuario", "Usuario"))
        self.var_tema = tk.StringVar(value=self.tema_activo)
        self.var_idioma = tk.StringVar(value=self.idioma_activo)
        self.var_fuente = tk.IntVar(value=self.config_actual.get("tamano_fuente", 10))
        self.var_color_menu = tk.StringVar(value=self.config_actual.get("color_barra_menu", "#000000"))
        self.var_color_letra = tk.StringVar(value=self.config_actual.get("color_letra", "#000000"))
        self.var_foto = tk.StringVar(value=self.config_actual.get("foto_perfil", ""))

        self._construir_ui()

    def _construir_ui(self):
        lbl_banner = tk.Label(
            self,
            text=self.t["cfg_banner"],
            bg=CONTORNOS,
            fg="#FFFFFF",
            font=FUENTE_TITULO,
            pady=8
        )
        lbl_banner.pack(fill=tk.X)

        contenedor = tk.Frame(self, bg=self.c_bg_panel, highlightthickness=3, highlightbackground=self.c_borde)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        filas = [
            (self.t["cfg_lbl_user"], self._widget_usuario),
            (self.t["cfg_lbl_theme"], self._widget_tema),
            (self.t["cfg_lbl_lang"], self._widget_idioma),
            (self.t["cfg_lbl_font"], self._widget_fuente),
            (self.t["cfg_lbl_menu_color"], self._widget_color_menu),
            (self.t["cfg_lbl_text_color"], self._widget_color_letra),
            (self.t["cfg_lbl_photo"], self._widget_foto)
        ]

        for idx, (etiqueta, fn_creador) in enumerate(filas):
            lbl = tk.Label(
                contenedor,
                text=etiqueta,
                bg=self.c_bg_panel,
                fg=self.c_fg,
                font=FUENTE_CUERPO,
                anchor="w"
            )
            lbl.grid(row=idx, column=0, sticky="w", padx=12, pady=6)
            fn_creador(contenedor, idx)

        contenedor.columnconfigure(1, weight=1)

        f_bot = tk.Frame(self, bg=self.c_bg_base)
        f_bot.pack(side=tk.BOTTOM, fill=tk.X, padx=14, pady=10)

        self.btn_default = tk.Button(
            f_bot,
            text=self.t["btn_default"],
            font=FUENTE_NEGRITA,
            bg=GRIS_RESET,
            fg=CONTORNOS,
            relief=tk.SOLID,
            bd=3,
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._restablecer_por_defecto
        )
        self.btn_default.pack(side=tk.LEFT)

        btn_cancelar = tk.Button(
            f_bot,
            text=self.t["cfg_btn_cancel"],
            font=FUENTE_NEGRITA,
            bg=ROJAZO,
            fg="#FFFFFF",
            relief=tk.SOLID,
            bd=3,
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.destroy
        )
        btn_cancelar.pack(side=tk.RIGHT, padx=4)

        btn_guardar = tk.Button(
            f_bot,
            text=self.t["cfg_btn_save"],
            font=FUENTE_NEGRITA,
            bg=BOTONES,
            fg=CONTORNOS,
            relief=tk.SOLID,
            bd=3,
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._guardar
        )
        btn_guardar.pack(side=tk.RIGHT, padx=4)

    def _validar_tamano_usuario(self, nuevo_texto):
        return len(nuevo_texto) <= 30

    def _widget_usuario(self, parent, r):
        vcmd = (self.register(self._validar_tamano_usuario), "%P")
        entry = tk.Entry(
            parent,
            textvariable=self.var_usuario,
            font=FUENTE_CUERPO,
            relief=tk.SOLID,
            bd=2,
            bg=self.c_entry_bg,
            fg=self.c_fg,
            insertbackground=self.c_fg,
            validate="key",
            validatecommand=vcmd
        )
        entry.grid(row=r, column=1, sticky="ew", padx=12, pady=6)

    def _widget_tema(self, parent, r):
        f = tk.Frame(parent, bg=self.c_bg_panel)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        for t in ["claro", "oscuro"]:
            tk.Radiobutton(
                f,
                text=t.upper(),
                value=t,
                variable=self.var_tema,
                bg=self.c_bg_panel,
                fg=self.c_fg,
                selectcolor=self.c_entry_bg,
                font=FUENTE_CUERPO,
                activebackground=self.c_bg_panel,
                activeforeground=self.c_fg
            ).pack(side=tk.LEFT, padx=4)

    def _widget_idioma(self, parent, r):
        f = tk.Frame(parent, bg=self.c_bg_panel)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        for i in ["es", "en"]:
            tk.Radiobutton(
                f,
                text=i.upper(),
                value=i,
                variable=self.var_idioma,
                bg=self.c_bg_panel,
                fg=self.c_fg,
                selectcolor=self.c_entry_bg,
                font=FUENTE_CUERPO,
                activebackground=self.c_bg_panel,
                activeforeground=self.c_fg
            ).pack(side=tk.LEFT, padx=4)

    def _widget_fuente(self, parent, r):
        spin = tk.Spinbox(
            parent,
            from_=8,
            to=30,
            textvariable=self.var_fuente,
            font=FUENTE_CUERPO,
            relief=tk.SOLID,
            bd=2,
            width=6,
            bg=self.c_entry_bg,
            fg=self.c_fg,
            buttonbackground=self.c_btn_bg
        )
        spin.grid(row=r, column=1, sticky="w", padx=12, pady=6)

    def _widget_color_menu(self, parent, r):
        f = tk.Frame(parent, bg=self.c_bg_panel)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        self.prev_menu = tk.Label(f, width=4, relief=tk.SOLID, bd=2, bg=self.var_color_menu.get())
        self.prev_menu.pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            f, text=self.t["cfg_btn_color"], font=FUENTE_CUERPO, relief=tk.SOLID, bd=2,
            bg=self.c_btn_bg, fg=self.c_fg, cursor="hand2", command=self._seleccionar_color_menu
        ).pack(side=tk.LEFT)

    def _widget_color_letra(self, parent, r):
        f = tk.Frame(parent, bg=self.c_bg_panel)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        self.prev_letra = tk.Label(f, width=4, relief=tk.SOLID, bd=2, bg=self.var_color_letra.get())
        self.prev_letra.pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            f, text=self.t["cfg_btn_color"], font=FUENTE_CUERPO, relief=tk.SOLID, bd=2,
            bg=self.c_btn_bg, fg=self.c_fg, cursor="hand2", command=self._seleccionar_color_letra
        ).pack(side=tk.LEFT)

    def _widget_foto(self, parent, r):
        f = tk.Frame(parent, bg=self.c_bg_panel)
        f.grid(row=r, column=1, sticky="ew", padx=12, pady=6)
        self.lbl_foto = tk.Label(
            f,
            text=os.path.basename(self.var_foto.get()) or self.t["cfg_not_assigned"],
            font=("Courier New", 9),
            bg=self.c_entry_bg,
            fg=self.c_fg,
            relief=tk.SOLID,
            bd=1,
            width=14,
            anchor="w"
        )
        self.lbl_foto.pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            f, text=self.t["cfg_btn_browse"], font=FUENTE_CUERPO, relief=tk.SOLID, bd=2,
            bg=self.c_btn_bg, fg=self.c_fg, cursor="hand2", command=self._seleccionar_foto
        ).pack(side=tk.LEFT)

    def _seleccionar_color_menu(self):
        c = colorchooser.askcolor(self.var_color_menu.get(), title=self.t["dlg_color_menu"])
        if c[1]:
            self.var_color_menu.set(c[1])
            self.prev_menu.configure(bg=c[1])

    def _seleccionar_color_letra(self):
        c = colorchooser.askcolor(self.var_color_letra.get(), title=self.t["dlg_color_text"])
        if c[1]:
            self.var_color_letra.set(c[1])
            self.prev_letra.configure(bg=c[1])

    def _seleccionar_foto(self):
        r = filedialog.askopenfilename(
            title=self.t["dlg_photo"],
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Todos", "*.*")]
        )
        if r:
            self.var_foto.set(r)
            self.lbl_foto.configure(text=os.path.basename(r))

    def _restablecer_por_defecto(self):
        defaults = getattr(cm, "configuracionPorDefecto", {
            "nombre_usuario": "Usuario",
            "tema_interfaz": "claro",
            "idioma": "es",
            "tamano_fuente": 12,
            "color_barra_menu": "#000000",
            "color_letra": "#000000",
            "foto_perfil": ""
        })

        self.var_usuario.set(defaults.get("nombre_usuario", "Usuario")[:30])
        self.var_tema.set(defaults.get("tema_interfaz", "claro"))
        self.var_idioma.set(defaults.get("idioma", "es"))
        self.var_fuente.set(defaults.get("tamano_fuente", 10))
        self.var_color_menu.set(defaults.get("color_barra_menu", "#000000"))
        self.var_color_letra.set(defaults.get("color_letra", "#000000"))
        self.var_foto.set(defaults.get("foto_perfil", ""))

        self.prev_menu.configure(bg=self.var_color_menu.get())
        self.prev_letra.configure(bg=self.var_color_letra.get())
        self.lbl_foto.configure(text=os.path.basename(self.var_foto.get()) or self.t["cfg_not_assigned"])

    def _guardar(self):
        try:
            fuente_val = int(self.var_fuente.get())
        except ValueError:
            messagebox.showerror(self.t["cfg_err_font_title"], self.t["cfg_err_font_msg"])
            return

        nueva_cfg = {
            "nombre_usuario": self.var_usuario.get(),
            "tema_interfaz": self.var_tema.get(),
            "idioma": self.var_idioma.get(),
            "tamano_fuente": fuente_val,
            "color_barra_menu": self.var_color_menu.get(),
            "color_letra": self.var_color_letra.get(),
            "foto_perfil": self.var_foto.get()
        }

        if cm.escribirConfiguracion(nueva_cfg):
            t_nuevo = obtener_textos(nueva_cfg["idioma"])
            messagebox.showinfo("ESTADO DE PERSISTENCIA", t_nuevo["saved_ok"])
            self.callback_guardado(nueva_cfg)
            self.destroy()
        else:
            messagebox.showerror("ERROR DE ARCHIVO", self.t["saved_err"])


# ==============================================================================
# VENTANA PRINCIPAL
# ==============================================================================
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GESTIÓN DE ARCHIVOS - PROYECTO 1")
        self.geometry("700x500")
        self.minsize(580, 420)

        self.imagen_avatar = None
        self.config = cm.leerConfiguracion()

        self._crear_estructura()
        self.aplicar_cambios_visuales()

    def _crear_estructura(self):
        # 1. Barra de menús modular
        self.frame_menu = tk.Frame(self, relief=tk.SOLID, bd=3)
        self.frame_menu.pack(side=tk.TOP, fill=tk.X)

        self.mb_archivo = tk.Menubutton(self.frame_menu, relief=tk.SOLID, bd=2)
        self.m_archivo = tk.Menu(self.mb_archivo, tearoff=0, bd=2, relief=tk.SOLID)
        self.mb_archivo.configure(menu=self.m_archivo)
        self.mb_archivo.pack(side=tk.LEFT, padx=3, pady=3)

        self.mb_edicion = tk.Menubutton(self.frame_menu, relief=tk.SOLID, bd=2)
        self.m_edicion = tk.Menu(self.mb_edicion, tearoff=0, bd=2, relief=tk.SOLID)
        self.mb_edicion.configure(menu=self.m_edicion)
        self.mb_edicion.pack(side=tk.LEFT, padx=3, pady=3)

        self.mb_ver = tk.Menubutton(self.frame_menu, relief=tk.SOLID, bd=2)
        self.m_ver = tk.Menu(self.mb_ver, tearoff=0, bd=2, relief=tk.SOLID)
        self.mb_ver.configure(menu=self.m_ver)
        self.mb_ver.pack(side=tk.LEFT, padx=3, pady=3)

        self.btn_settings = tk.Button(
            self.frame_menu,
            relief=tk.SOLID,
            bd=2,
            cursor="hand2",
            command=self._abrir_settings
        )
        self.btn_settings.pack(side=tk.RIGHT, padx=4, pady=3)

        # 2. Barra de estado inferior (empaquetada antes para reservar su lugar)
        self.status_bar = tk.Label(
            self,
            relief=tk.SOLID,
            bd=2,
            font=("Courier New", 9, "bold"),
            anchor="w",
            padx=8,
            pady=3
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 3. Contenedor central principal
        self.marco_central = tk.Frame(self, relief=tk.SOLID, bd=4)
        self.marco_central.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.header_panel = tk.Frame(self.marco_central, bg=CONTORNOS, pady=4)
        self.header_panel.pack(fill=tk.X)
        self.lbl_panel_titulo = tk.Label(
            self.header_panel,
            bg=CONTORNOS,
            fg="#FFFFFF",
            font=FUENTE_TITULO
        )
        self.lbl_panel_titulo.pack(side=tk.LEFT, padx=8)

        # Cuerpo dividido en dos bloques
        self.cuerpo = tk.Frame(self.marco_central)
        self.cuerpo.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.bloque_textos = tk.Frame(self.cuerpo, relief=tk.SOLID, bd=2, padx=12, pady=12)
        self.bloque_textos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_usuario = tk.Label(self.bloque_textos, anchor="w")
        self.lbl_usuario.pack(fill=tk.X, pady=4)

        self.lbl_tema = tk.Label(self.bloque_textos, anchor="w")
        self.lbl_tema.pack(fill=tk.X, pady=4)

        self.lbl_idioma = tk.Label(self.bloque_textos, anchor="w")
        self.lbl_idioma.pack(fill=tk.X, pady=4)

        self.lbl_fuente = tk.Label(self.bloque_textos, anchor="w")
        self.lbl_fuente.pack(fill=tk.X, pady=4)

        self.lbl_foto = tk.Label(self.bloque_textos, anchor="w")
        self.lbl_foto.pack(fill=tk.X, pady=4)

        # Bloque de avatar
        self.bloque_avatar = tk.Frame(self.cuerpo, relief=tk.SOLID, bd=2, padx=10, pady=10)
        self.bloque_avatar.pack(side=tk.RIGHT, padx=(10, 0))

        self.lbl_avatar_header = tk.Label(self.bloque_avatar, text="[ FOTO ]", font=FUENTE_NEGRITA)
        self.lbl_avatar_header.pack(pady=(0, 6))
        self.lbl_avatar_img = tk.Label(self.bloque_avatar, relief=tk.SOLID, bd=3)
        self.lbl_avatar_img.pack()

    def aplicar_cambios_visuales(self):
        t = obtener_textos(self.config.get("idioma", "es"))

        color_menu = self.config.get("color_barra_menu", "#000000")
        color_letra = self.config.get("color_letra", "#000000")
        tamano_f = self.config.get("tamano_fuente", 10)
        tema = self.config.get("tema_interfaz", "claro")
        foto_ruta = self.config.get("foto_perfil", "")

        if tema == "oscuro":
            bg_base = "#121212"
            bg_panel = "#1E1E1E"
            fg_general = "#FFFFFF" if color_letra == "#000000" else color_letra
            accent_btn = "#FF3366"
            borde_barra = AMARILLO_CHILLANTE
            menu_btn_bg = "#2A2A2A"
            menu_btn_fg = "#FFFFFF"
        else:
            bg_base = AMARILLO_CHILLANTE
            bg_panel = FONDO
            fg_general = color_letra
            accent_btn = BOTONES
            borde_barra = CONTORNOS
            menu_btn_bg = FONDO
            menu_btn_fg = CONTORNOS

        f_dinamica = ("Courier New", tamano_f, "bold")
        f_dinamica_lg = ("Courier New", tamano_f + 2, "bold")

        self.configure(bg=bg_base)
        self.marco_central.configure(bg=bg_panel)
        self.cuerpo.configure(bg=bg_panel)
        self.bloque_textos.configure(bg=bg_panel)
        self.bloque_avatar.configure(bg=bg_panel)
        self.lbl_avatar_header.configure(bg=bg_panel, fg=fg_general)

        self.frame_menu.configure(bg=color_menu, highlightthickness=2, highlightbackground=borde_barra)
        for mb in (self.mb_archivo, self.mb_edicion, self.mb_ver):
            mb.configure(bg=menu_btn_bg, fg=menu_btn_fg, font=FUENTE_NEGRITA)

        self.mb_archivo.configure(text=t["menu_file"])
        self.mb_edicion.configure(text=t["menu_edit"])
        self.mb_ver.configure(text=t["menu_view"])

        self.btn_settings.configure(
            text=f"⚡ {t['menu_settings']}",
            bg=accent_btn,
            fg=CONTORNOS,
            font=FUENTE_NEGRITA
        )

        for m in (self.m_archivo, self.m_edicion, self.m_ver):
            m.delete(0, tk.END)

        self.m_archivo.add_command(label=t["sim_new"], command=lambda: self._simular(t["sim_new"]))
        self.m_archivo.add_command(label=t["sim_open"], command=lambda: self._simular(t["sim_open"]))
        self.m_archivo.add_separator()
        self.m_archivo.add_command(label=t["sim_exit"], command=self.quit)

        self.m_edicion.add_command(label=t["sim_undo"], command=lambda: self._simular(t["sim_undo"]))
        self.m_edicion.add_command(label=t["sim_cut"], command=lambda: self._simular(t["sim_cut"]))
        self.m_edicion.add_command(label=t["sim_copy"], command=lambda: self._simular(t["sim_copy"]))
        self.m_edicion.add_command(label=t["sim_paste"], command=lambda: self._simular(t["sim_paste"]))

        self.m_ver.add_command(label=t["sim_statusbar"], command=lambda: self._simular(t["sim_statusbar"]))

        self.lbl_panel_titulo.configure(text=t["panel_title"])

        self.lbl_usuario.configure(
            text=t["welcome"].format(usuario=self.config.get("nombre_usuario", "Usuario")),
            bg=bg_panel, fg=fg_general, font=f_dinamica_lg
        )
        self.lbl_tema.configure(
            text=t["theme_lbl"].format(tema=tema.upper()),
            bg=bg_panel, fg=fg_general, font=f_dinamica
        )
        self.lbl_idioma.configure(
            text=t["lang_lbl"].format(idioma=self.config.get("idioma", "es").upper()),
            bg=bg_panel, fg=fg_general, font=f_dinamica
        )
        self.lbl_fuente.configure(
            text=t["font_lbl"].format(tamano=tamano_f),
            bg=bg_panel, fg=fg_general, font=f_dinamica
        )
        self.lbl_foto.configure(
            text=t["photo_lbl"].format(foto=os.path.basename(foto_ruta) or "NONE"),
            bg=bg_panel, fg=fg_general, font=f_dinamica
        )

        self._actualizar_avatar(foto_ruta, bg_panel)

        self.status_bar.configure(
            text=f" PERSISTENCIA | UTF-8 | {tema.upper()} | {self.config.get('idioma', 'es').upper()} ",
            bg=accent_btn,
            fg=CONTORNOS
        )

    def _actualizar_avatar(self, ruta, bg_panel):
        if ruta and os.path.exists(ruta):
            try:
                img = Image.open(ruta)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                self.imagen_avatar = ImageTk.PhotoImage(img)
                self.lbl_avatar_img.configure(image=self.imagen_avatar, text="", width=150, height=150, bg=bg_panel)
                return
            except Exception:
                pass
        self.imagen_avatar = None
        self.lbl_avatar_img.configure(image="", text="[ VACÍO ]", width=14, height=8, font=FUENTE_NEGRITA, bg=bg_panel)

    def _abrir_settings(self):
        VentanaConfig(self, self.config, self._recibir_nueva_config)

    def _recibir_nueva_config(self, nueva_config):
        self.config = nueva_config
        self.aplicar_cambios_visuales()

    def _simular(self, accion):
        t = obtener_textos(self.config.get("idioma", "es"))
        messagebox.showinfo("MENU SIMULADO", t["sim_msg"].format(opc=accion))