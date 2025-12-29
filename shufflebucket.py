import random

class CollatzBitCipher:
    def __init__(self):
        # ÖRNEK S-BOX (Bunu değiştirirsen artık sonuç da değişecek!)
        self.sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
        
    def run(self):
        print("--- S-BOX DUYARLI & DENGELİ BİT ÜRETECİ ---")
        
        try:
            seed_input = input("Başlangıç Tohumu (Seed) giriniz: ")
            user_seed = int(seed_input)
        except ValueError:
            user_seed = 1923
            print("Varsayılan seed atandı.")

        # --- KRİTİK DÜZELTME BURADA ---
        # S-Box'ın içeriğine göre benzersiz bir sayı (imza) üretiyoruz.
        # i+1 ile çarpıyoruz ki [1, 2] ile [2, 1] aynı sonucu vermesin (Sıra önemli olsun).
        sbox_signature = sum(val * (i + 1) for i, val in enumerate(self.sbox))
        
        # Kullanıcının seed'i ile S-Box imzasını birleştiriyoruz.
        # Artık S-Box değişirse, 'final_seed' değişir, dolayısıyla shuffle değişir!
        final_seed = user_seed + sbox_signature
        
        # Rastgelelik motorunu bu yeni "Güçlendirilmiş Seed" ile başlatıyoruz.
        rng = random.Random(final_seed)
        
        target_total = 32
        target_half = target_total // 2
        
        print(f"\nHedef: {target_total} bit (%50 - %50 dağılım)...\n")

        collected_zeros = []
        collected_ones = []
        state = user_seed # Collatz motoru hala kullanıcının girdiği saf sayıdan başlar
        
        loop_count = 0
        while len(collected_zeros) < target_half or len(collected_ones) < target_half:
            loop_count += 1
            
            # Collatz Adımı
            if state % 2 == 0:
                state //= 2
                raw_bit = 0
            else:
                state = 3 * state + 1
                raw_bit = 1
            
            # S-Box Karıştırma
            sbox_val = self.sbox[state % 16]
            processed_bit = (raw_bit + sbox_val) % 2
            
            # Kova Doldurma
            if processed_bit == 0:
                if len(collected_zeros) < target_half:
                    collected_zeros.append(0)
            else:
                if len(collected_ones) < target_half:
                    collected_ones.append(1)
            
            if loop_count > 50000: break

        # Karıştırma (Artık S-Box'a göre değişiyor!)
        final_bits = collected_zeros + collected_ones
        rng.shuffle(final_bits)
        
        print("="*50)
        print("SONUÇ: ŞİFRELİ BİT DİZİSİ")
        print("="*50)
        
        bit_string = "".join(map(str, final_bits))
        print(f"\n>> ÇIKTI (String): {bit_string}")
        print(f"\n>> ÇIKTI (Liste) : {final_bits}")
        
        print("\n" + "-"*50)
        zeros = final_bits.count(0)
        ones = final_bits.count(1)
        
        if zeros == ones:
            print(f"DURUM   : ✅ BAŞARILI (0:{zeros}, 1:{ones})")
        else:
            print(f"DURUM   : ❌ HATA")
        print("="*50)

if __name__ == "__main__":
    algo = CollatzBitCipher()
    algo.run()