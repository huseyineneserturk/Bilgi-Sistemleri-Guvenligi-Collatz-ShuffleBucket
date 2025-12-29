# Collatz Cipher Generator 🎲

Bu proje, ünlü matematiksel problem **Collatz Sanısı (3n+1)** ve kriptografik **S-Box** yapısını kullanarak güvenli ve dengeli (balanced) rastgele sayı dizileri üretir.

## 🚀 Özellikler

* **Matematiksel Kaos:** Collatz algoritması ile tahmin edilemez sayı üretimi.
* **S-Box Karıştırma:** Çıktıların lineerliğini bozan kriptografik katman.
* **Mükemmel Denge:** Çıktıda her zaman **eşit sayıda 0 ve 1** bulunur (%50 - %50).
* **Deterministik Yapı:** Aynı `seed` girildiğinde her zaman aynı şifreyi üretir (Analiz için uygundur).

## 🛠️ Kurulum ve Çalıştırma

Bilgisayarınızda Python yüklü olması yeterlidir.

1.  Repoyu klonlayın veya zip olarak indirin.
2.  Terminali açın ve dosyanın olduğu dizine gidin.
3.  Aşağıdaki komutu yazın:

```bash
python collatz_cipher.py
