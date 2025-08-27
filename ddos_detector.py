#!/usr/bin/env python3
"""
DDoS Detector untuk Pembelajaran Defense
⚠️ HANYA UNTUK TESTING SISTEM SENDIRI!
"""

import time
import threading
import socket
import psutil
import json
import logging
from collections import defaultdict, deque
from scapy.all import *
import config
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
import pyfiglet

console = Console()

class DDoSDetector:
    def __init__(self):
        self.thresholds = config.DDoS_THRESHOLDS
        self.running = False
        self.detected_attacks = []
        self.connection_stats = defaultdict(int)
        self.bandwidth_stats = deque(maxlen=60)  # 60 detik history
        self.suspicious_ips = set()
        self.blocked_ips = set()
        
        # Setup logging
        logging.basicConfig(
            filename=config.MONITORING_CONFIG['log_file'],
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Network monitoring
        self.network_stats = {
            'packets_received': 0,
            'bytes_received': 0,
            'connections_active': 0,
            'connections_total': 0,
            'start_time': time.time()
        }
    
    def show_banner(self):
        """Menampilkan banner aplikasi"""
        banner = pyfiglet.figlet_format("DDoS DETECTOR", font="slant")
        console.print(Panel(banner, style="bold blue"))
        console.print("[bold yellow]🔍 Sistem Deteksi DDoS Aktif![/bold yellow]")
        console.print("[bold green]Monitoring network traffic untuk mendeteksi serangan...[/bold green]\n")
    
    def monitor_network_interface(self):
        """Monitor network interface untuk traffic analysis"""
        try:
            # Dapatkan network interface stats
            net_io = psutil.net_io_counters()
            
            # Update bandwidth stats
            current_time = time.time()
            bandwidth_data = {
                'timestamp': current_time,
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
            
            self.bandwidth_stats.append(bandwidth_data)
            
            # Hitung bandwidth per detik
            if len(self.bandwidth_stats) > 1:
                time_diff = self.bandwidth_stats[-1]['timestamp'] - self.bandwidth_stats[0]['timestamp']
                if time_diff > 0:
                    bytes_per_sec = (self.bandwidth_stats[-1]['bytes_recv'] - self.bandwidth_stats[0]['bytes_recv']) / time_diff
                    
                    # Deteksi bandwidth anomaly
                    if bytes_per_sec > self.thresholds['bandwidth_threshold']:
                        self.detect_bandwidth_attack(bytes_per_sec)
            
        except Exception as e:
            console.print(f"[red]Error monitoring network: {e}[/red]")
    
    def detect_bandwidth_attack(self, bytes_per_sec):
        """Deteksi serangan berdasarkan bandwidth"""
        attack_info = {
            'type': 'Bandwidth Flood',
            'timestamp': time.time(),
            'severity': 'HIGH' if bytes_per_sec > self.thresholds['bandwidth_threshold'] * 2 else 'MEDIUM',
            'details': f'Bandwidth: {bytes_per_sec:.2f} bytes/sec (Threshold: {self.thresholds["bandwidth_threshold"]:,})'
        }
        
        self.detected_attacks.append(attack_info)
        self.log_attack(attack_info)
        console.print(f"[bold red]🚨 BANDWIDTH ATTACK DETECTED![/bold red] {attack_info['details']}")
    
    def packet_callback(self, packet):
        """Callback untuk setiap paket yang diterima"""
        try:
            if IP in packet:
                source_ip = packet[IP].src
                self.network_stats['packets_received'] += 1
                
                # Update connection stats per IP
                self.connection_stats[source_ip] += 1
                
                # Deteksi connection flood
                if self.connection_stats[source_ip] > self.thresholds['max_connections_per_ip']:
                    self.detect_connection_flood(source_ip, self.connection_stats[source_ip])
                
                # Deteksi SYN flood
                if TCP in packet and packet[TCP].flags & 0x02:  # SYN flag
                    self.detect_syn_flood(source_ip)
                
                # Deteksi UDP flood
                if UDP in packet:
                    self.detect_udp_flood(source_ip)
                
        except Exception as e:
            console.print(f"[red]Error processing packet: {e}[/red]")
    
    def detect_connection_flood(self, source_ip, connection_count):
        """Deteksi connection flood dari IP tertentu"""
        if source_ip not in self.suspicious_ips:
            attack_info = {
                'type': 'Connection Flood',
                'timestamp': time.time(),
                'source_ip': source_ip,
                'severity': 'HIGH' if connection_count > self.thresholds['max_connections_per_ip'] * 2 else 'MEDIUM',
                'details': f'IP {source_ip} membuat {connection_count} koneksi (Threshold: {self.thresholds["max_connections_per_ip"]})'
            }
            
            self.detected_attacks.append(attack_info)
            self.suspicious_ips.add(source_ip)
            self.log_attack(attack_info)
            console.print(f"[bold red]🚨 CONNECTION FLOOD DETECTED![/bold red] {attack_info['details']}")
    
    def detect_syn_flood(self, source_ip):
        """Deteksi SYN flood attack"""
        # Implementasi deteksi SYN flood yang lebih advanced
        pass
    
    def detect_udp_flood(self, source_ip):
        """Deteksi UDP flood attack"""
        # Implementasi deteksi UDP flood yang lebih advanced
        pass
    
    def monitor_connections(self):
        """Monitor active connections"""
        try:
            connections = psutil.net_connections()
            tcp_connections = [conn for conn in connections if conn.status == 'ESTABLISHED']
            
            self.network_stats['connections_active'] = len(tcp_connections)
            self.network_stats['connections_total'] += len(tcp_connections)
            
            # Deteksi connection spike
            if len(tcp_connections) > self.thresholds['requests_per_second']:
                self.detect_connection_spike(len(tcp_connections))
                
        except Exception as e:
            console.print(f"[red]Error monitoring connections: {e}[/red]")
    
    def detect_connection_spike(self, connection_count):
        """Deteksi spike dalam jumlah koneksi"""
        attack_info = {
            'type': 'Connection Spike',
            'timestamp': time.time(),
            'severity': 'HIGH' if connection_count > self.thresholds['requests_per_second'] * 2 else 'MEDIUM',
            'details': f'Active connections: {connection_count} (Threshold: {self.thresholds["requests_per_second"]})'
        }
        
        self.detected_attacks.append(attack_info)
        self.log_attack(attack_info)
        console.print(f"[bold red]🚨 CONNECTION SPIKE DETECTED![/bold red] {attack_info['details']}")
    
    def log_attack(self, attack_info):
        """Log serangan yang terdeteksi"""
        logging.warning(f"DDoS Attack Detected: {json.dumps(attack_info)}")
    
    def generate_dashboard(self):
        """Generate dashboard untuk monitoring"""
        # Network stats table
        stats_table = Table(title="Network Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        elapsed_time = time.time() - self.network_stats['start_time']
        packets_per_sec = self.network_stats['packets_received'] / elapsed_time if elapsed_time > 0 else 0
        
        stats_table.add_row("Packets Received", f"{self.network_stats['packets_received']:,}")
        stats_table.add_row("Active Connections", f"{self.network_stats['connections_active']}")
        stats_table.add_row("Packets/Second", f"{packets_per_sec:.2f}")
        stats_table.add_row("Suspicious IPs", f"{len(self.suspicious_ips)}")
        stats_table.add_row("Blocked IPs", f"{len(self.blocked_ips)}")
        stats_table.add_row("Attacks Detected", f"{len(self.detected_attacks)}")
        
        # Recent attacks table
        attacks_table = Table(title="Recent Attacks (Last 5)")
        attacks_table.add_column("Time", style="cyan")
        attacks_table.add_column("Type", style="red")
        attacks_table.add_column("Severity", style="yellow")
        attacks_table.add_column("Details", style="white")
        
        for attack in self.detected_attacks[-5:]:
            time_str = time.strftime("%H:%M:%S", time.localtime(attack['timestamp']))
            attacks_table.add_row(
                time_str,
                attack['type'],
                attack['severity'],
                attack.get('details', 'N/A')[:50] + "..." if len(attack.get('details', '')) > 50 else attack.get('details', 'N/A')
            )
        
        return Panel(f"{stats_table}\n\n{attacks_table}")
    
    def start_monitoring(self):
        """Mulai monitoring network"""
        self.show_banner()
        
        # Start packet sniffing
        sniff_thread = threading.Thread(target=self.sniff_packets)
        sniff_thread.daemon = True
        sniff_thread.start()
        
        # Start monitoring loop
        with Live(self.generate_dashboard(), refresh_per_second=1) as live:
            try:
                while True:
                    # Update network stats
                    self.monitor_network_interface()
                    self.monitor_connections()
                    
                    # Update dashboard
                    live.update(self.generate_dashboard())
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Monitoring dihentikan oleh user[/bold yellow]")
    
    def sniff_packets(self):
        """Sniff network packets"""
        try:
            console.print("[green]🔍 Memulai packet sniffing...[/green]")
            sniff(prn=self.packet_callback, store=0)
        except Exception as e:
            console.print(f"[red]Error dalam packet sniffing: {e}[/red]")

def main():
    """Main function"""
    detector = DDoSDetector()
    
    console.print("\n[bold cyan]DDoS Detector untuk Pembelajaran Defense[/bold cyan]")
    console.print("Sistem akan mulai monitoring network traffic...")
    console.print("Tekan Ctrl+C untuk berhenti\n")
    
    try:
        detector.start_monitoring()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Monitoring dihentikan[/bold yellow]")

if __name__ == "__main__":
    main()
