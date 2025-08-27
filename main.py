#!/usr/bin/env python3
"""
Main Launcher untuk DDoS Defense Learning Project
⚠️ HANYA UNTUK TESTING SISTEM SENDIRI!
"""

import os
import sys
import time
import subprocess
import threading
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import pyfiglet

console = Console()

class DDoSDefenseLauncher:
    def __init__(self):
        self.components = {
            '1': {
                'name': 'DDoS Simulator',
                'file': 'ddos_simulator.py',
                'description': 'Simulasi serangan untuk testing defensif',
                'color': 'red'
            },
            '2': {
                'name': 'DDoS Detector',
                'file': 'ddos_detector.py',
                'description': 'Sistem deteksi serangan DDoS',
                'color': 'blue'
            },
            '3': {
                'name': 'DDoS Mitigation',
                'file': 'mitigation.py',
                'description': 'Tools untuk memblokir serangan',
                'color': 'green'
            },
            '4': {
                'name': 'Monitoring Dashboard',
                'file': 'monitor.py',
                'description': 'Dashboard monitoring traffic real-time',
                'color': 'cyan'
            },
            '5': {
                'name': 'Install Dependencies',
                'file': None,
                'description': 'Install semua package yang diperlukan',
                'color': 'yellow'
            },
            '6': {
                'name': 'System Check',
                'file': None,
                'description': 'Cek sistem dan dependencies',
                'color': 'magenta'
            }
        }
    
    def show_banner(self):
        """Tampilkan banner utama"""
        banner = pyfiglet.figlet_format("DDoS DEFENSE", font="slant")
        console.print(Panel(banner, style="bold blue"))
        console.print("[bold yellow]🛡️  Sistem Pembelajaran Defense DDoS Lengkap![/bold yellow]")
        console.print("[bold green]Pilih komponen yang ingin Anda jalankan...[/bold green]\n")
    
    def show_menu(self):
        """Tampilkan menu utama"""
        menu_table = Table(title="DDoS Defense Learning Project - Main Menu")
        menu_table.add_column("No", style="cyan", justify="center")
        menu_table.add_column("Komponen", style="white")
        menu_table.add_column("Deskripsi", style="green")
        menu_table.add_column("Status", style="yellow")
        
        for key, component in self.components.items():
            # Check if file exists
            if component['file']:
                status = "✅ Ready" if os.path.exists(component['file']) else "❌ Missing"
            else:
                status = "⚙️  System"
            
            menu_table.add_row(
                key,
                f"[{component['color']}]{component['name']}[/{component['color']}]",
                component['description'],
                status
            )
        
        menu_table.add_row("0", "[bold red]Exit[/bold red]", "Keluar dari aplikasi", "🚪")
        
        console.print(menu_table)
    
    def check_dependencies(self):
        """Cek dependencies yang diperlukan"""
        console.print("\n[bold cyan]=== SYSTEM CHECK ===[/bold cyan]")
        
        required_packages = [
            'scapy', 'psutil', 'matplotlib', 'numpy', 
            'flask', 'requests', 'colorama', 'rich', 'pyfiglet'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                console.print(f"[green]✅ {package}[/green]")
            except ImportError:
                console.print(f"[red]❌ {package} - NOT INSTALLED[/red]")
                missing_packages.append(package)
        
        if missing_packages:
            console.print(f"\n[bold yellow]⚠️  {len(missing_packages)} package belum terinstall![/bold yellow]")
            console.print("[yellow]Jalankan opsi 5 untuk install dependencies[/yellow]")
            return False
        else:
            console.print("\n[bold green]🎉 Semua dependencies sudah terinstall![/bold green]")
            return True
    
    def install_dependencies(self):
        """Install dependencies yang diperlukan"""
        console.print("\n[bold cyan]=== INSTALLING DEPENDENCIES ===[/bold cyan]")
        
        try:
            # Check if pip is available
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                 capture_output=True, text=True)
            
            if result.returncode != 0:
                console.print("[red]❌ pip tidak tersedia![/red]")
                return False
            
            # Install from requirements.txt
            if os.path.exists('requirements.txt'):
                console.print("[blue]📦 Installing packages dari requirements.txt...[/blue]")
                
                with Progress() as progress:
                    task = progress.add_task("[cyan]Installing...", total=100)
                    
                    # Simulate progress
                    for i in range(100):
                        progress.update(task, advance=1)
                        time.sleep(0.05)
                
                # Actual installation
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    console.print("[green]✅ Dependencies berhasil diinstall![/green]")
                    return True
                else:
                    console.print(f"[red]❌ Error installing dependencies: {result.stderr}[/red]")
                    return False
            else:
                console.print("[red]❌ requirements.txt tidak ditemukan![/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            return False
    
    def run_component(self, component_key):
        """Jalankan komponen yang dipilih"""
        if component_key not in self.components:
            console.print("[red]❌ Komponen tidak valid![/red]")
            return
        
        component = self.components[component_key]
        
        if component['file'] is None:
            # System component
            if component_key == '5':
                self.install_dependencies()
            elif component_key == '6':
                self.check_dependencies()
            return
        
        # Check if file exists
        if not os.path.exists(component['file']):
            console.print(f"[red]❌ File {component['file']} tidak ditemukan![/red]")
            return
        
        console.print(f"\n[bold {component['color']}]🚀 Menjalankan {component['name']}...[/bold {component['color']}]")
        console.print(f"[blue]File:[/blue] {component['file']}")
        console.print(f"[blue]Deskripsi:[/blue] {component['description']}\n")
        
        try:
            # Run the component
            result = subprocess.run([sys.executable, component['file']], 
                                 capture_output=False, text=False)
            
            if result.returncode == 0:
                console.print(f"\n[green]✅ {component['name']} selesai dengan sukses![/green]")
            else:
                console.print(f"\n[yellow]⚠️  {component['name']} selesai dengan exit code: {result.returncode}[/yellow]")
                
        except KeyboardInterrupt:
            console.print(f"\n[yellow]⏹️  {component['name']} dihentikan oleh user[/yellow]")
        except Exception as e:
            console.print(f"\n[red]❌ Error menjalankan {component['name']}: {e}[/red]")
    
    def show_usage_guide(self):
        """Tampilkan panduan penggunaan"""
        console.print("\n[bold cyan]=== PANDUAN PENGGUNAAN ===[/bold cyan]")
        
        guide = """
[bold yellow]🎯 Tujuan Pembelajaran:[/bold yellow]
• Memahami cara kerja serangan DDoS
• Belajar mendeteksi serangan DDoS  
• Implementasi sistem pertahanan DDoS
• Testing keamanan sistem sendiri

[bold yellow]📋 Urutan Penggunaan yang Disarankan:[/bold yellow]
1. Install Dependencies (opsi 5)
2. System Check (opsi 6) 
3. Monitoring Dashboard (opsi 4) - untuk monitoring baseline
4. DDoS Simulator (opsi 1) - untuk testing defensif
5. DDoS Detector (opsi 2) - untuk deteksi serangan
6. DDoS Mitigation (opsi 3) - untuk pertahanan

[bold yellow]⚠️  PERINGATAN PENTING:[/bold yellow]
• HANYA gunakan pada sistem yang Anda miliki
• JANGAN PERNAH gunakan untuk testing sistem orang lain
• Tujuan utama: pembelajaran cybersecurity defensif
• Semua aktivitas di-log untuk audit trail

[bold yellow]🔧 Troubleshooting:[/bold yellow]
• Pastikan semua dependencies terinstall
• Jalankan sebagai Administrator/root jika diperlukan
• Cek firewall dan antivirus settings
• Monitor log files untuk error details
        """
        
        console.print(Panel(guide, title="📖 Panduan Lengkap", style="bold blue"))
    
    def main_loop(self):
        """Main loop aplikasi"""
        while True:
            try:
                self.show_banner()
                self.show_menu()
                
                choice = input("\n[bold cyan]Pilihan Anda (0-6): [/bold cyan]")
                
                if choice == '0':
                    console.print("\n[bold yellow]👋 Terima kasih telah menggunakan DDoS Defense Learning Project![/bold yellow]")
                    console.print("[bold green]Semoga pembelajaran Anda bermanfaat untuk cybersecurity![/bold green]")
                    break
                
                elif choice in self.components:
                    self.run_component(choice)
                    
                    # Ask if user wants to continue
                    if choice in ['1', '2', '3', '4']:  # Only for main components
                        continue_choice = input("\n[bold yellow]Kembali ke menu utama? (y/N): [/bold yellow]")
                        if continue_choice.lower() != 'y':
                            break
                
                elif choice == 'help':
                    self.show_usage_guide()
                    input("\n[bold cyan]Tekan Enter untuk kembali ke menu...[/bold cyan]")
                
                else:
                    console.print("[red]❌ Pilihan tidak valid![/red]")
                    console.print("[yellow]Ketik 'help' untuk panduan penggunaan[/yellow]")
                
                # Clear screen for better UX
                os.system('cls' if os.name == 'nt' else 'clear')
                
            except KeyboardInterrupt:
                console.print("\n\n[bold yellow]👋 Aplikasi dihentikan oleh user[/bold yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]❌ Error dalam main loop: {e}[/red]")
                input("\n[bold cyan]Tekan Enter untuk melanjutkan...[/bold cyan]")

def main():
    """Main function"""
    launcher = DDoSDefenseLauncher()
    
    try:
        launcher.main_loop()
    except Exception as e:
        console.print(f"\n[red]❌ Fatal error: {e}[/red]")
        console.print("[yellow]Silakan cek error log dan coba lagi[/yellow]")

if __name__ == "__main__":
    main()
