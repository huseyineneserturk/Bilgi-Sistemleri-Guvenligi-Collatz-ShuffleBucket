import random

class CollatzBitCipher:
    """
    Collatz Sanısı (3n+1) ve S-Box kullanarak 
    Kriptografik Rastgele Sayı Üreteci (CSPRNG) simülasyonu.
    """
    def __init__(self):
        # S-Box: Doğrusallığı bozmak ve kaosu artırmak için kullanılan karışıklık tablosu.
        # Bu tablo algoritmanın 'Gizli Anahtarı' gibi davranır.
        self.sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
        
    def run(self):
        print("--- COLLATZ & S-BOX TABANLI ŞİFRELEME ---")
        
        # 1. Kullanıcıdan Seed (Tohum) Alma
        try:
            seed_input = input("Başlangıç Tohumu (Seed) giriniz: ")
            seed = int(seed_input)
        except ValueError:
            seed = 1923
            print("Hatalı giriş, varsayılan seed (1923) atandı.")

        # Seed'e bağlı deterministik karıştırma için random motorunu başlatıyoruz.
        rng = random.Random(seed)
        
        target_total = 32 # İstenen çıktı uzunluğu (Bit)
        target_half = target_total // 2  # Hedef: Eşit sayıda 0 ve 1 (16'şar tane)
        
        print(f"\nHedef: %50-%50 Dağılımlı {target_total} bitlik güvenli dizi üretiliyor...\n")

        collected_zeros = []
        collected_ones = []
        state = seed
        
        # 2. Üretim Döngüsü (Kova Mantığı)
        # Eşit sayıda 0 ve 1 elde edene kadar Collatz motorunu çalıştırır.
        loop_count = 0
        while len(collected_zeros) < target_half or len(collected_ones) < target_half:
            loop_count += 1
            
            # A) Collatz Matematiksel İşlemi
            if state % 2 == 0:
                state //= 2
                raw_bit = 0
            else:
                state = 3 * state + 1
                raw_bit = 1
            
            # B) S-Box ile Yapısal Karıştırma
            # Ham biti S-Box tablosundaki değerle harmanlıyoruz.
            sbox_val = self.sbox[state % 16]
            processed_bit = (raw_bit + sbox_val) % 2
            
            # C) Dengeleme (0 ve 1 sayılarını zorunlu eşitleme)
            if processed_bit == 0:
                if len(collected_zeros) < target_half:
                    collected_zeros.append(0)
            else:
                if len(collected_ones) < target_half:
                    collected_ones.append(1)
            
            if loop_count > 50000: # Sonsuz döngü önleyici
                print("! Uyarı: Maksimum döngü sınırına ulaşıldı.")
                break

        # 3. Final Karıştırma (Shuffle)
        # Sıralı birikmiş 0 ve 1'leri seed'e göre karıştırarak homojen hale getirir.
        final_bits = collected_zeros + collected_ones
        rng.shuffle(final_bits)
        
        # 4. Çıktı Gösterimi
        print("="*50)
        print("SONUÇ: ŞİFRELİ BİT DİZİSİ")
        print("="*50)
        
        # String formatı (Kopyalama için kolay)
        bit_string = "".join(map(str, final_bits))
        print(f"\n>> ÇIKTI (String): {bit_string}")
        
        # Liste formatı (Analiz için)
        print(f"\n>> ÇIKTI (Liste) : {final_bits}")
        
        print("\n" + "-"*50)
        zeros = final_bits.count(0)
        ones = final_bits.count(1)
        
        # Doğrulama
        if zeros == ones:
            print(f"DURUM   : ✅ BAŞARILI (0:{zeros}, 1:{ones})")
        else:
            print(f"DURUM   : ❌ DENGESİZ")
        print("="*50)

if __name__ == "__main__":
    algo = CollatzBitCipher()
    algo.run()