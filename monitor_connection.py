# -*- coding: utf-8 -*-
import sys
import subprocess  # Importa il modulo subprocess per eseguire nuovi processi
import platform  # Importa il modulo platform per accedere a informazioni sulla piattaforma, come il nome del sistema operativo
import concurrent.futures  # Importa il modulo concurrent.futures per il supporto del multithreading

def is_valid_ip(ip):  # Definisce una funzione per verificare se un indirizzo IP è valido
    parts = ip.split('.')  # Divide l'indirizzo IP in parti utilizzando il punto come separatore
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)  # Controlla se l'indirizzo IP è valido

def ping_host(ip):  # Definisce una funzione per eseguire un ping a un host
    if not is_valid_ip(ip):  # Controlla se l'indirizzo IP è valido
        print(f"Indirizzo IP non valido: {ip}")
        return False  # Ritorna False se l'indirizzo IP non è valido
    param = '-n' if platform.system().lower()=='windows' else '-c'  # Imposta il parametro per il comando ping in base al sistema operativo
    command = ['ping', param, '1', ip]  # Crea il comando ping

    try:  # Tenta di eseguire il comando ping
        #output = subprocess.run(' '.join(command), capture_output=True, timeout=5, shell=True)   Esegue il comando ping e cattura l'output
        output = subprocess.run(command, capture_output=True, timeout=1)  # Esegue il comando ping e cattura l'output
        return output.returncode == 0  # Ritorna True se il ping è riuscito, False altrimenti
    except subprocess.TimeoutExpired:
        print(f"Timeout scaduto durante il ping a {ip}")  # Stampa un messaggio di errore se il timeout scade
        return False  # Ritorna False se il timeout scade
    except Exception as e:
        print(f"Errore durante il ping a {ip}: {str(e)}")  # Stampa un messaggio di errore se si verifica un'eccezione
        return False  # Ritorna False se si verifica un'eccezione

hosts = input("Inserisci gli indirizzi IP degli host da monitorare, separati da virgole: ").split(',')  # Chiede all'utente di inserire gli indirizzi IP degli host da monitorare

with concurrent.futures.ThreadPoolExecutor() as executor:  # Crea un pool di thread per eseguire il ping a più host contemporaneamente
    future_to_ip = {executor.submit(ping_host, host.strip()): host.strip() for host in hosts}  # Sottomette i task al pool di thread e memorizza i Future in un dizionario
    for future in concurrent.futures.as_completed(future_to_ip):  # Aspetta che ogni task completi
        ip = future_to_ip[future]  # Ottiene l'indirizzo IP associato al Future
        try: # Gestisce le eccezioni che possono verificarsi durante l'esecuzione del ping
            if future.result(): # Controlla se l'host è online o offline
                print(f"{ip} online")
            else:
                print(f"{ip} offline")
        except Exception as e:
            print(f"Errore durante il controllo dell'host {ip}: {str(e)}") # Stampa un messaggio di errore se si verifica un'eccezione durante il ping