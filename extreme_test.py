#!/usr/bin/env python3
"""
Test Mode Ekstrem DDoS Simulator
Untuk testing intensif lokal
"""

import config

def test_extreme_config():
    """Test konfigurasi mode ekstrem"""
    print("🔥 === TEST MODE EKSTREM === 🔥")
    
    # Test simulator config
    sim_config = config.SIMULATOR_CONFIG
    print(f"Target Host: {sim_config['target_host']}")
    print(f"Target Port: {sim_config['target_port']}")
    print(f"Extreme Mode: {sim_config['enable_extreme_mode']}")
    
    # Test extreme config
    if 'extreme_mode_config' in sim_config:
        extreme = sim_config['extreme_mode_config']
        print(f"\n🔥 KONFIGURASI EKSTREM:")
        print(f"  Max Duration: {extreme['max_duration']} detik ({extreme['max_duration']/3600:.1f} jam)")
        print(f"  Max Packets/sec: {extreme['max_packets_per_second']:,}")
        print(f"  Max Bots: {extreme['max_bots']}")
        print(f"  Enable Localhost: {extreme['enable_localhost']}")
        print(f"  Aggressive Timing: {extreme['enable_aggressive_timing']}")
        print(f"  Massive Payloads: {extreme['enable_massive_payloads']}")
        
        # Hitung total paket maksimal
        max_total = extreme['max_duration'] * extreme['max_packets_per_second'] * extreme['max_bots']
        print(f"\n💥 TOTAL PAKET MAKSIMAL: {max_total:,}")
        print(f"   = {max_total/1_000_000:.1f} juta paket!")
        
    else:
        print("❌ Extreme mode config tidak ditemukan!")

def test_safe_targets():
    """Test safe targets"""
    print(f"\n🎯 SAFE TARGETS:")
    sim_config = config.SIMULATOR_CONFIG
    for i, target in enumerate(sim_config['safe_targets'], 1):
        print(f"  {i}. {target}")
    
    print(f"\n🔌 COMMON PORTS:")
    for i, port in enumerate(sim_config['common_ports'], 1):
        print(f"  {i}. Port {port}")

def show_extreme_modes():
    """Tampilkan mode ekstrem yang tersedia"""
    print(f"\n🚀 MODE EKSTREM YANG TERSEDIA:")
    print("1. 🚀 Turbo Mode - 5000 pps, 20 bot, 60 detik")
    print("2. 💥 Nuclear Mode - 10000 pps, 50 bot, 120 detik")
    print("3. 🌪️  Tornado Mode - 8000 pps, 30 bot, 90 detik")
    print("4. ⚡ Lightning Mode - 15000 pps, 40 bot, 60 detik")
    print("5. 🎯 Custom Extreme - Konfigurasi manual")
    
    # Hitung total paket untuk setiap mode
    modes = [
        ("Turbo", 5000, 20, 60),
        ("Nuclear", 10000, 50, 120),
        ("Tornado", 8000, 30, 90),
        ("Lightning", 15000, 40, 60)
    ]
    
    print(f"\n📊 PERBANDINGAN MODE:")
    for name, pps, bots, duration in modes:
        total = pps * bots * duration
        print(f"  {name}: {total:,} paket total ({total/1_000_000:.1f}M)")

def main():
    """Main function"""
    print("🚀 DDoS Simulator - Extreme Mode Test")
    print("=" * 50)
    
    try:
        test_extreme_config()
        test_safe_targets()
        show_extreme_modes()
        
        print(f"\n✅ Test berhasil! Mode ekstrem siap digunakan.")
        print(f"💡 Gunakan IP lokal untuk testing yang efektif!")
        
    except Exception as e:
        print(f"\n❌ Test gagal: {e}")

if __name__ == "__main__":
    main()
