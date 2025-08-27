# DDoS Defense Learning Project

**⚠️ PERINGATAN PENTING:**
Proyek ini dibuat SEMATA-MATA untuk tujuan pembelajaran dan testing defensif. 
JANGAN PERNAH gunakan untuk menyerang sistem orang lain!

## Tujuan Pembelajaran
- Memahami cara kerja serangan DDoS
- Belajar mendeteksi serangan DDoS
- Implementasi sistem pertahanan DDoS
- Testing keamanan sistem sendiri

## Komponen Proyek
1. **ddos_simulator.py** - Simulator serangan untuk testing defensif (dengan pilihan target IP & port)
2. **ddos_detector.py** - Sistem deteksi serangan DDoS
3. **mitigation.py** - Tools untuk memblokir serangan
4. **monitor.py** - Dashboard monitoring traffic
5. **config.py** - Konfigurasi sistem
6. **test_simulator.py** - Test suite untuk validasi konfigurasi

## Cara Penggunaan
1. Install dependencies: `pip install -r requirements.txt`
2. Jalankan simulator: `python ddos_simulator.py`
3. Jalankan detector: `python ddos_detector.py`
4. Monitor dashboard: `python monitor.py`

## 🎯 Fitur Target Selection

### **Keamanan Target IP**
- **Safe Targets**: IP yang aman untuk testing (router, gateway lokal)
- **Dangerous IP Detection**: Otomatis deteksi IP berbahaya (localhost, broadcast)
- **Custom IP Input**: Bisa input IP custom dengan validasi
- **Port Selection**: Pilihan port umum atau custom port

### **Target yang Aman untuk Testing**
- `192.168.1.1` - Router lokal
- `192.168.1.254` - Gateway lokal  
- `10.0.0.1` - Network lain
- `172.16.0.1` - Network lain

### **Port yang Umum untuk Testing**
- Port 80 (HTTP) - Web server
- Port 443 (HTTPS) - Secure web
- Port 22 (SSH) - Remote access
- Port 21 (FTP) - File transfer
- Port 53 (DNS) - Domain resolution

## Legal Disclaimer
- Hanya gunakan pada sistem yang Anda miliki
- Jangan gunakan untuk testing sistem orang lain
- Tujuan utama: pembelajaran cybersecurity defensif
