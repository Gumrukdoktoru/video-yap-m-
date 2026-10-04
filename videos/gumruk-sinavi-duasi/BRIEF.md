---
workflow: general-video
flow: automation
storyboard: no
message: "Gümrük sınavına dua yetmez — hazırlık Can'lı 7/24 Eğitim Merkezi'nden"
destination: instagram-reels
aspect: 1080x1920
language: tr
audience: Gümrük Müşavirliği / Müşavir Yardımcılığı sınavına hazırlanan adaylar
length: 40.6s
angle: meme-parody
---

## Intent

"Kimsenin bilmediği KPSS DUASI" sınıf meme'inin gümrük sınavlarına uyarlaması,
Can'lı 7/24 Eğitim Merkezi için. Komik bir video olacak: projeksiyon perdesinde
PowerPoint slaytları, ciddi bir hoca sesi duayı okuyor, sınıf hep bir ağızdan
"AMİN" diyor, ardından kahkaha ve markalı kapanış kartı geliyor.

## Assets

- src: kullanıcının yüklediği orijinal video (KPSS Duası, 720x1280, 25.7s). Sadece yapı ve tempo için referans, görüntüsü kullanılmadı.
- assets/video/plate_comp.mp4: yapay zekâyla üretilmiş sınıf çekimi (Runway: nano-banana-pro still + seedance-2 image-to-video). Gümrük slaytları perdeye OpenCV ile perspektif takibi yapılarak yerleştirildi.
- assets/audio/mix.wav: ElevenLabs "Mahmut Hoca" seslendirmesi (en iyi take) + 24 katmanlı "Amin" korosu (Adilcan / Belma / Dusk sesleri) + Runway kahkaha, whoosh ve damga efektleri + sentezlenmiş sınıf ortam sesi. -14 LUFS.

## Customizations

- Görüntü: yapay zekâyla yeni sınıf çekimi (kullanıcının seçimi; orijinal çekim kullanılmadı).
- Ses: yapay zekâ sesi ve AMİN korosu (kullanıcının seçimi).
- Kapanış: sadece isim ve slogan ("Dua sizden, hazırlık bizden."). Telefon, adres veya iddia uydurulmadı.
- Slayt metinleri onaylanan taslaktaki gibi (GTİP, FOB/CIF, kırmızı/yeşil hat, mevzuat, kambiyo, "Diğerleri").

## Notes

- Logo ve iletişim bilgisi gelince kapanış kartına eklenecek.
