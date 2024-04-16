from pymongo import MongoClient
from pymongo.errors import ConfigurationError
import os


mongo_pass = os.environ['mongo_password']
try:
    # Conexión a MongoDB
    uri = f"mongodb+srv://maugallo1:{mongo_pass}@cluster0.bgisyyf.mongodb.net/"
    cliente = MongoClient(uri)
    db = cliente["files"]
    _memory_menu = db["_memory_menu"]
except ConfigurationError as e:
    print("Error de configuración al conectar a MongoDB:", e)
    # Manejar el error de configuración de manera apropiada, como registrar o notificar al usuario.
    # Aquí podrías agregar código adicional para manejar la situación de error de conexión.

# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    nueva_receta = {
        'nombre': nombre,
        'ingredientes': ingredientes,
        'pasos': pasos
    }

    _memory_menu.insert_one(nueva_receta)
    print("Receta agregada con éxito.")

# Función para actualizar una receta existente
def actualizar_receta():
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")
    nueva_receta = {}

    receta = _memory_menu.find_one({'_id': id_receta})

    if receta:
        print(f"Receta actual: {receta}")
        nueva_receta['nombre'] = input("Nuevo nombre de la receta (deje en blanco para no cambiar): ") or receta['nombre']
        nueva_receta['ingredientes'] = input("Nuevos ingredientes (deje en blanco para no cambiar): ") or receta['ingredientes']
        nueva_receta['pasos'] = input("Nuevos pasos de la receta (deje en blanco para no cambiar): ") or receta['pasos']

        _memory_menu.update_one({'_id': id_receta}, {'$set': nueva_receta})
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def eliminar_receta():
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")

    resultado = _memory_menu.delete_one({'_id': id_receta})

    if resultado.deleted_count:
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para ver un listado de recetas
def ver_listado_recetas():
    cantidad_recetas = _memory_menu.count_documents({})  # Contar el número de documentos en la colección

    if cantidad_recetas:
        recetas = _memory_menu.find()
        print("Listado de recetas:")
        for receta in recetas:
            print(f"ID: {receta['_id']}, Nombre: {receta['nombre']}, Ingredientes: {receta['ingredientes']}, Pasos: {receta['pasos']}")
    else:
        print("No hay recetas en el libro.")



# Función principal
def main():
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Ver listado de recetas")
        print("f) Salir")

        opcion = input("Ingrese la opción deseada: ").lower()

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'c':
            actualizar_receta()
        elif opcion == 'd':
            eliminar_receta()
        elif opcion == 'e':
            ver_listado_recetas()
        elif opcion == 'f':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

if __name__ == "__main__":
    main()
