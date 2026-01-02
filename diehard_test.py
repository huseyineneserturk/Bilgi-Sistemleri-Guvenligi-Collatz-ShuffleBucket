#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collatz Cipher - Diehard Test Suite
====================================
Collatz tabanlı rastgele bit üretecinin istatistiksel testleri.

Diehard testleri, rastgele sayı üreteçlerinin kalitesini değerlendirmek için
kullanılan klasik test setidir. Bu implementasyon, temel Diehard testlerini
içerir ve sonuçları raporlar.
"""

import random
import math
from collections import Counter
from typing import List, Tuple
import struct


# ============================================================================
# COLLATZ ŞİFRELEME ALGORİTMASI (Orijinal)
# ============================================================================

def generate_cipher_bits(seed: int, num_bits: int = 32) -> List[int]:
    """
    Collatz tabanlı dengeli bit dizisi üretir.
    
    Args:
        seed: Başlangıç tohumu
        num_bits: Üretilecek bit sayısı (çift sayı olmalı)
    
    Returns:
        Dengeli bit dizisi
    """
    s_box = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    
    target_per_bucket = num_bits // 2
    bucket_0 = []
    bucket_1 = []
    current = seed
    
    while len(bucket_0) < target_per_bucket or len(bucket_1) < target_per_bucket:
        # Collatz kuralı
        if current % 2 == 0:
            current = current // 2
        else:
            current = (3 * current) + 1
        
        # S-Box karıştırma
        index = current % 16
        scrambled = s_box[index]
        final_bit = scrambled % 2
        
        # Kova sistemi
        if final_bit == 0 and len(bucket_0) < target_per_bucket:
            bucket_0.append(final_bit)
        elif final_bit == 1 and len(bucket_1) < target_per_bucket:
            bucket_1.append(final_bit)
    
    # Final karıştırma
    combined = bucket_0 + bucket_1
    random.seed(seed)
    random.shuffle(combined)
    
    return combined


def generate_large_dataset(seed: int, num_bits: int) -> List[int]:
    """
    Büyük veri seti üretir (Diehard testleri için).
    
    Args:
        seed: Başlangıç tohumu
        num_bits: Toplam bit sayısı
    
    Returns:
        Bit dizisi
    """
    all_bits = []
    current_seed = seed
    
    while len(all_bits) < num_bits:
        chunk = generate_cipher_bits(current_seed, min(1024, num_bits - len(all_bits)))
        all_bits.extend(chunk)
        current_seed = (current_seed * 1103515245 + 12345) % (2**31)  # LCG
    
    return all_bits[:num_bits]


# ============================================================================
# YARDIMCI FONKSİYONLAR
# ============================================================================

def bits_to_bytes(bits: List[int]) -> bytes:
    """Bit listesini byte dizisine çevirir."""
    byte_list = []
    for i in range(0, len(bits), 8):
        byte_chunk = bits[i:i+8]
        if len(byte_chunk) == 8:
            byte_val = int(''.join(map(str, byte_chunk)), 2)
            byte_list.append(byte_val)
    return bytes(byte_list)


def bits_to_integers(bits: List[int], bit_width: int = 32) -> List[int]:
    """Bit dizisini tam sayılara çevirir."""
    integers = []
    for i in range(0, len(bits), bit_width):
        chunk = bits[i:i+bit_width]
        if len(chunk) == bit_width:
            val = int(''.join(map(str, chunk)), 2)
            integers.append(val)
    return integers


def chi_square_test(observed: List[int], expected: List[float]) -> Tuple[float, bool]:
    """
    Ki-kare testi yapar.
    
    Returns:
        (chi_square_value, is_random)
    """
    chi_square = 0
    for obs, exp in zip(observed, expected):
        if exp > 0:
            chi_square += ((obs - exp) ** 2) / exp
    
    # Serbestlik derecesi = kategoriler - 1
    df = len(observed) - 1
    
    # Kritik değer (α=0.05 için yaklaşık)
    critical_values = {1: 3.841, 2: 5.991, 3: 7.815, 7: 14.067, 15: 24.996, 255: 293.248}
    critical = critical_values.get(df, df * 1.2)  # Yaklaşık
    
    return chi_square, chi_square < critical


# ============================================================================
# DİEHARD TEST FONKSİYONLARI
# ============================================================================

def test_frequency(bits: List[int]) -> dict:
    """
    Frekans Testi (Monobit Test)
    
    Bitlerdeki 0 ve 1'lerin dengeli olup olmadığını kontrol eder.
    """
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    
    expected = n / 2
    chi_square = ((ones - expected) ** 2 + (zeros - expected) ** 2) / expected
    
    # Ki-kare değeri 3.841'den küçükse (df=1, α=0.05) geçer
    passed = chi_square < 3.841
    
    return {
        "test": "Frequency Test (Monobit)",
        "ones": ones,
        "zeros": zeros,
        "expected": expected,
        "chi_square": round(chi_square, 4),
        "critical_value": 3.841,
        "passed": passed,
        "balance": f"{(ones/n)*100:.2f}% ones, {(zeros/n)*100:.2f}% zeros"
    }


def test_runs(bits: List[int]) -> dict:
    """
    Runs Testi
    
    Ardışık aynı bitlerin (runs) dağılımını kontrol eder.
    """
    n = len(bits)
    ones = sum(bits)
    proportion = ones / n
    
    # Ön koşul: proportion ≈ 0.5
    if abs(proportion - 0.5) >= 0.1:
        return {
            "test": "Runs Test",
            "passed": False,
            "note": "Proportion test failed (prerequisite)"
        }
    
    # Runs sayısını hesapla
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1
    
    # Beklenen runs ve varyans
    expected_runs = (2 * ones * (n - ones) / n) + 1
    variance = (2 * ones * (n - ones) * (2 * ones * (n - ones) - n)) / (n**2 * (n - 1))
    
    if variance <= 0:
        return {
            "test": "Runs Test",
            "passed": False,
            "note": "Invalid variance"
        }
    
    # Z-skoru
    z_score = (runs - expected_runs) / math.sqrt(variance)
    
    # |z| < 1.96 ise (α=0.05) geçer
    passed = abs(z_score) < 1.96
    
    return {
        "test": "Runs Test",
        "total_runs": runs,
        "expected_runs": round(expected_runs, 2),
        "z_score": round(z_score, 4),
        "critical_value": 1.96,
        "passed": passed
    }


def test_longest_run(bits: List[int], block_size: int = 128) -> dict:
    """
    Longest Run in Block Test
    
    Bloklar içindeki en uzun 1 dizisinin dağılımını kontrol eder.
    """
    n = len(bits)
    num_blocks = n // block_size
    
    if num_blocks < 10:
        return {
            "test": "Longest Run in Block",
            "passed": False,
            "note": "Insufficient data"
        }
    
    longest_runs = []
    for i in range(num_blocks):
        block = bits[i*block_size:(i+1)*block_size]
        current_run = 0
        max_run = 0
        
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        longest_runs.append(max_run)
    
    # Kategorilere ayır (128-bit bloklar için)
    categories = [0, 4, 5, 6, 7, 8]  # <=4, 5, 6, 7, 8, >=9
    observed = [0] * 6
    
    for run in longest_runs:
        if run <= 4:
            observed[0] += 1
        elif run == 5:
            observed[1] += 1
        elif run == 6:
            observed[2] += 1
        elif run == 7:
            observed[3] += 1
        elif run == 8:
            observed[4] += 1
        else:
            observed[5] += 1
    
    # Beklenen dağılım (teorik)
    expected = [num_blocks * p for p in [0.2148, 0.3672, 0.2305, 0.1875, 0.0879, 0.0121]]
    
    chi_square, passed = chi_square_test(observed, expected)
    
    return {
        "test": "Longest Run in Block",
        "num_blocks": num_blocks,
        "observed": observed,
        "expected": [round(e, 2) for e in expected],
        "chi_square": round(chi_square, 4),
        "passed": passed
    }


def test_poker(bits: List[int], m: int = 4) -> dict:
    """
    Poker Testi
    
    m-bitlik segmentlerin dağılımını kontrol eder.
    """
    n = len(bits) // m
    
    if n < 5 * (2**m):  # Yeterli örnek kontrolü
        return {
            "test": "Poker Test",
            "passed": False,
            "note": "Insufficient samples"
        }
    
    # m-bitlik segmentleri say
    segments = []
    for i in range(n):
        segment = bits[i*m:(i+1)*m]
        seg_val = int(''.join(map(str, segment)), 2)
        segments.append(seg_val)
    
    # Frekansları hesapla
    freq = Counter(segments)
    observed = [freq.get(i, 0) for i in range(2**m)]
    
    # Beklenen: her segment eşit olasılıkla
    expected = [n / (2**m)] * (2**m)
    
    chi_square, passed = chi_square_test(observed, expected)
    
    return {
        "test": f"Poker Test (m={m})",
        "segments": n,
        "unique_patterns": len(freq),
        "total_patterns": 2**m,
        "chi_square": round(chi_square, 4),
        "passed": passed
    }


def test_autocorrelation(bits: List[int], d: int = 1) -> dict:
    """
    Otokorelasyon Testi
    
    d pozisyon kaydırılmış bit dizisiyle korelasyonu kontrol eder.
    """
    n = len(bits) - d
    
    if n < 100:
        return {
            "test": f"Autocorrelation (d={d})",
            "passed": False,
            "note": "Insufficient data"
        }
    
    # XOR işlemi ve 1'leri say
    matches = sum(bits[i] == bits[i+d] for i in range(n))
    
    # Beklenen değer
    expected = n / 2
    variance = n / 4
    
    # Z-skoru
    z_score = (matches - expected) / math.sqrt(variance)
    
    # |z| < 1.96 ise geçer
    passed = abs(z_score) < 1.96
    
    return {
        "test": f"Autocorrelation Test (d={d})",
        "matches": matches,
        "expected": expected,
        "z_score": round(z_score, 4),
        "critical_value": 1.96,
        "passed": passed
    }


def test_binary_matrix_rank(bits: List[int], rows: int = 32, cols: int = 32) -> dict:
    """
    Binary Matrix Rank Testi
    
    Matris rankının dağılımını kontrol eder.
    """
    matrix_size = rows * cols
    num_matrices = len(bits) // matrix_size
    
    if num_matrices < 10:
        return {
            "test": "Binary Matrix Rank",
            "passed": False,
            "note": "Insufficient data for matrices"
        }
    
    def compute_rank(matrix):
        """Basit Gauss eliminasyonu ile rank hesapla."""
        m = [row[:] for row in matrix]  # Kopya
        rank = 0
        
        for col in range(min(rows, cols)):
            # Pivot bul
            pivot_row = None
            for row in range(rank, rows):
                if m[row][col] == 1:
                    pivot_row = row
                    break
            
            if pivot_row is None:
                continue
            
            # Satırları değiştir
            m[rank], m[pivot_row] = m[pivot_row], m[rank]
            
            # Eliminasyon
            for row in range(rows):
                if row != rank and m[row][col] == 1:
                    for c in range(cols):
                        m[row][c] ^= m[rank][c]
            
            rank += 1
        
        return rank
    
    ranks = []
    for i in range(num_matrices):
        matrix_bits = bits[i*matrix_size:(i+1)*matrix_size]
        matrix = [[matrix_bits[r*cols + c] for c in range(cols)] for r in range(rows)]
        rank = compute_rank(matrix)
        ranks.append(rank)
    
    # Rank dağılımını kategorize et
    rank_dist = Counter(ranks)
    full_rank = min(rows, cols)
    
    observed = [
        rank_dist.get(full_rank, 0),
        rank_dist.get(full_rank - 1, 0),
        sum(rank_dist.get(r, 0) for r in range(full_rank - 1))
    ]
    
    # Beklenen dağılım (teorik yaklaşım)
    p_full = 0.2888
    p_minus1 = 0.5776
    p_other = 0.1336
    expected = [num_matrices * p for p in [p_full, p_minus1, p_other]]
    
    chi_square, passed = chi_square_test(observed, expected)
    
    return {
        "test": "Binary Matrix Rank",
        "num_matrices": num_matrices,
        "rank_distribution": dict(rank_dist),
        "chi_square": round(chi_square, 4),
        "passed": passed
    }


# ============================================================================
# TEST SÜİTİ
# ============================================================================

def run_diehard_tests(seed: int, num_bits: int = 100000) -> dict:
    """
    Tüm Diehard testlerini çalıştırır.
    
    Args:
        seed: Başlangıç tohumu
        num_bits: Test için üretilecek bit sayısı
    
    Returns:
        Test sonuçları sözlüğü
    """
    print(f"\n{'='*70}")
    print(f"  COLLATZ CIPHER - DIEHARD TEST SÜİTİ")
    print(f"{'='*70}")
    print(f"Seed: {seed}")
    print(f"Bit sayısı: {num_bits:,}")
    print(f"{'='*70}\n")
    
    # Veri üretimi
    print("📊 Veri üretiliyor...")
    bits = generate_large_dataset(seed, num_bits)
    print(f"✅ {len(bits):,} bit üretildi\n")
    
    # Testler
    results = {}
    
    tests = [
        ("Frequency", lambda: test_frequency(bits)),
        ("Runs", lambda: test_runs(bits)),
        ("Longest Run", lambda: test_longest_run(bits)),
        ("Poker (m=4)", lambda: test_poker(bits, m=4)),
        ("Autocorrelation (d=1)", lambda: test_autocorrelation(bits, d=1)),
        ("Autocorrelation (d=2)", lambda: test_autocorrelation(bits, d=2)),
        ("Binary Matrix Rank", lambda: test_binary_matrix_rank(bits)),
    ]
    
    for test_name, test_func in tests:
        print(f"🔍 Çalıştırılıyor: {test_name}...")
        result = test_func()
        results[test_name] = result
        
        status = "✅ BAŞARILI" if result.get("passed") else "❌ BAŞARISIZ"
        print(f"   {status}")
        print()
    
    return results


def print_detailed_results(results: dict):
    """Test sonuçlarını detaylı yazdırır."""
    print(f"\n{'='*70}")
    print(f"  DETAYLI TEST SONUÇLARI")
    print(f"{'='*70}\n")
    
    for test_name, result in results.items():
        print(f"📋 {result['test']}")
        print(f"   {'─'*66}")
        
        for key, value in result.items():
            if key not in ["test", "passed"]:
                print(f"   • {key}: {value}")
        
        status = "✅ GEÇTI" if result.get("passed") else "❌ GEÇEMEDİ"
        print(f"   • Sonuç: {status}")
        print()
    
    # Özet
    total = len(results)
    passed = sum(1 for r in results.values() if r.get("passed"))
    
    print(f"{'='*70}")
    print(f"  ÖZET: {passed}/{total} test başarılı ({(passed/total)*100:.1f}%)")
    print(f"{'='*70}\n")


# ============================================================================
# ANA PROGRAM
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n🎲 Collatz Cipher - Diehard Test Suite")
    print("━" * 70)
    
    # Kullanıcıdan seed al
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    else:
        try:
            seed = int(input("\nBaşlangıç Tohumu (Seed) giriniz: "))
        except ValueError:
            print("❌ Geçersiz seed! Varsayılan 1923 kullanılıyor.")
            seed = 1923
    
    # Test sayısı
    print("\nÖnerilen bit sayıları:")
    print("  • Hızlı test: 10,000")
    print("  • Orta test: 100,000")
    print("  • Kapsamlı test: 1,000,000")
    
    try:
        num_bits = int(input("\nTest için bit sayısı (varsayılan 100000): ") or "100000")
    except ValueError:
        print("❌ Geçersiz sayı! 100,000 kullanılıyor.")
        num_bits = 100000
    
    # Testleri çalıştır
    results = run_diehard_tests(seed, num_bits)
    
    # Detaylı sonuçları göster
    print_detailed_results(results)
    
    print("💡 Not: Diehard testleri, rastgele sayı üreteçlerinin kalitesini")
    print("   değerlendirmek için endüstri standardı testlerdir.")
    print("\n   Daha kapsamlı testler için NIST SP 800-22 test süiti önerilir.")
