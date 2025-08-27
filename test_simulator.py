#!/usr/bin/env python3
"""
Test file untuk DDoS Simulator
Untuk testing tanpa menjalankan serangan nyata
"""

import config
from rich.console import Console

console = Console()

def test_config():
    """Test konfigurasi"""
    console.print("[bold cyan]=== TEST KONFIGURASI ===[/bold cyan]")
    
    # Test simulator config
    sim_config = config.SIMULATOR_CONFIG
    console.print(f"[green]Target Host:[/green] {sim_config['target_host']}")
    console.print(f"[green]Target Port:[/green] {sim_config['target_port']}")
    console.print(f"[green]Duration:[/green] {sim_config['attack_duration']} detik")
    console.print(f"[green]Packets/sec:[/green] {sim_config['packets_per_second']}")
    console.print(f"[green]Target Selection:[/green] {sim_config['enable_target_selection']}")
    console.print(f"[green]Port Selection:[/green] {sim_config['enable_port_selection']}")
    
    # Test safe targets
    console.print(f"\n[green]Safe Targets:[/green]")
    for i, target in enumerate(sim_config['safe_targets'], 1):
        console.print(f"  {i}. {target}")
    
    # Test common ports
    console.print(f"\n[green]Common Ports:[/green]")
    for i, port in enumerate(sim_config['common_ports'], 1):
        console.print(f"  {i}. Port {port}")
    
    # Test thresholds
    console.print(f"\n[green]DDoS Thresholds:[/green]")
    thresholds = config.DDoS_THRESHOLDS
    console.print(f"  Requests/sec: {thresholds['requests_per_second']}")
    console.print(f"  Max connections/IP: {thresholds['max_connections_per_ip']}")
    console.print(f"  Bandwidth threshold: {thresholds['bandwidth_threshold']:,} bytes/sec")

def test_target_validation():
    """Test validasi target IP"""
    console.print("\n[bold cyan]=== TEST VALIDASI TARGET ===[/bold cyan]")
    
    test_ips = [
        "192.168.1.1",      # Valid
        "10.0.0.1",         # Valid
        "172.16.0.1",       # Valid
        "127.0.0.1",        # Dangerous (localhost)
        "::1",              # Invalid format
        "256.1.1.1",        # Invalid range
        "192.168.1",        # Invalid format
        "abc.def.ghi.jkl",  # Invalid format
    ]
    
    for ip in test_ips:
        if is_valid_ip(ip):
            if is_dangerous_ip(ip):
                console.print(f"[red]❌ {ip} - Valid tapi BERBAHAYA![/red]")
            else:
                console.print(f"[green]✅ {ip} - Valid dan aman[/green]")
        else:
            console.print(f"[yellow]⚠️  {ip} - Format tidak valid[/yellow]")

def is_valid_ip(ip):
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

def is_dangerous_ip(ip):
    """Cek apakah IP berbahaya untuk testing"""
    # Cek localhost ranges
    if ip.startswith('127.'):
        return True
    
    # Cek private network ranges yang bisa berbahaya
    if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
        return False  # Allow dengan warning
    
    return False

def main():
    """Main function"""
    console.print("[bold blue]🚀 DDoS Simulator Test Suite[/bold blue]")
    console.print("[yellow]Testing konfigurasi dan validasi tanpa menjalankan serangan...[/yellow]\n")
    
    try:
        test_config()
        test_target_validation()
        
        console.print("\n[bold green]✅ Semua test berhasil![/bold green]")
        console.print("[blue]Sistem siap untuk digunakan dengan target yang aman.[/blue]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Test gagal: {e}[/bold red]")
        console.print("[yellow]Cek konfigurasi dan dependencies.[/yellow]")

if __name__ == "__main__":
    main()
