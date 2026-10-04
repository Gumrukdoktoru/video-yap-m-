# Üretim hattı (HyperFrames öncesi)

HyperFrames kompozisyonunun kullandığı iki dosya burada üretildi:
`assets/video/plate_comp.mp4` ve `assets/audio/mix.wav`.

Bu klasörden çalıştırın (`cd pipeline`). Gerekenler: `pip install numpy opencv-python-headless pillow`, ayrıca `ffmpeg`.

1. **Slaytlar.** `python3 render_slides.py` komutu `slides/*.png` dosyalarını üretir: 1650x1000 boyutunda, PowerPoint görünümlü, Carlito Bold yazı tipiyle. Metinleri değiştirmek için `slide(...)` satırlarını düzenleyin.
2. **Perde takibi ve kompozit.** `python3 composite.py <sinif_plaka.mp4> ../assets/video/plate_comp.mp4 36.4` komutunu çalıştırın. Sınıf çekimi Runway ile üretildi: nano-banana-pro ile bir kare, ardından seedance-2 ile 10 saniyelik görüntüden videoya dönüşüm. Betik her karede yeşil perdeyi bulur ve dört kenara ayrı ayrı doğru oturtarak köşeleri hesaplar. Ardından slaytı perspektifle yerleştirir; perdenin kendi ışık düşüşü korunur. 10 saniyelik çekim ileri-geri (ping-pong) oynatılarak uzatılır. Slayt geçiş zamanları `SCHED` içinde, seslendirmeye göre ayarlıdır (`vo_times.json`).
3. **Seslendirme.** `build_vo.py` ElevenLabs "Mahmut Hoca" take'ini satırlara böler, aradaki boşlukları kısaltır ve `atempo=1.15` uygular. Çıktı `vo_times.json` içindeki satır zamanlarıdır.
4. **AMİN korosu.** `build_chorus.py` üç sesin (Adilcan, Belma, Dusk) 12 "Amiiiin!" take'ini rastgele (sabit seed) gecikme, perde ve pan ile 24 katman hâlinde üst üste bindirir.
5. **Miks.** Seslendirme, koro, kahkaha, ortam sesi, whoosh, damga sesi ve kapanış müziği ffmpeg `amix` ile birleştirilir, ardından `loudnorm` ile -14 LUFS'a getirilir. Ses efektleri Runway ile üretildi.

Ham TTS take'leri ve ses efektleri depoya eklenmedi. Yeniden üretmek için ElevenLabs akışı: "Gümrük Sınavı Duası - Seslendirme".
