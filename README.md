# URCXPatch v1.3 — Advanced TikTok FPS Booster

**URCXPatch** adalah aplikasi desktop GUI berbasis Python untuk mengubah **frame rate (FPS)** video menjadi 30, 60, atau 120 FPS. Dirancang khusus untuk kreator TikTok agar bisa mengunggah video dengan kualitas tinggi (tanpa kompres berlebihan).
---

## ✨ Fitur Utama

- 🖥️ Antarmuka modern dengan `customtkinter`
- 🎬 Konversi ke 30/60/120 FPS
- 🚀 Deteksi & akselerasi GPU otomatis (NVIDIA, AMD, Intel QSV)
- 📊 Progress bar real-time saat proses konversi
- 📂 Analisis metadata video (FPS & durasi)
- ⚙️ Instalasi otomatis FFmpeg jika belum ada

---

## 🛠️ Teknologi

- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [ffmpeg](https://ffmpeg.org/)
- threading, subprocess, requests, json, os

---

## 📥 Cara Instal & Jalankan

### 1. Clone repository

```bash
git clone https://github.com/NAMA_KAMU/urcxpatch.git
cd urcxpatch
```

### 2. Install dependencies Python

```bash
pip install customtkinter requests
```

### 3. Jalankan aplikasi

```bash
python urcxpatch.py
```

> Jika `ffmpeg` belum tersedia, aplikasi akan otomatis mengunduh versi terbaru dari GitHub.

---

## ⚠️ Catatan Penting untuk 120 FPS

Mengubah ke 120 FPS akan:
- Membutuhkan waktu lebih lama
- Menggunakan RAM dan CPU/GPU lebih tinggi
- Membuat file output jauh lebih besar

Tidak direkomendasikan untuk video berdurasi panjang (di atas 1 menit), kecuali menggunakan GPU.

---

## 📸 Tampilan Aplikasi

![Preview GUI](https://dummyimage.com/800x500/1a1a1a/ffffff&text=URCXPatch+GUI+Preview)

---

## 📋 Rencana Pengembangan (TODO)

- [x] GUI dark mode
- [x] Analisa & konversi video otomatis
- [x] Deteksi GPU otomatis (NVENC/AMF/QSV)
- [x] Instalasi otomatis FFmpeg
- [ ] Fitur drag-and-drop file
- [ ] Pilihan resolusi (720p, 1080p, 4K)
- [ ] Multi-video batch processing
- [ ] Preset TikTok, Reels, YouTube Shorts

---

## 🤝 Kontribusi

Pull request dan issue sangat diterima!  
Silakan fork, buat perubahan, dan ajukan PR.  
Bisa bantu dengan fitur, bugfix, UI, atau dokumentasi.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

## 📬 Kontak
