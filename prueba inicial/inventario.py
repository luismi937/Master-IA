import json
import os
import uuid

# Configuración del archivo de almacenamiento persistente
DB_FILE = "inventario.json"

# Categorías predefinidas solicitadas por el enunciado
CATEGORIAS_VALIDAS = {"Electrónica", "Ropa", "Alimentos", "Hogar", "Otros"}
CATEGORIA_DEFECTO = "Otros"

def _cargar_datos():
    """Función interna para cargar los productos desde el archivo JSON de forma persistente."""
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {}

def _guardar_datos(datos):
    """Función interna para guardar los productos en el archivo JSON."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False

def add_product(category: str, name: str, price: float) -> str:
    """Añade un nuevo producto al inventario y devuelve su ID único."""
    datos = _cargar_datos()
    
    # Validar categoría o asignar la categoría por defecto si no encaja
    cat_final = category if category in CATEGORIAS_VALIDAS else CATEGORIA_DEFECTO
    
    # Generar un ID único en formato string
    product_id = str(uuid.uuid4())
    
    datos[product_id] = {
        "category": cat_final,
        "name": name,
        "price": float(price)
    }
    
    _guardar_datos(datos)
    return product_id

def delete_product(product_id: str) -> bool:
    """Elimina un producto por su ID. Devuelve True si se eliminó, False si no existía."""
    datos = _cargar_datos()
    if product_id in datos:
        del datos[product_id]
        return _guardar_datos(datos)
    return False

def search_product(name: str) -> list:
    """Busca productos por nombre y devuelve una lista de diccionarios con sus datos e ID."""
    datos = _cargar_datos()
    resultados = []
    
    for p_id, p_info in datos.items():
        if name.lower() in p_info["name"].lower():
            resultados.append({
                "product_id": p_id,
                "category": p_info["category"],
                "name": p_info["name"],
                "price": p_info["price"]
            })
    return resultados

def search_category(category: str) -> list:
    """Obtiene todos los productos pertenecientes a una categoría exacta."""
    datos = _cargar_datos()
    resultados = []
    
    for p_id, p_info in datos.items():
        if p_info["category"] == category:
            resultados.append({
                "product_id": p_id,
                "category": p_info["category"],
                "name": p_info["name"],
                "price": p_info["price"]
            })
    return resultados

def get_categories() -> dict:
    """Devuelve un diccionario con todas las categorías y el número total de productos en cada una."""
    datos = _cargar_datos()
    
    # Inicializar el conteo de todas las categorías predefinidas a 0
    conteo = {cat: 0 for cat in CATEGORIAS_VALIDAS}
    
    for p_info in datos.values():
        cat = p_info["category"]
        if cat in conteo:
            conteo[cat] += 1
            
    return conteo

def update_product(product_id: str, category: str = None, name: str = None, price: float = None) -> bool:
    """Actualiza los valores de un producto existente según los parámetros pasados (salvo el ID)."""
    datos = _cargar_datos()
    
    if product_id not in datos:
        return False
        
    # Actualizar solo los campos que no sean None
    if category is not None:
        cat_final = category if category in CATEGORIAS_VALIDAS else CATEGORIA_DEFECTO
        datos[product_id]["category"] = cat_final
        
    if name is not None:
        datos[product_id]["name"] = name
        
    if price is not None:
        datos[product_id]["price"] = float(price)
        
    return _guardar_datos(datos)


# ==========================================
# BLOQUE DE PRUEBA DIRECTA (MÉTODO RECOMENDADO)
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DIRECTAS DESDE INVENTARIO.PY ---\n")
    
    # 1. Probar añadir productos
    id_tele = add_product("Electrónica", "Televisor Smart", 450.00)
    id_pan = add_product("Alimentos", "Pan Integral", 1.20)
    id_raro = add_product("Zapatos", "Botas de cuero", 89.99) # Va a ir a 'Otros'
    
    print(f"[OK] Producto creado en Electrónica con ID: {id_tele}")
    print(f"[OK] Producto creado en Alimentos con ID: {id_pan}")
    print(f"[OK] Producto creado en Categoría Desconocida (debe ser Otros): {id_raro}\n")
    
    # 2. Probar ver categorías actuales
    print("--- Estado de las categorías actuales ---")
    print(get_categories(), "\n")
    
    # 3. Probar buscar producto por nombre
    print("--- Buscando productos que contengan 'Smart' ---")
    print(search_product("Smart"), "\n")
    
    # 4. Probar actualización de un valor
    print("--- Modificando precio del Pan Integral a 1.45 ---")
    update_product(product_id=id_pan, price=1.45)
    print(f"Comprobación en Alimentos: {search_category('Alimentos')}\n")
    
    # 5. Probar borrado
    print("--- Eliminando el Televisor Smart ---")
    borrado_exitoso = delete_product(id_tele)
    print(f"¿Se borró correctamente?: {borrado_exitoso}")
    print(f"Buscar de nuevo 'Smart' (debe salir vacío): {search_product('Smart')}\n")
    
    print("---PRUEBAS TERMINADAS CON ÉXITO ---")