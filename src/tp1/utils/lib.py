from scapy.all import get_if_list

def hello_world() -> str:
    """
    Hello world function
    """
    return "hello world"


def choose_interface() -> str:
    """
    Return network interface and input user choice
    """
    interface = get_if_list()

    print("Interfaces dispo:")
    for index, iface in enumerate(interface, start=1):
        print(f"{index}. {iface}")
    
    while True:
        choice = input("Choisissez le numéro de l'interface: ")
        if not choice.isdigit():
            print("Entrée invalide")
            continue

        choice_index = int(choice) - 1

        if 0 <= choice_index < len(interface):
            return interface[choice_index]
        
        print("Numéro invalide")
