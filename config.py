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
    'target_host': '192.168.1.1',   # Default target (bisa diubah saat runtime)
    'target_port': 80,               # Port target
    'attack_duration': 30,           # Durasi serangan dalam detik
    'packets_per_second': 50,        # Jumlah paket per detik
    'enable_target_selection': True, # Enable pilihan target IP
    'enable_port_selection': True,   # Enable pilihan port
    'safe_targets': [                # IP yang aman untuk testing
        '192.168.1.1',              # Router lokal
        '192.168.1.254',            # Gateway lokal
        '10.0.0.1',                 # Network lain
        '172.16.0.1'                # Network lain
    ],
    'common_ports': [                # Port yang umum untuk testing
        80,    # HTTP
        443,   # HTTPS
        22,    # SSH
        21,    # FTP
        25,    # SMTP
        53,    # DNS
        3389,  # RDP
        8080,  # HTTP Alt
        8443    # HTTPS Alt
    ]
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
