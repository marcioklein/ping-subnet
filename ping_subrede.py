import ipaddress
import platform
import subprocess

def ping(ip):
    """
    Faz ping em um IP. Retorna True se responder.
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


def testar_subrede(subnet):
    """
    Testa IPs de uma sub-rede até encontrar algum que responda ao ping.
    """
    rede = ipaddress.ip_network(subnet, strict=False)
    sistema = platform.system().lower()

    usa_emoji = sistema != "windows"

    for ip in rede.hosts():
        print(f"Testando {ip} ...", end=" ")
        if ping(ip):
            if usa_emoji:
                print("✅ Respondeu!")
            else:
                print("OK - Respondeu!")
            return ip
        else:
            if usa_emoji:
                print("❌ Sem resposta")
            else:
                print("Falhou - Sem resposta")

    print("Nenhum host respondeu.")
    return None


if __name__ == "__main__":
    subnet = input("Digite a sub-rede (ex: 192.168.1.0/24): ").strip()
    ip_respondendo = testar_subrede(subnet)

    if ip_respondendo:
        print(f"\nPrimeiro host que respondeu: {ip_respondendo}")
    else:
        print("\nNenhum host da sub-rede respondeu ao ping.")

    # Mantém a janela aberta no Windows
    input("\nPressione Enter para sair...")
