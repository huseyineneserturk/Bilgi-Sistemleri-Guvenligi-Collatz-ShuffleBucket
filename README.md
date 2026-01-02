# 🎲 Collatz Cipher Generator

<div align="center">

**🔐 Collatz Sanısı (3n+1) + Kriptografik S-Box = Kaos Teorisi ile Şifreleme**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-Educational-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

*Matematik, kaos ve kriptografi buluşuyor!*

---

### ⚡ Hızlı Başlangıç
```bash
python shufflebucket.py
```

</div>

---

## 📐 Algoritma Akış Diyagramı

![Collatz Cipher Flow](diagram.png)

---

## 🎯 Nedir Bu Proje?

Bu proje, **Collatz Sanısı** olarak bilinen ünlü matematik problemini kriptografik bir araç haline getiriyor! Deterministik ama tahmin edilemez bit dizileri üreterek, eğitim amaçlı şifreleme demonstrasyonu sunuyor.

### 🌟 Temel Özellikler

| Özellik | Açıklama |
|---------|----------|
| ✅ **Mükemmel Denge** | Her zaman %50 sıfır, %50 bir |
| 🔐 **S-Box Karıştırma** | Kriptografik katman ile lineerlik kırılması |
| 🎯 **Deterministik** | Aynı seed → Aynı sonuç (test edilebilir!) |
| ⚡ **Collatz Kaosu** | Tahmin edilemez sayı üretimi |
| 🧪 **Eğitici** | Açık kaynak, anlaşılır kod yapısı |

---

## 🔧 Algoritma Nasıl Çalışır?

### 📊 Pseudo Code

```
FUNCTION generate_cipher(seed):
    // Başlangıç Ayarları
    INITIALIZE s_box = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    INITIALIZE bucket_0 = []
    INITIALIZE bucket_1 = []
    INITIALIZE current = seed
    
    // Ana Üretim Döngüsü
    WHILE (LENGTH(bucket_0) < 16) OR (LENGTH(bucket_1) < 16):
        
        // 1. Collatz Kuralı
        IF current MOD 2 == 0:
            raw_bit = 0
            current = current / 2
        ELSE:
            raw_bit = 1
            current = (3 * current) + 1
        END IF
        
        // 2. S-Box ile Karıştırma
        index = current MOD 16
        scrambled = s_box[index]
        final_bit = scrambled MOD 2
        
        // 3. Kova Sistemi
        IF final_bit == 0 AND LENGTH(bucket_0) < 16:
            APPEND final_bit TO bucket_0
        ELSE IF final_bit == 1 AND LENGTH(bucket_1) < 16:
            APPEND final_bit TO bucket_1
        END IF
        
    END WHILE
    
    // 4. Final Karıştırma
    combined = bucket_0 + bucket_1
    SHUFFLE combined WITH SEED(seed)
    
    RETURN combined
END FUNCTION
```

### 🔄 Adım Adım İşleyiş

#### **1️⃣ Başlangıç**
```python
seed = 1923  # Kullanıcıdan alınan tohum değeri
current = seed
```

#### **2️⃣ Collatz Döngüsü**
```
Sayı çift mi? → Evet: 2'ye böl (bit: 0)
             → Hayır: 3n+1 yap (bit: 1)
```

#### **3️⃣ S-Box Karıştırma**
```
Ham bit → S-Box tablosu → Karıştırılmış bit
```

#### **4️⃣ Kova Toplama**
```
0'lar → Kova 0 (16 adet)
1'ler → Kova 1 (16 adet)
```

#### **5️⃣ Fisher-Yates Shuffle**
```
32 bit → Deterministik karıştırma → Dengeli dağılım
```

---

## 🚀 Kurulum ve Kullanım

### Gereksinimler
- Python 3.7 veya üzeri
- Standart kütüphaneler (random, math)

### Çalıştırma
```bash
# Terminal'de
python shufflebucket.py

# Bir seed giriniz (örn: 1923)
```

---

## 📊 Örnek Çıktılar

### 🎯 Taslak Anahtar (Kod İçindeki S-Box ile)

```
--- S-BOX DUYARLI & DENGELİ BİT ÜRETECİ ---
Başlangıç Tohumu (Seed) giriniz: 1923

Hedef: 32 bit (%50 - %50 dağılım)...

==================================================
SONUÇ: ŞİFRELİ BİT DİZİSİ
==================================================

>> ÇIKTI (String): 11000100110001010111001001101101

>> ÇIKTI (Liste) : [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 
                    0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 
                    0, 1, 1, 0, 1, 1, 0, 1]

--------------------------------------------------
DURUM   : ✅ BAŞARILI (0:16, 1:16)
==================================================
```

### 🏆 Challenge - Orijinal Anahtar

```
--- S-BOX DUYARLI & DENGELİ BİT ÜRETECİ ---
Başlangıç Tohumu (Seed) giriniz: 1923

Hedef: 32 bit (%50 - %50 dağılım)...

==================================================
SONUÇ: ŞİFRELİ BİT DİZİSİ
==================================================

>> ÇIKTI (String): 01111100000111010110000011100110

>> ÇIKTI (Liste) : [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 
                    1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 
                    1, 1, 1, 0, 0, 1, 1, 0]

--------------------------------------------------
DURUM   : ✅ BAŞARILI (0:16, 1:16)
==================================================
```

**🎮 Meydan Okuma:** Yukarıdaki çıktıyı üreten gizli S-Box'ı bulabilir misin?

