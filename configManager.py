import json
import shutil
import os

CONFIG_ARCHIVO = "configuracion.json"
BACKUP_ARCHIVO = "configuracion.bak"
TEMP_ARCHIVO = "configuracion.tmp"

configuracionPorDefecto = {
        "nombre_usuario": "Usuario",
        "tema_interfaz": "claro",
        "idioma": "español",
        "tamano_fuente": 12,
        "color_barra_menu": "#FFFFFF",
        "color_letra": "#000000",
        "foto_perfil": "FotoPerfilPorDefecto.png"
    }

def leerConfiguracion():
    try:
        with open(CONFIG_ARCHIVO, "r", encoding="utf-8") as archivo:
            configuracion = json.load(archivo)
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