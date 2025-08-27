#!/usr/bin/env python3
"""
DDoS Monitoring Dashboard untuk Pembelajaran Defense
⚠️ HANYA UNTUK TESTING SISTEM SENDIRI!
"""

import time
import threading
import json
import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np
from collections import deque
import config
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
import pyfiglet

console = Console()

class DDoSMonitor:
    def __init__(self):
        self.running = False
        self.monitoring_data = {
            'timestamps': deque(maxlen=300),  # 5 menit history
            'packets_per_sec': deque(maxlen=300),
            'connections': deque(maxlen=300),
            'bandwidth': deque(maxlen=300),
            'cpu_usage': deque(maxlen=300),
            'memory_usage': deque(maxlen=300)
        }
        
        # Attack detection
        self.attack_alerts = []
        self.suspicious_ips = set()
        
        # Setup matplotlib untuk real-time plotting
        plt.style.use('dark_background')
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('DDoS Defense Monitoring Dashboard', fontsize=16, color='white')
        
        # Initialize plots
        self.setup_plots()
    
    def setup_plots(self):
        """Setup matplotlib plots"""
        # Network Traffic
        self.axes[0, 0].set_title('Network Traffic (Packets/sec)', color='white')
        self.axes[0, 0].set_ylabel('Packets/sec', color='white')
        self.axes[0, 0].grid(True, alpha=0.3)
        
        # Active Connections
        self.axes[0, 1].set_title('Active Connections', color='white')
        self.axes[0, 1].set_ylabel('Connections', color='white')
        self.axes[0, 1].grid(True, alpha=0.3)
        
        # Bandwidth Usage
        self.axes[1, 0].set_title('Bandwidth Usage (MB/s)', color='white')
        self.axes[1, 0].set_ylabel('MB/s', color='white')
        self.axes[1, 0].grid(True, alpha=0.3)
        
        # System Resources
        self.axes[1, 1].set_title('System Resources (%)', color='white')
        self.axes[1, 1].set_ylabel('Usage %', color='white')
        self.axes[1, 1].grid(True, alpha=0.3)
        
        # Set colors
        for ax in self.axes.flat:
            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
    
    def collect_system_metrics(self):
        """Collect system metrics"""
        try:
            current_time = time.time()
            
            # Network stats
            net_io = psutil.net_io_counters()
            connections = psutil.net_connections()
            active_connections = len([conn for conn in connections if conn.status == 'ESTABLISHED'])
            
            # Calculate packets per second (simplified)
            if len(self.monitoring_data['timestamps']) > 0:
                time_diff = current_time - self.monitoring_data['timestamps'][-1]
                if time_diff > 0:
                    packets_per_sec = (net_io.packets_recv - self.monitoring_data['packets_per_sec'][-1]) / time_diff
                else:
                    packets_per_sec = 0
            else:
                packets_per_sec = 0
            
            # Bandwidth calculation
            if len(self.monitoring_data['timestamps']) > 0:
                time_diff = current_time - self.monitoring_data['timestamps'][-1]
                if time_diff > 0:
                    bandwidth = (net_io.bytes_recv - self.monitoring_data['bandwidth'][-1]) / time_diff / (1024 * 1024)  # MB/s
                else:
                    bandwidth = 0
            else:
                bandwidth = 0
            
            # System resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Store data
            self.monitoring_data['timestamps'].append(current_time)
            self.monitoring_data['packets_per_sec'].append(packets_per_sec)
            self.monitoring_data['connections'].append(active_connections)
            self.monitoring_data['bandwidth'].append(bandwidth)
            self.monitoring_data['cpu_usage'].append(cpu_percent)
            self.monitoring_data['memory_usage'].append(memory_percent)
            
            # Attack detection
            self.detect_anomalies(packets_per_sec, active_connections, bandwidth, cpu_percent)
            
        except Exception as e:
            console.print(f"[red]Error collecting metrics: {e}[/red]")
    
    def detect_anomalies(self, packets_per_sec, connections, bandwidth, cpu):
        """Deteksi anomaly yang mungkin serangan DDoS"""
        thresholds = config.DDoS_THRESHOLDS
        
        alerts = []
        
        # Packet rate anomaly
        if packets_per_sec > thresholds['requests_per_second']:
            alerts.append({
                'type': 'High Packet Rate',
                'severity': 'HIGH' if packets_per_sec > thresholds['requests_per_second'] * 2 else 'MEDIUM',
                'value': f'{packets_per_sec:.2f} packets/sec',
                'threshold': f'{thresholds["requests_per_second"]} packets/sec'
            })
        
        # Connection spike
        if connections > thresholds['max_connections_per_ip'] * 10:
            alerts.append({
                'type': 'Connection Spike',
                'severity': 'HIGH' if connections > thresholds['max_connections_per_ip'] * 20 else 'MEDIUM',
                'value': f'{connections} connections',
                'threshold': f'{thresholds["max_connections_per_ip"] * 10} connections'
            })
        
        # Bandwidth anomaly
        if bandwidth > thresholds['bandwidth_threshold'] / (1024 * 1024):  # Convert to MB/s
            alerts.append({
                'type': 'Bandwidth Flood',
                'severity': 'HIGH' if bandwidth > thresholds['bandwidth_threshold'] / (1024 * 1024) * 2 else 'MEDIUM',
                'value': f'{bandwidth:.2f} MB/s',
                'threshold': f'{thresholds["bandwidth_threshold"] / (1024 * 1024):.2f} MB/s'
            })
        
        # CPU spike (indirect DDoS indicator)
        if cpu > 80:
            alerts.append({
                'type': 'High CPU Usage',
                'severity': 'MEDIUM',
                'value': f'{cpu:.1f}%',
                'threshold': '80%'
            })
        
        # Add alerts
        for alert in alerts:
            alert['timestamp'] = time.time()
            self.attack_alerts.append(alert)
            
            # Keep only last 50 alerts
            if len(self.attack_alerts) > 50:
                self.attack_alerts = self.attack_alerts[-50:]
            
            # Log alert
            console.print(f"[bold red]🚨 {alert['type']} DETECTED![/bold red] {alert['value']} (Threshold: {alert['threshold']})")
    
    def update_plots(self, frame):
        """Update matplotlib plots"""
        try:
            # Clear all plots
            for ax in self.axes.flat:
                ax.clear()
                ax.set_facecolor('#1e1e1e')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.spines['left'].set_color('white')
            
            if len(self.monitoring_data['timestamps']) > 1:
                # Convert timestamps to relative time
                relative_times = [t - self.monitoring_data['timestamps'][0] for t in self.monitoring_data['timestamps']]
                
                # Network Traffic
                self.axes[0, 0].set_title('Network Traffic (Packets/sec)', color='white')
                self.axes[0, 0].plot(relative_times, list(self.monitoring_data['packets_per_sec']), 'g-', linewidth=2)
                self.axes[0, 0].set_ylabel('Packets/sec', color='white')
                self.axes[0, 0].grid(True, alpha=0.3)
                
                # Active Connections
                self.axes[0, 1].set_title('Active Connections', color='white')
                self.axes[0, 1].plot(relative_times, list(self.monitoring_data['connections']), 'b-', linewidth=2)
                self.axes[0, 1].set_ylabel('Connections', color='white')
                self.axes[0, 1].grid(True, alpha=0.3)
                
                # Bandwidth Usage
                self.axes[1, 0].set_title('Bandwidth Usage (MB/s)', color='white')
                self.axes[1, 0].plot(relative_times, list(self.monitoring_data['bandwidth']), 'y-', linewidth=2)
                self.axes[1, 0].set_ylabel('MB/s', color='white')
                self.axes[1, 0].grid(True, alpha=0.3)
                
                # System Resources
                self.axes[1, 1].set_title('System Resources (%)', color='white')
                self.axes[1, 1].plot(relative_times, list(self.monitoring_data['cpu_usage']), 'r-', linewidth=2, label='CPU')
                self.axes[1, 1].plot(relative_times, list(self.monitoring_data['memory_usage']), 'm-', linewidth=2, label='Memory')
                self.axes[1, 1].set_ylabel('Usage %', color='white')
                self.axes[1, 1].legend()
                self.axes[1, 1].grid(True, alpha=0.3)
            
        except Exception as e:
            console.print(f"[red]Error updating plots: {e}[/red]")
    
    def create_tkinter_dashboard(self):
        """Buat Tkinter dashboard dengan matplotlib"""
        root = tk.Tk()
        root.title("DDoS Defense Monitoring Dashboard")
        root.configure(bg='#1e1e1e')
        
        # Create matplotlib canvas
        canvas = FigureCanvasTkAgg(self.fig, root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Create control panel
        control_frame = tk.Frame(root, bg='#1e1e1e')
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Status labels
        status_frame = tk.Frame(control_frame, bg='#1e1e1e')
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.status_labels = {}
        status_items = [
            ('Packets/sec', '0'),
            ('Connections', '0'),
            ('Bandwidth', '0 MB/s'),
            ('CPU Usage', '0%'),
            ('Memory Usage', '0%'),
            ('Alerts', '0')
        ]
        
        for i, (label, value) in enumerate(status_items):
            tk.Label(status_frame, text=f"{label}:", bg='#1e1e1e', fg='white', font=('Arial', 10)).grid(row=i, column=0, sticky='w', padx=5)
            value_label = tk.Label(status_frame, text=value, bg='#1e1e1e', fg='yellow', font=('Arial', 10, 'bold'))
            value_label.grid(row=i, column=1, sticky='w', padx=5)
            self.status_labels[label] = value_label
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg='#1e1e1e')
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.start_button = tk.Button(button_frame, text="Start Monitoring", command=self.start_monitoring, 
                                    bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Monitoring", command=self.stop_monitoring, 
                                   bg='#f44336', fg='white', font=('Arial', 10, 'bold'), state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        # Start animation
        self.ani = animation.FuncAnimation(self.fig, self.update_plots, interval=1000, blit=False)
        
        return root
    
    def start_monitoring(self):
        """Start monitoring"""
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        console.print("[green]✅ Monitoring started![/green]")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        console.print("[yellow]⏹️  Monitoring stopped![/yellow]")
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                self.collect_system_metrics()
                
                # Update status labels
                if hasattr(self, 'status_labels'):
                    if self.monitoring_data['packets_per_sec']:
                        self.status_labels['Packets/sec'].config(text=f"{self.monitoring_data['packets_per_sec'][-1]:.2f}")
                    if self.monitoring_data['connections']:
                        self.status_labels['Connections'].config(text=f"{self.monitoring_data['connections'][-1]}")
                    if self.monitoring_data['bandwidth']:
                        self.status_labels['Bandwidth'].config(text=f"{self.monitoring_data['bandwidth'][-1]:.2f} MB/s")
                    if self.monitoring_data['cpu_usage']:
                        self.status_labels['CPU Usage'].config(text=f"{self.monitoring_data['cpu_usage'][-1]:.1f}%")
                    if self.monitoring_data['memory_usage']:
                        self.status_labels['Memory Usage'].config(text=f"{self.monitoring_data['memory_usage'][-1]:.1f}%")
                    
                    self.status_labels['Alerts'].config(text=f"{len(self.attack_alerts)}")
                
                time.sleep(1)
                
            except Exception as e:
                console.print(f"[red]Error in monitoring loop: {e}[/red]")
                time.sleep(1)
    
    def show_console_dashboard(self):
        """Show console-based dashboard"""
        self.show_banner()
        
        with Live(self.generate_console_dashboard(), refresh_per_second=1) as live:
            try:
                while True:
                    self.collect_system_metrics()
                    live.update(self.generate_console_dashboard())
                    time.sleep(1)
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Monitoring dihentikan oleh user[/bold yellow]")
    
    def generate_console_dashboard(self):
        """Generate console dashboard"""
        # System stats table
        stats_table = Table(title="System Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        stats_table.add_column("Status", style="yellow")
        
        if self.monitoring_data['packets_per_sec']:
            packets = self.monitoring_data['packets_per_sec'][-1]
            status = "🚨 HIGH" if packets > config.DDoS_THRESHOLDS['requests_per_second'] else "✅ NORMAL"
            stats_table.add_row("Packets/sec", f"{packets:.2f}", status)
        
        if self.monitoring_data['connections']:
            connections = self.monitoring_data['connections'][-1]
            status = "🚨 HIGH" if connections > config.DDoS_THRESHOLDS['max_connections_per_ip'] * 10 else "✅ NORMAL"
            stats_table.add_row("Active Connections", str(connections), status)
        
        if self.monitoring_data['bandwidth']:
            bandwidth = self.monitoring_data['bandwidth'][-1]
            status = "🚨 HIGH" if bandwidth > config.DDoS_THRESHOLDS['bandwidth_threshold'] / (1024 * 1024) else "✅ NORMAL"
            stats_table.add_row("Bandwidth", f"{bandwidth:.2f} MB/s", status)
        
        if self.monitoring_data['cpu_usage']:
            cpu = self.monitoring_data['cpu_usage'][-1]
            status = "⚠️  HIGH" if cpu > 80 else "✅ NORMAL"
            stats_table.add_row("CPU Usage", f"{cpu:.1f}%", status)
        
        if self.monitoring_data['memory_usage']:
            memory = self.monitoring_data['memory_usage'][-1]
            status = "⚠️  HIGH" if memory > 80 else "✅ NORMAL"
            stats_table.add_row("Memory Usage", f"{memory:.1f}%", status)
        
        # Recent alerts table
        alerts_table = Table(title="Recent Alerts (Last 5)")
        alerts_table.add_column("Time", style="cyan")
        alerts_table.add_column("Type", style="red")
        alerts_table.add_column("Severity", style="yellow")
        alerts_table.add_column("Value", style="white")
        
        for alert in self.attack_alerts[-5:]:
            time_str = time.strftime("%H:%M:%S", time.localtime(alert['timestamp']))
            alerts_table.add_row(
                time_str,
                alert['type'],
                alert['severity'],
                alert['value']
            )
        
        return Panel(f"{stats_table}\n\n{alerts_table}")
    
    def show_banner(self):
        """Show banner"""
        banner = pyfiglet.figlet_format("DDoS MONITOR", font="slant")
        console.print(Panel(banner, style="bold cyan"))
        console.print("[bold yellow]📊 Real-time Monitoring Dashboard Aktif![/bold yellow]")
        console.print("[bold green]Monitoring sistem dan network untuk deteksi serangan...[/bold green]\n")

def main():
    """Main function"""
    monitor = DDoSMonitor()
    
    console.print("\n[bold cyan]DDoS Monitoring Dashboard untuk Pembelajaran Defense[/bold cyan]")
    console.print("1. GUI Dashboard (Matplotlib + Tkinter)")
    console.print("2. Console Dashboard")
    
    choice = input("\nPilihan Anda (1-2): ")
    
    if choice == "1":
        try:
            root = monitor.create_tkinter_dashboard()
            root.mainloop()
        except Exception as e:
            console.print(f"[red]Error creating GUI dashboard: {e}[/red]")
            console.print("[yellow]Falling back to console dashboard...[/yellow]")
            monitor.show_console_dashboard()
    elif choice == "2":
        monitor.show_console_dashboard()
    else:
        console.print("[red]Pilihan tidak valid![/red]")

if __name__ == "__main__":
    main()