---

## 🧪 Kullanım Alanları

| Alan | Açıklama |
|------|----------|
| 🎓 **Eğitim** | Kriptografi ve kaos teorisi öğretimi |
| 🔬 **Araştırma** | PRNG/CSPRNG analizi |
| 🧮 **Matematik** | Collatz sanısı çalışmaları |
| 💻 **Simülasyon** | Rastgele sayı üreteci testleri |

---

## 🔬 Diehard Test Suite

Bu proje, rastgele sayı üretecinin kalitesini değerlendirmek için **Diehard Test Suite** içerir!

### 📊 Testler

Implementasyon edilen testler:

| Test | Açıklama | Amaç |
|------|----------|------|
| **Frequency Test** | 0/1 dengesi | Monobit dağılımı |
| **Runs Test** | Ardışık bit grupları | Run dağılımı |
| **Longest Run** | En uzun 1 dizisi | Blok içi maksimum |
| **Poker Test** | m-bit paternleri | Segment dağılımı |
| **Autocorrelation** | Kendisiyle korelasyon | Bağımsızlık |
| **Matrix Rank** | Matris rankları | Lineer bağımsızlık |

### 🚀 Nasıl Çalıştırılır?

```bash
# Diehard testlerini çalıştır
python diehard_tests.py

# Veya direkt seed ile
python diehard_tests.py 1923
```

### 📈 Örnek Test Çıktısı

```
🎲 Collatz Cipher - Diehard Test Suite
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

======================================================================
  COLLATZ CIPHER - DIEHARD TEST SÜİTİ
======================================================================
Seed: 1923
Bit sayısı: 100,000
======================================================================

📊 Veri üretiliyor...
✅ 100,000 bit üretildi

🔍 Çalıştırılıyor: Frequency...
   ✅ BAŞARILI

🔍 Çalıştırılıyor: Runs...
   ✅ BAŞARILI

🔍 Çalıştırılıyor: Longest Run...
   ✅ BAŞARILI

🔍 Çalıştırılıyor: Poker (m=4)...
   ✅ BAŞARILI

🔍 Çalıştırılıyor: Autocorrelation (d=1)...
   ✅ BAŞARILI

🔍 Çalıştırılıyor: Autocorrelation (d=2)...
   ✅ BAŞARILI

🔍 Çalıştırılıyor: Binary Matrix Rank...
   ✅ BAŞARILI

======================================================================
  ÖZET: 7/7 test başarılı (100.0%)
======================================================================
```

### 🎯 Test Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Hızlı Test** | 10,000 bit | Temel kontrol |
| **Orta Test** | 100,000 bit | Önerilen |
| **Kapsamlı Test** | 1,000,000 bit | Detaylı analiz |

### 📚 Test Metodolojisi

Her test, belirli istatistiksel özellikleri kontrol eder:

1. **Ki-Kare Testi**: Dağılım analizi (α=0.05)
2. **Z-Skoru**: Normal dağılım kontrolü
3. **Kritik Değerler**: %95 güven aralığı

### ⚠️ Test Sonuçları Hakkında

> **Not:** Bu testler, algoritmanın rastgelelik kalitesini **eğitim amaçlı** değerlendirir. Üretim ortamında kullanım için:
> - NIST SP 800-22 test suite
> - TestU01 battery
> - Dieharder (genişletilmiş Diehard)
> 
> gibi endüstri standardı test araçları kullanılmalıdır.

---

## 🎨 Teknik Detaylar

### S-Box Yapısı
```python
s_box = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
```
- 16 elemanlı permütasyon
- Lineer ilişkileri bozar
- Kriptografik karıştırma sağlar

### Collatz Fonksiyonu
```
f(n) = n/2     eğer n çift ise
f(n) = 3n+1    eğer n tek ise
```

### Fisher-Yates Shuffle
- Deterministik karıştırma
- O(n) zaman karmaşıklığı
- Uniform dağılım garantisi

---

## ⚠️ Önemli Notlar

> **📢 Uyarı:** Bu proje **eğitim amaçlıdır**. Gerçek üretim ortamlarında endüstri standardı kriptografik kütüphaneler (örn: `cryptography`, `PyCryptodome`) kullanılmalıdır.

### Neden Üretim Ortamında Kullanılmamalı?

1. ❌ **Kriptografik Dayanıklılık Testi Yok:** Profesyonel inceleme ve testlerden geçmemiş
2. ❌ **Sınırlı Entropi:** 32-bit çıktı, modern standartlar için yetersiz
3. ❌ **Collatz Sanısı:** Henüz matematiksel olarak kanıtlanmamış bir teori
4. ❌ **S-Box Güvenliği:** Endüstri standardı S-Box'lar (AES, DES vb.) kullanılmalı

---

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılara açıktır!

```bash
# Repo'yu fork edin
# Değişikliklerinizi yapın
# Pull request gönderin
```

---

## 📝 Lisans

Bu proje eğitim amaçlı olarak geliştirilmiştir. Özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz.

---

## 🌟 Yıldız Vermeyi Unutmayın!

Projeyi beğendiyseniz ⭐ vermeyi unutmayın!

---

<div align="center">

**Matematik + Kaos + Kriptografi = 🎲**

*Hüseyin Enes Ertürk tarafından geliştirildi*

[🔝 Yukarı Çık](#-collatz-cipher-generator)

</div>
