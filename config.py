# Configuration file untuk DDoS Defense Learning Project

# Threshold untuk deteksi DDoS
DDoS_THRESHOLDS = {
    'requests_per_second': 100,      # Jumlah request per detik yang dianggap normal
    'connection_timeout': 30,        # Timeout koneksi dalam detik
    'max_connections_per_ip': 10,    # Maksimal koneksi per IP
    'bandwidth_threshold': 1000000,  # 1MB per detik
}

# Konfigurasi simulator
SIMULATOR_CONFIG = {
    'target_host': '127.0.0.1',     # Hanya localhost untuk testing
    'target_port': 80,               # Port target
    'attack_duration': 30,           # Durasi serangan dalam detik
    'packets_per_second': 50,        # Jumlah paket per detik
}

# Konfigurasi monitoring
MONITORING_CONFIG = {
    'log_file': 'ddos_attack.log',
    'alert_email': 'admin@localhost',
    'enable_notifications': True,
}

# Konfigurasi mitigation
MITIGATION_CONFIG = {
    'enable_auto_block': True,
    'block_duration': 300,           # 5 menit
    'whitelist_ips': ['127.0.0.1'],  # IP yang tidak akan diblokir
    'rate_limiting': True,
}

# Warna untuk output
COLORS = {
    'success': '\033[92m',
    'warning': '\033[93m',
    'error': '\033[91m',
    'info': '\033[94m',
    'reset': '\033[0m'
}
