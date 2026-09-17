from src.repositories.deportes_repository import DeportesRepository

def obtener_todos_los_deportes():
    return DeportesRepository.obtener_todos()