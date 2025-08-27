#!/usr/bin/env python3
"""
DDoS Mitigation System untuk Pembelajaran Defense
⚠️ HANYA UNTUK TESTING SISTEM SENDIRI!
"""

import time
import threading
import subprocess
import platform
import json
import logging
from collections import defaultdict
import config
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import pyfiglet

console = Console()

class DDoSMitigation:
    def __init__(self):
        self.config = config.MITIGATION_CONFIG
        self.blocked_ips = set()
        self.whitelist_ips = set(self.config['whitelist_ips'])
        self.rate_limits = defaultdict(int)
        self.block_history = []
        
        # Setup logging
        logging.basicConfig(
            filename='mitigation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Platform detection
        self.platform = platform.system().lower()
        console.print(f"[blue]Platform terdeteksi: {self.platform}[/blue]")
    
    def show_banner(self):
        """Menampilkan banner aplikasi"""
        banner = pyfiglet.figlet_format("DDoS MITIGATION", font="slant")
        console.print(Panel(banner, style="bold green"))
        console.print("[bold yellow]🛡️  Sistem Pertahanan DDoS Aktif![/bold yellow]")
        console.print("[bold green]Menggunakan berbagai teknik untuk memblokir serangan...[/bold green]\n")
    
    def block_ip(self, ip_address, reason="DDoS Attack", duration=None):
        """Block IP address menggunakan firewall"""
        if ip_address in self.whitelist_ips:
            console.print(f"[yellow]⚠️  IP {ip_address} ada di whitelist, tidak bisa diblokir[/yellow]")
            return False
        
        if ip_address in self.blocked_ips:
            console.print(f"[blue]IP {ip_address} sudah diblokir sebelumnya[/blue]")
            return True
        
        try:
            if self.platform == "windows":
                success = self.block_ip_windows(ip_address)
            elif self.platform == "linux":
                success = self.block_ip_linux(ip_address)
            elif self.platform == "darwin":  # macOS
                success = self.block_ip_macos(ip_address)
            else:
                console.print(f"[red]Platform {self.platform} tidak didukung[/red]")
                return False
            
            if success:
                self.blocked_ips.add(ip_address)
                block_info = {
                    'ip': ip_address,
                    'timestamp': time.time(),
                    'reason': reason,
                    'duration': duration or self.config['block_duration'],
                    'platform': self.platform
                }
                self.block_history.append(block_info)
                
                console.print(f"[bold green]✅ IP {ip_address} berhasil diblokir![/bold green]")
                logging.info(f"IP {ip_address} blocked: {reason}")
                
                # Auto-unblock setelah durasi tertentu
                if duration:
                    threading.Timer(duration, self.unblock_ip, args=[ip_address]).start()
                
                return True
            else:
                console.print(f"[red]❌ Gagal memblokir IP {ip_address}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error blocking IP {ip_address}: {e}[/red]")
            logging.error(f"Error blocking IP {ip_address}: {e}")
            return False
    
    def block_ip_windows(self, ip_address):
        """Block IP di Windows menggunakan Windows Firewall"""
        try:
            # Buat rule untuk memblokir IP
            rule_name = f"Block_DDoS_{ip_address.replace('.', '_')}"
            
            # Command untuk Windows Firewall
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name="{rule_name}"',
                'dir=in',
                'action=block',
                f'remoteip={ip_address}',
                'enable=yes'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"[green]Windows Firewall rule '{rule_name}' berhasil dibuat[/green]")
                return True
            else:
                console.print(f"[red]Error Windows Firewall: {result.stderr}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error dalam Windows Firewall: {e}[/red]")
            return False
    
    def block_ip_linux(self, ip_address):
        """Block IP di Linux menggunakan iptables"""
        try:
            # Command untuk iptables
            cmd = ['iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"[green]iptables rule berhasil dibuat untuk IP {ip_address}[/green]")
                return True
            else:
                console.print(f"[red]Error iptables: {result.stderr}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error dalam iptables: {e}[/red]")
            return False
    
    def block_ip_macos(self, ip_address):
        """Block IP di macOS menggunakan pfctl"""
        try:
            # Buat temporary pf rule
            pf_rule = f"block drop from {ip_address} to any\n"
            
            # Tulis ke temporary file
            with open('/tmp/ddos_block.pf', 'w') as f:
                f.write(pf_rule)
            
            # Load rule ke pf
            cmd = ['pfctl', '-f', '/tmp/ddos_block.pf']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"[green]pf rule berhasil dibuat untuk IP {ip_address}[/green]")
                return True
            else:
                console.print(f"[red]Error pfctl: {result.stderr}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error dalam pfctl: {e}[/red]")
            return False
    
    def unblock_ip(self, ip_address):
        """Unblock IP address"""
        try:
            if ip_address not in self.blocked_ips:
                return False
            
            if self.platform == "windows":
                success = self.unblock_ip_windows(ip_address)
            elif self.platform == "linux":
                success = self.unblock_ip_linux(ip_address)
            elif self.platform == "darwin":
                success = self.unblock_ip_macos(ip_address)
            else:
                return False
            
            if success:
                self.blocked_ips.remove(ip_address)
                console.print(f"[green]✅ IP {ip_address} berhasil di-unblock[/green]")
                logging.info(f"IP {ip_address} unblocked")
                return True
            
        except Exception as e:
            console.print(f"[red]Error unblocking IP {ip_address}: {e}[/red]")
            return False
    
    def unblock_ip_windows(self, ip_address):
        """Unblock IP di Windows"""
        try:
            rule_name = f"Block_DDoS_{ip_address.replace('.', '_')}"
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name="{rule_name}"'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"[red]Error unblocking Windows: {e}[/red]")
            return False
    
    def unblock_ip_linux(self, ip_address):
        """Unblock IP di Linux"""
        try:
            cmd = ['iptables', '-D', 'INPUT', '-s', ip_address, '-j', 'DROP']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"[red]Error unblocking Linux: {e}[/red]")
            return False
    
    def unblock_ip_macos(self, ip_address):
        """Unblock IP di macOS"""
        try:
            # Flush semua rules
            cmd = ['pfctl', '-F', 'all', '-f', '/etc/pf.conf']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"[red]Error unblocking macOS: {e}[/red]")
            return False
    
    def rate_limit_ip(self, ip_address, max_requests=10, window_seconds=60):
        """Implementasi rate limiting untuk IP tertentu"""
        current_time = time.time()
        
        # Cleanup old entries
        self.rate_limits = {ip: count for ip, count in self.rate_limits.items() 
                           if current_time - count['timestamp'] < window_seconds}
        
        if ip_address not in self.rate_limits:
            self.rate_limits[ip_address] = {
                'count': 1,
                'timestamp': current_time
            }
        else:
            self.rate_limits[ip_address]['count'] += 1
        
        # Check if rate limit exceeded
        if self.rate_limits[ip_address]['count'] > max_requests:
            console.print(f"[yellow]⚠️  Rate limit exceeded untuk IP {ip_address}[/yellow]")
            return self.block_ip(ip_address, "Rate Limit Exceeded", 300)  # Block for 5 minutes
        
        return False
    
    def show_status(self):
        """Tampilkan status mitigation system"""
        console.print("\n[bold cyan]=== STATUS MITIGATION SYSTEM ===[/bold cyan]")
        
        # Blocked IPs table
        blocked_table = Table(title="Blocked IP Addresses")
        blocked_table.add_column("IP Address", style="red")
        blocked_table.add_column("Block Time", style="cyan")
        blocked_table.add_column("Reason", style="yellow")
        blocked_table.add_column("Duration", style="green")
        
        for block_info in self.block_history[-10:]:  # Show last 10
            time_str = time.strftime("%H:%M:%S", time.localtime(block_info['timestamp']))
            duration_str = f"{block_info['duration']}s" if block_info['duration'] else "Permanent"
            
            blocked_table.add_row(
                block_info['ip'],
                time_str,
                block_info['reason'],
                duration_str
            )
        
        # Rate limiting table
        rate_table = Table(title="Rate Limiting Status")
        rate_table.add_column("IP Address", style="cyan")
        rate_table.add_column("Requests", style="yellow")
        rate_table.add_column("Last Request", style="green")
        
        current_time = time.time()
        for ip, data in self.rate_limits.items():
            time_ago = current_time - data['timestamp']
            time_str = f"{time_ago:.1f}s ago"
            
            rate_table.add_row(
                ip,
                str(data['count']),
                time_str
            )
        
        console.print(blocked_table)
        console.print(rate_table)
        
        # Summary
        console.print(f"\n[bold blue]Total IPs Blocked:[/bold blue] {len(self.blocked_ips)}")
        console.print(f"[bold blue]Total IPs Rate Limited:[/bold blue] {len(self.rate_limits)}")
        console.print(f"[bold blue]Whitelist IPs:[/bold blue] {len(self.whitelist_ips)}")
    
    def auto_mitigation(self, attack_data):
        """Automatic mitigation berdasarkan data serangan"""
        if not self.config['enable_auto_block']:
            return
        
        try:
            if 'source_ip' in attack_data:
                source_ip = attack_data['source_ip']
                
                # Auto-block berdasarkan severity
                if attack_data.get('severity') == 'HIGH':
                    duration = self.config['block_duration'] * 2  # Block longer for high severity
                    self.block_ip(source_ip, f"Auto-block: {attack_data['type']}", duration)
                elif attack_data.get('severity') == 'MEDIUM':
                    # Rate limit untuk medium severity
                    self.rate_limit_ip(source_ip, max_requests=5, window_seconds=30)
            
            # Log auto-mitigation
            logging.info(f"Auto-mitigation applied: {json.dumps(attack_data)}")
            
        except Exception as e:
            console.print(f"[red]Error dalam auto-mitigation: {e}[/red]")
    
    def interactive_mode(self):
        """Mode interaktif untuk manual mitigation"""
        self.show_banner()
        
        while True:
            console.print("\n[bold cyan]=== DDoS MITIGATION MENU ===[/bold cyan]")
            console.print("1. Block IP Address")
            console.print("2. Unblock IP Address")
            console.print("3. Show Status")
            console.print("4. Add to Whitelist")
            console.print("5. Remove from Whitelist")
            console.print("6. Exit")
            
            choice = input("\nPilihan Anda (1-6): ")
            
            if choice == "1":
                ip = input("Masukkan IP address untuk diblokir: ")
                reason = input("Alasan blocking (optional): ") or "Manual Block"
                self.block_ip(ip, reason)
                
            elif choice == "2":
                ip = input("Masukkan IP address untuk di-unblock: ")
                self.unblock_ip(ip)
                
            elif choice == "3":
                self.show_status()
                
            elif choice == "4":
                ip = input("Masukkan IP address untuk whitelist: ")
                self.whitelist_ips.add(ip)
                console.print(f"[green]IP {ip} ditambahkan ke whitelist[/green]")
                
            elif choice == "5":
                ip = input("Masukkan IP address untuk hapus dari whitelist: ")
                if ip in self.whitelist_ips:
                    self.whitelist_ips.remove(ip)
                    console.print(f"[green]IP {ip} dihapus dari whitelist[/green]")
                else:
                    console.print(f"[yellow]IP {ip} tidak ada di whitelist[/yellow]")
                    
            elif choice == "6":
                console.print("[yellow]Keluar dari mitigation system[/yellow]")
                break
                
            else:
                console.print("[red]Pilihan tidak valid![/red]")

def main():
    """Main function"""
    mitigation = DDoSMitigation()
    
    console.print("\n[bold cyan]DDoS Mitigation System untuk Pembelajaran Defense[/bold cyan]")
    console.print("1. Interactive Mode")
    console.print("2. Test Block IP")
    console.print("3. Show Status")
    
    choice = input("\nPilihan Anda (1-3): ")
    
    if choice == "1":
        mitigation.interactive_mode()
    elif choice == "2":
        ip = input("Masukkan IP untuk test block: ")
        mitigation.block_ip(ip, "Test Block", 60)
        time.sleep(2)
        mitigation.unblock_ip(ip)
    elif choice == "3":
        mitigation.show_status()
    else:
        console.print("[red]Pilihan tidak valid![/red]")

if __name__ == "__main__":
    main()
