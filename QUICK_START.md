# 🚀 Quick Start Guide - DDoS Defense Learning Project

## ⚡ Langkah Cepat untuk Memulai

### 1. **Install Dependencies**
```bash
# Install semua package yang diperlukan
pip install -r requirements.txt
```

### 2. **Jalankan Main Launcher**
```bash
python main.py
```

### 3. **Pilih Menu yang Diinginkan**
- **1** - DDoS Simulator (untuk testing defensif)
- **2** - DDoS Detector (untuk deteksi serangan)
- **3** - DDoS Mitigation (untuk pertahanan)
- **4** - Monitoring Dashboard (untuk monitoring real-time)
- **5** - Install Dependencies
- **6** - System Check

## 🎯 **Urutan Penggunaan yang Disarankan**

### **Step 1: Setup Awal**
```bash
python main.py
# Pilih opsi 5 (Install Dependencies)
# Pilih opsi 6 (System Check)
```

### **Step 2: Monitoring Baseline**
```bash
python main.py
# Pilih opsi 4 (Monitoring Dashboard)
# Pilih 1 untuk GUI Dashboard atau 2 untuk Console
```

### **Step 3: Testing Defensif**
```bash
python main.py
# Pilih opsi 1 (DDoS Simulator)
# Pilih tipe serangan (1-4)
# Konfirmasi dengan 'y'
```

### **Step 4: Deteksi & Pertahanan**
```bash
# Terminal 1: Jalankan Detector
python ddos_detector.py

# Terminal 2: Jalankan Mitigation
python mitigation.py

# Terminal 3: Jalankan Simulator
python ddos_simulator.py
```

## 🔧 **Troubleshooting Cepat**

### **Error: "Module not found"**
```bash
pip install -r requirements.txt
```

### **Error: "Permission denied"**
```bash
# Windows: Run as Administrator
# Linux/Mac: sudo python main.py
```

### **Error: "Scapy requires root"**
```bash
# Linux/Mac: sudo python ddos_simulator.py
# Windows: Run as Administrator
```

### **Dashboard tidak muncul**
```bash
# Coba console dashboard dulu
python monitor.py
# Pilih opsi 2 (Console Dashboard)
```

## 📊 **Monitoring & Testing**

### **Real-time Monitoring**
- **GUI Dashboard**: Grafik real-time dengan matplotlib
- **Console Dashboard**: Text-based monitoring yang ringan
- **Log Files**: Semua aktivitas tersimpan di log

### **Testing Defensif**
- **SYN Flood**: Simulasi TCP connection flood
- **UDP Flood**: Simulasi UDP packet flood  
- **HTTP Flood**: Simulasi HTTP request flood
- **Mixed Attack**: Kombinasi semua tipe serangan

### **Detection & Mitigation**
- **Auto-detection**: Sistem otomatis mendeteksi anomaly
- **IP Blocking**: Block IP yang mencurigakan
- **Rate Limiting**: Batasi request rate per IP
- **Whitelist**: IP yang tidak akan diblokir

## ⚠️ **Peringatan Penting**

1. **HANYA untuk sistem sendiri** - Jangan test sistem orang lain!
2. **Tujuan pembelajaran** - Bukan untuk serangan nyata
3. **Logging aktif** - Semua aktivitas tercatat
4. **Firewall aware** - Pastikan firewall tidak memblokir

## 🎓 **Apa yang Akan Anda Pelajari**

- ✅ Cara kerja serangan DDoS
- ✅ Teknik deteksi anomaly network
- ✅ Implementasi sistem pertahanan
- ✅ Monitoring dan alerting
- ✅ Rate limiting dan IP blocking
- ✅ Real-time dashboard development
- ✅ Network security best practices

## 🚀 **Next Steps**

Setelah memahami dasar-dasar:
1. **Customize thresholds** di `config.py`
2. **Add new attack types** di simulator
3. **Implement ML-based detection**
4. **Add email/SMS alerts**
5. **Integrate dengan SIEM tools**

---

**🎯 Happy Learning! Semoga proyek ini membantu Anda memahami cybersecurity defense!**
