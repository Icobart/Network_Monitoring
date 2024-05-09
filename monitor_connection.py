# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:19:23 2024

@author: enric
"""
"""
from ping3 import ping, verbose_ping

def ping_host(ip):
    try:
        delay = ping(ip)
        if delay is None:
            return f"{ip} is offline"
        else:
            return f"{ip} is online, ping in {delay} seconds"
    except OSError as e:
        return f"Network error: {str(e)}"
    except TimeoutError:
        return f"Request to {ip} timed out."
    except Exception as e:
        return f"Cannot ping {ip}: {str(e)}"

hosts = input("Enter the IP addresses of the hosts to monitor, separated by commas: ").split(',')

for host in hosts:
    print(ping_host(host.strip()))
"""
"""
import concurrent.futures
from ping3 import ping
def ping_host(ip):
    try:
        delay = ping(ip)
        if delay is None:
            return f"{ip} is offline"
        else:
            return f"{ip} is online, ping in {delay} seconds"
    except OSError as e:
        return f"Network error: {str(e)}"
    except TimeoutError:
        return f"Request to {ip} timed out."
    except Exception as e:
        return f"Cannot ping {ip}: {str(e)}"

hosts = input("Enter the IP addresses of the hosts to monitor, separated by commas: ").split(',')

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(ping_host, host.strip()): host for host in hosts}
    for future in concurrent.futures.as_completed(futures):
        host = futures[future]
        try:
            print(future.result())
        except Exception as e:
            print(f"Cannot ping {host}: {str(e)}")
"""
"""
import os
import platform
def ping_host(ip):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', ip]

    return os.system(' '.join(command)) == 0

hosts = input("Enter the IP addresses of the hosts to monitor, separated by commas: ").split(',')

for host in hosts:
    if ping_host(host.strip()):
        print(f"{host.strip()} is online")
    else:
        print(f"{host.strip()} is offline")
"""
"""
import os, sys
import subprocess
import platform

def ping_host(ip):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', ip]

    try:
        output = subprocess.check_output(' '.join(command), stderr=subprocess.STDOUT, shell=True)
        if 'unreachable' in output.decode('utf-8').lower():
            return False
        else:
            return True
    except Exception as e:
        print(f"Error pinging {ip}: {str(e)}")
        return False

hosts = input("Enter the IP addresses of the hosts to monitor, separated by commas: ").split(',')

for host in hosts:
    if ping_host(host.strip()):
        print(f"{host.strip()} is online")
    else:
        print(f"{host.strip()} is offline")
"""
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
        output = subprocess.run(' '.join(command), stderr=subprocess.STDOUT, capture_output=True, timeout=5, shell=True)  # Esegue il comando ping e cattura l'output
        if 'unreachable' in output.stdout.decode('utf-8').lower():  # Controlla se l'host è irraggiungibile
            return False 
        else:
            return True
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
                print(f"{ip} is online")
            else:
                print(f"{ip} is offline")
        except Exception as e:
            print(f"Error checking host {ip}: {str(e)}") # Stampa un messaggio di errore se si verifica un'eccezione durante il ping