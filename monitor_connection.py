# -*- coding: utf-8 -*-
import subprocess
import platform 
import concurrent.futures

def is_valid_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

def ping_host(ip):
    if not is_valid_ip(ip):
        print(f"Indirizzo IP non valido: {ip}")
        return False
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', ip]

    try:
        output = subprocess.run(command, capture_output=True, timeout=5)
        return output.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout scaduto durante il ping a {ip}")
        return False
    except Exception as e:
        print(f"Errore durante il ping a {ip}: {str(e)}")
        return False

hosts = input("Inserisci gli indirizzi IP degli host da monitorare, separati da virgole: ").split(',')

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_ip = {executor.submit(ping_host, host.strip()): host.strip() for host in hosts}
    for future in concurrent.futures.as_completed(future_to_ip):
        ip = future_to_ip[future] 
        try: 
            if future.result():
                print(f"{ip} online")
            else:
                print(f"{ip} offline")
        except Exception as e:
            print(f"Errore durante il controllo dell'host {ip}: {str(e)}")