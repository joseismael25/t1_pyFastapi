"""Cliente de consola para consumir la API de aprendices.

Inicia la API en otra terminal y ejecuta desde la raíz del proyecto:
    python -m src.views.view
"""
import json
import httpx

API_URL = "http://127.0.0.1:8000"


def mostrar_respuesta(response: httpx.Response) -> None:
    print(f"\nEstado HTTP: {response.status_code}")
    if response.content:
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except ValueError:
            print(response.text)
    elif response.is_success:
        print("Operación completada correctamente.")


def pedir_texto(etiqueta: str, opcional: bool = False):
    sufijo = " (Enter para omitir)" if opcional else ""
    valor = input(f"{etiqueta}{sufijo}: ").strip()
    return valor if valor else (None if opcional else "")


def pedir_id() -> str:
    return pedir_texto("ID del aprendiz")


def crear_aprendiz(client: httpx.Client):
    datos = {
        "document": pedir_texto("Documento"),
        "firstname": pedir_texto("Nombre"),
        "lastname": pedir_texto("Apellido"),
        "email": pedir_texto("Correo electrónico"),
        "age": pedir_texto("Edad"),
        "program": pedir_texto("Programa"),
        "record_number": pedir_texto("Número de ficha"),
    }
    if not all(datos.values()):
        print("Todos los campos son obligatorios.")
        return
    try:
        datos["age"] = int(datos["age"])
        datos["record_number"] = int(datos["record_number"])
    except (TypeError, ValueError):
        print("La edad y el número de ficha deben ser números enteros.")
        return
    mostrar_respuesta(client.post("/Trainees/", json=datos))


def listar_aprendices(client: httpx.Client):
    mostrar_respuesta(client.get("/Trainees/"))


def consultar_aprendiz(client: httpx.Client):
    trainee_id = pedir_id()
    if not trainee_id:
        print("Debes escribir el ID del aprendiz.")
        return
    mostrar_respuesta(client.get(f"/Trainees/{trainee_id}"))


def actualizar_aprendiz(client: httpx.Client):
    trainee_id = pedir_id()
    if not trainee_id:
        print("Debes escribir el ID del aprendiz.")
        return
    datos = {}
    campos = [
        ("firstname", "Nombre"), ("lastname", "Apellido"),
        ("email", "Correo electrónico"), ("age", "Edad"),
        ("program", "Programa"), ("record_number", "Número de ficha"),
    ]
    for campo, etiqueta in campos:
        valor = pedir_texto(etiqueta, opcional=True)
        if valor is not None:
            if campo in ("age", "record_number"):
                try:
                    valor = int(valor)
                except ValueError:
                    print(f"{etiqueta} debe ser un número entero.")
                    return
            datos[campo] = valor
    if not datos:
        print("No ingresaste ningún campo para actualizar.")
        return
    mostrar_respuesta(client.put(f"/Trainees/{trainee_id}", json=datos))


def eliminar_aprendiz(client: httpx.Client):
    trainee_id = pedir_id()
    if not trainee_id:
        print("Debes escribir el ID del aprendiz.")
        return
    confirmar = input(f"¿Seguro que deseas eliminar el registro {trainee_id}? (s/N): ").strip().lower()
    if confirmar != "s":
        print("Operación cancelada.")
        return
    mostrar_respuesta(client.delete(f"/Trainees/{trainee_id}"))


def main():
    print(f"\nCliente de consola para la API: {API_URL}")
    try:
        with httpx.Client(base_url=API_URL, timeout=10.0) as client:
            try:
                response = client.get("/")
                response.raise_for_status()
            except httpx.RequestError:
                print("No se pudo conectar con la API. Iníciala primero en otra terminal:")
                print("python -m uvicorn src.main:app --reload")
                return
            while True:
                print("\n=== GESTIÓN DE APRENDICES ===")
                print("1. Registrar aprendiz")
                print("2. Listar aprendices")
                print("3. Consultar aprendiz por ID")
                print("4. Actualizar aprendiz")
                print("5. Eliminar aprendiz")
                print("0. Salir")
                opcion = input("Selecciona una opción: ").strip()
                try:
                    if opcion == "1":
                        crear_aprendiz(client)
                    elif opcion == "2":
                        listar_aprendices(client)
                    elif opcion == "3":
                        consultar_aprendiz(client)
                    elif opcion == "4":
                        actualizar_aprendiz(client)
                    elif opcion == "5":
                        eliminar_aprendiz(client)
                    elif opcion == "0":
                        print("Hasta luego.")
                        break
                    else:
                        print("Opción no válida. Intenta de nuevo.")
                except httpx.RequestError as exc:
                    print(f"Error de conexión con la API: {exc}")
                except KeyboardInterrupt:
                    print("\nOperación cancelada.")
                    break
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")


if __name__ == "__main__":
    main()
