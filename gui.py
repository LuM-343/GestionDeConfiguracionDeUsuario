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
        "menu_settings": "CONFIGURACIÓN*",
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
        "btn_default": "[POR DEFECTO]"
    },
    "en": {
        "menu_file": "[FILE]",
        "menu_edit": "[EDIT]",
        "menu_view": "[VIEW]",
        "menu_settings": "SETTINGS*",
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
        "btn_default": "[RESET / DEFAULTS]"
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

        self.title("CONFIGURACIÓN DE INTERFAZ - PROYECTO 1")
        self.geometry("500x560")
        self.resizable(False, False)
        self.configure(bg=AMARILLO_CHILLANTE)
        self.transient(parent)
        self.grab_set()

        # Variables vinculadas a campos requeridos
        self.var_usuario = tk.StringVar(value=self.config_actual.get("nombre_usuario", "Usuario"))
        self.var_tema = tk.StringVar(value=self.config_actual.get("tema_interfaz", "claro"))
        self.var_idioma = tk.StringVar(value=self.config_actual.get("idioma", "es"))
        self.var_fuente = tk.IntVar(value=self.config_actual.get("tamano_fuente", 10))
        self.var_color_menu = tk.StringVar(value=self.config_actual.get("color_barra_menu", "#000000"))
        self.var_color_letra = tk.StringVar(value=self.config_actual.get("color_letra", "#000000"))
        self.var_foto = tk.StringVar(value=self.config_actual.get("foto_perfil", ""))

        self._construir_ui()

    def _construir_ui(self):
        # Cabecera 
        lbl_banner = tk.Label(
            self,
            text="[ PANEL DE CONTROL :: EDICIÓN ]",
            bg=CONTORNOS,
            fg="#FFFFFF",
            font=FUENTE_TITULO,
            pady=8
        )
        lbl_banner.pack(fill=tk.X)

        contenedor = tk.Frame(self, bg=FONDO, highlightthickness=3, highlightbackground=CONTORNOS)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        filas = [
            ("1. USUARIO [UTF-8]:", self._widget_usuario),
            ("2. TEMA UI:", self._widget_tema),
            ("3. IDIOMA:", self._widget_idioma),
            ("4. TAMAÑO FUENTE:", self._widget_fuente),
            ("5. COLOR BARRA:", self._widget_color_menu),
            ("6. COLOR TEXTO:", self._widget_color_letra),
            ("7. FOTO PERFIL:", self._widget_foto)
        ]

        for idx, (etiqueta, fn_creador) in enumerate(filas):
            lbl = tk.Label(
                contenedor,
                text=etiqueta,
                bg=FONDO,
                fg=CONTORNOS,
                font=FUENTE_CUERPO,
                anchor="w"
            )
            lbl.grid(row=idx, column=0, sticky="w", padx=12, pady=6)
            fn_creador(contenedor, idx)

        contenedor.columnconfigure(1, weight=1)

        # Botones inferiores 
        f_bot = tk.Frame(self, bg=AMARILLO_CHILLANTE)
        f_bot.pack(side=tk.BOTTOM, fill=tk.X, padx=14, pady=10)

        # Botón para restablecer valores por defecto
        t = obtener_textos(self.var_idioma.get())
        self.btn_default = tk.Button(
            f_bot,
            text=t["btn_default"],
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
            text="CANCELAR [X]",
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
            text="GUARDAR [✔]",
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
        # Límite estricto de 30 caracteres
        return len(nuevo_texto) <= 30

    def _widget_usuario(self, parent, r):
        vcmd = (self.register(self._validar_tamano_usuario), "%P")
        entry = tk.Entry(
            parent,
            textvariable=self.var_usuario,
            font=FUENTE_CUERPO,
            relief=tk.SOLID,
            bd=2,
            bg="#FFFFFF",
            validate="key",
            validatecommand=vcmd
        )
        entry.grid(row=r, column=1, sticky="ew", padx=12, pady=6)

    def _widget_tema(self, parent, r):
        f = tk.Frame(parent, bg=FONDO)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        for t in ["claro", "oscuro"]:
            tk.Radiobutton(
                f,
                text=t.upper(),
                value=t,
                variable=self.var_tema,
                bg=FONDO,
                fg=CONTORNOS,
                font=FUENTE_CUERPO,
                activebackground=FONDO
            ).pack(side=tk.LEFT, padx=4)

    def _widget_idioma(self, parent, r):
        f = tk.Frame(parent, bg=FONDO)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        for i in ["es", "en"]:
            tk.Radiobutton(
                f,
                text=i.upper(),
                value=i,
                variable=self.var_idioma,
                bg=FONDO,
                fg=CONTORNOS,
                font=FUENTE_CUERPO,
                activebackground=FONDO,
                selectcolor="#FFFFFF",
                command=self._actualizar_etiqueta_boton_default
            ).pack(side=tk.LEFT, padx=4)

    def _actualizar_etiqueta_boton_default(self):
        t = obtener_textos(self.var_idioma.get())
        self.btn_default.configure(text=t["btn_default"])

    def _widget_fuente(self, parent, r):
        spin = tk.Spinbox(
            parent,
            from_=8,
            to=22,
            textvariable=self.var_fuente,
            font=FUENTE_CUERPO,
            relief=tk.SOLID,
            bd=2,
            width=6
        )
        spin.grid(row=r, column=1, sticky="w", padx=12, pady=6)

    def _widget_color_menu(self, parent, r):
        f = tk.Frame(parent, bg=FONDO)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        self.prev_menu = tk.Label(f, width=4, relief=tk.SOLID, bd=2, bg=self.var_color_menu.get())
        self.prev_menu.pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            f, text="ELEGIR COLOR", font=FUENTE_CUERPO, relief=tk.SOLID, bd=2,
            bg=FONDO, cursor="hand2", command=self._seleccionar_color_menu
        ).pack(side=tk.LEFT)

    def _widget_color_letra(self, parent, r):
        f = tk.Frame(parent, bg=FONDO)
        f.grid(row=r, column=1, sticky="w", padx=12, pady=6)
        self.prev_letra = tk.Label(f, width=4, relief=tk.SOLID, bd=2, bg=self.var_color_letra.get())
        self.prev_letra.pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            f, text="ELEGIR COLOR", font=FUENTE_CUERPO, relief=tk.SOLID, bd=2,
            bg=FONDO, cursor="hand2", command=self._seleccionar_color_letra
        ).pack(side=tk.LEFT)

    def _widget_foto(self, parent, r):
        f = tk.Frame(parent, bg=FONDO)
        f.grid(row=r, column=1, sticky="ew", padx=12, pady=6)
        self.lbl_foto = tk.Label(
            f,
            text=os.path.basename(self.var_foto.get()) or "NO ASIGNADA",
            font=("Courier New", 9),
            bg="#EFEFEF",
            relief=tk.SOLID,
            bd=1,
            width=14,
            anchor="w"
        )
        self.lbl_foto.pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(
            f, text="EXPLORAR...", font=FUENTE_CUERPO, relief=tk.SOLID, bd=2,
            bg=FONDO, cursor="hand2", command=self._seleccionar_foto
        ).pack(side=tk.LEFT)

    def _seleccionar_color_menu(self):
        c = colorchooser.askcolor(self.var_color_menu.get(), title="SELECCIONAR COLOR DE BARRA")
        if c[1]:
            self.var_color_menu.set(c[1])
            self.prev_menu.configure(bg=c[1])

    def _seleccionar_color_letra(self):
        c = colorchooser.askcolor(self.var_color_letra.get(), title="SELECCIONAR COLOR DE LETRA")
        if c[1]:
            self.var_color_letra.set(c[1])
            self.prev_letra.configure(bg=c[1])

    def _seleccionar_foto(self):
        r = filedialog.askopenfilename(
            title="SELECCIONAR FOTO DE PERFIL",
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
            "tamano_fuente": 10,
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
        self.lbl_foto.configure(text=os.path.basename(self.var_foto.get()) or "NO ASIGNADA")
        self._actualizar_etiqueta_boton_default()

    def _guardar(self):
        try:
            fuente_val = int(self.var_fuente.get())
        except ValueError:
            messagebox.showerror("ERROR DE TIPO", "EL TAMAÑO DE FUENTE DEBE SER UN ENTERO.")
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

        # Guardado con validaciones en configManager
        if cm.escribirConfiguracion(nueva_cfg):
            t = obtener_textos(nueva_cfg["idioma"])
            messagebox.showinfo("ESTADO DE PERSISTENCIA", t["saved_ok"])
            self.callback_guardado(nueva_cfg)
            self.destroy()
        else:
            t = obtener_textos(self.var_idioma.get())
            messagebox.showerror("ERROR DE ARCHIVO", t["saved_err"])


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

        # Botón Settings destacado 
        self.btn_settings = tk.Button(
            self.frame_menu,
            relief=tk.SOLID,
            bd=2,
            cursor="hand2",
            command=self._abrir_settings
        )
        self.btn_settings.pack(side=tk.RIGHT, padx=4, pady=3)

        # 2. Contenedor central principal
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
        self.lbl_avatar_img = tk.Label(self.bloque_avatar, relief=tk.SOLID, bd=3, width=110, height=110)
        self.lbl_avatar_img.pack()

        # 3. Barra de estado inferior maciza
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

    def aplicar_cambios_visuales(self):
        t = obtener_textos(self.config.get("idioma", "es"))

        color_menu = self.config.get("color_barra_menu", "#000000")
        color_letra = self.config.get("color_letra", "#000000")
        tamano_f = self.config.get("tamano_fuente", 10)
        tema = self.config.get("tema_interfaz", "claro")
        foto_ruta = self.config.get("foto_perfil", "")

        # Configuración visual de paleta según tema claro u oscuro
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

        # Fondos
        self.configure(bg=bg_base)
        self.marco_central.configure(bg=bg_panel)
        self.cuerpo.configure(bg=bg_panel)
        self.bloque_textos.configure(bg=bg_panel)
        self.bloque_avatar.configure(bg=bg_panel)
        self.lbl_avatar_header.configure(bg=bg_panel, fg=fg_general)

        # Barra de menús
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

        # Submenús simulados
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

        # Título
        self.lbl_panel_titulo.configure(text=t["panel_title"])

        # Datos
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

        # Imagen
        self._actualizar_avatar(foto_ruta, bg_panel)

        # Barra de estado
        self.status_bar.configure(
            text=f" PERSISTENCIA | UTF-8 | {tema.upper()} | {self.config.get('idioma', 'es').upper()} ",
            bg=accent_btn,
            fg=CONTORNOS
        )

    def _actualizar_avatar(self, ruta, bg_panel):
        if ruta and os.path.exists(ruta):
            try:
                img = Image.open(ruta)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.imagen_avatar = ImageTk.PhotoImage(img)
                self.lbl_avatar_img.configure(image=self.imagen_avatar, text="", bg=bg_panel)
                return
            except Exception:
                pass
        self.imagen_avatar = None
        self.lbl_avatar_img.configure(image="", text="[ VACÍO ]", font=FUENTE_NEGRITA, bg=bg_panel)

    def _abrir_settings(self):
        VentanaConfig(self, self.config, self._recibir_nueva_config)

    def _recibir_nueva_config(self, nueva_config):
        self.config = nueva_config
        self.aplicar_cambios_visuales()

    def _simular(self, accion):
        t = obtener_textos(self.config.get("idioma", "es"))
        messagebox.showinfo("MENU SIMULADO", t["sim_msg"].format(opc=accion))


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()