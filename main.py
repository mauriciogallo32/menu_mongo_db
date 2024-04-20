from pymongo import MongoClient
from bson import ObjectId

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['recetas_db']
recetas_collection = db['recetas']

# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    nueva_receta = {
        'nombre': nombre,
        'ingredientes': ingredientes.split(','),
        'pasos': pasos
    }
    recetas_collection.insert_one(nueva_receta)
    print("Receta agregada con éxito.")

# Función para actualizar una receta existente
def actualizar_receta():
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")
    receta = recetas_collection.find_one({'_id': ObjectId(id_receta)})

    if receta:
        print(f"Receta actual: {receta}")
        nombre = input("Nuevo nombre de la receta (deje en blanco para no cambiar): ") or receta['nombre']
        ingredientes = input("Nuevos ingredientes (deje en blanco para no cambiar): ") or ','.join(receta['ingredientes'])
        pasos = input("Nuevos pasos de la receta (deje en blanco para no cambiar): ") or receta['pasos']

        recetas_collection.update_one({'_id': ObjectId(id_receta)}, {'$set': {'nombre': nombre, 'ingredientes': ingredientes.split(','), 'pasos': pasos}})
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def eliminar_receta():
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")
    receta = recetas_collection.find_one({'_id': ObjectId(id_receta)})

    if receta:
        recetas_collection.delete_one({'_id': ObjectId(id_receta)})
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para ver un listado de recetas
def ver_listado_recetas():
    recetas = recetas_collection.find()

    count = recetas_collection.count_documents({})  # Contar documentos en la colección

    if count > 0:
        for receta in recetas:
            print(f"ID: {receta['_id']}, Nombre: {receta['nombre']}, Ingredientes: {', '.join(receta['ingredientes'])}, Pasos: {receta['pasos']}")
    else:
        print("No hay recetas en el libro.")

# Función principal
def menu_principal():
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
    menu_principal()