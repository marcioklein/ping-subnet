import ipaddress
import platform
import subprocess

def ping(ip):
    """
    Hace ping a una IP. Devuelve True si responde.
    """
    sistema = platform.system().lower()

    if sistema == "windows":
        comando = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        comando = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return resultado.returncode == 0
    except Exception:
        return False


def probar_subred(subred):
    """
    Prueba las IPs de una subred hasta encontrar alguna que responda al ping.
    """
    red = ipaddress.ip_network(subred, strict=False)
    sistema = platform.system().lower()

    usa_emoji = sistema != "windows"

    for ip in red.hosts():
        print(f"Probando {ip} ...", end=" ")
        if ping(ip):
            if usa_emoji:
                print("✅ ¡Respondió!")
            else:
                print("OK - ¡Respondió!")
            return ip
        else:
            if usa_emoji:
                print("❌ Sin respuesta")
            else:
                print("Falló - Sin respuesta")

    print("Ningún host respondió.")
    return None


if __name__ == "__main__":
    while True:
        subred = input("\nIngrese la subred (ej: 192.168.1.0/24) o 'salir' para terminar: ").strip()
        if subred.lower() in ["salir", "exit", "quit"]:
            print("Cerrando el programa...")
            break

        try:
            ip_respondio = probar_subred(subred)
            if ip_respondio:
                print(f"\nPrimer host que respondió: {ip_respondio}")
            else:
                print("\nNingún host de la subred respondió al ping.")
        except ValueError:
            print("❌ Subred inválida, intente de nuevo.")
