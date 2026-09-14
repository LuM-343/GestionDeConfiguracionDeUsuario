import json
import shutil
import os
import re

CONFIG_ARCHIVO = "configuracion.json"
BACKUP_ARCHIVO = "configuracion.bak"
TEMP_ARCHIVO = "configuracion.tmp"

configuracionPorDefecto = {
        "nombre_usuario": "Usuario",
        "tema_interfaz": "claro",
        "idioma": "es",
        "tamano_fuente": 12,
        "color_barra_menu": "#FFFFFF",
        "color_letra": "#000000",
        "foto_perfil": ""
    }

#Verifica si una cadena cumple con el formato #RRGGBB.
def colorHexvalido(color): 
    return bool(re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", str(color).strip()))

#Revisa si cada campo de la configuración es válido, si no lo modifica por el valor por defecto.
def validarRepararConfiguracion(datos): 

    if not isinstance(datos, dict):
        return configuracionPorDefecto.copy()

    valida = configuracionPorDefecto.copy()

    # 1. Nombre de usuario
    nombre = datos.get("nombre_usuario")
    if isinstance(nombre, str) and nombre.strip():
        valida["nombre_usuario"] = nombre
    else:
        print("[Validación] nombre_usuario inválido. Usando por defecto.")

    # 2. Tema de interfaz (solo 'claro' u 'oscuro')
    tema = str(datos.get("tema_interfaz", "")).strip().lower()
    if tema in ["claro", "oscuro"]:
        valida["tema_interfaz"] = tema
    else:
        print(f"[Validación] tema_interfaz '{tema}' inválido. Degradando a valor por defecto ('claro').")
        valida["tema_interfaz"] = "claro"

    # 3. Idioma
    idioma = str(datos.get("idioma", "")).strip().lower()
    if any(k in idioma for k in ["es", "en"]):
        valida["idioma"] = datos["idioma"]
    else:
        print(f"[Validación] idioma '{idioma}' desconocido. Usando por defecto ('es').")
        valida["idioma"] = "es"

    # 4. Tamaño de fuente (entero entre 8 y 30)
    try:
        tam = int(datos.get("tamano_fuente"))
        if 8 <= tam <= 30:
            valida["tamano_fuente"] = tam
        else:
            print(f"[Validación] tamano_fuente fuera de rango ({tam}). Usando por defecto.")
            valida["tamano_fuente"] = 10
    except (ValueError, TypeError):
        print("[Validación] tamano_fuente no es numérico. Usando por defecto.")
        valida["tamano_fuente"] = 10

    # 5. Color de la barra de menú
    col_menu = datos.get("color_barra_menu")
    if colorHexvalido(col_menu):
        valida["color_barra_menu"] = col_menu
    else:
        print(f"[Validación] color_barra_menu '{col_menu}' inválido. Usando por defecto.")
        valida["color_barra_menu"] = configuracionPorDefecto["color_barra_menu"]

    # 6. Color de letra
    col_letra = datos.get("color_letra")
    if colorHexvalido(col_letra):
        valida["color_letra"] = col_letra
    else:
        print(f"[Validación] color_letra '{col_letra}' inválido. Usando por defecto.")
        valida["color_letra"] = configuracionPorDefecto["color_letra"]

    # 7. Foto de perfil
    foto = datos.get("foto_perfil")
    if isinstance(foto, str):
        valida["foto_perfil"] = foto
    else:
        valida["foto_perfil"] = ""

    return valida

def leerConfiguracion():
    try:
        with open(CONFIG_ARCHIVO, "r", encoding="utf-8") as archivo:
            configuracion = json.load(archivo)
            return validarRepararConfiguracion(configuracion)
    except FileNotFoundError:
            print("[Aviso] Archivo ausente: cargando valores por defecto.")
            return configuracionPorDefecto.copy()
    except json.JSONDecodeError as e:
        print(f"[Error] Archivo corrupto ({e}): cargando valores por defecto.")
        return configuracionPorDefecto.copy()
    except PermissionError:
        print("[Error] Permiso denegado al leer el archivo de configuración.")
        return configuracionPorDefecto.copy()
    except Exception as e:
        print(f"[Error inesperado] {e}: cargando valores por defecto.")
        return configuracionPorDefecto.copy()
    
    return configuracion

#Crear respaldo con .bak
def crearRespaldo():
    if os.path.exists(CONFIG_ARCHIVO):
        try:
            shutil.copy(CONFIG_ARCHIVO, BACKUP_ARCHIVO)
            print("Respaldo creado exitosamente.")
            return True
        except Exception as e:
            print(f"Ocurrió un error al crear el respaldo: {e}")
            return False
    return True

def escribirConfiguracion(configuracion=configuracionPorDefecto):
    try:
        crearRespaldo()
        with open(TEMP_ARCHIVO, "w", encoding="utf-8") as temp:
            json.dump(configuracion, temp, indent=4, ensure_ascii=False)
        os.replace(TEMP_ARCHIVO, CONFIG_ARCHIVO)
        return True
    except PermissionError:
        print("[Error] Permisos insuficientes para escribir la configuración.")
        if os.path.exists(TEMP_ARCHIVO):
            os.remove(TEMP_ARCHIVO)
        return False
    except Exception as e:
        print(f"[Error al guardar] {e}")
        if os.path.exists(TEMP_ARCHIVO):
            os.remove(TEMP_ARCHIVO)
        return False