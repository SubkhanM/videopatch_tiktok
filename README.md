# URCXPatch v1.3 — Advanced TikTok FPS Booster

**URCXPatch** is a Python-based desktop GUI application to convert **video frame rates (FPS)** to 30, 60, or 120 FPS. Designed especially for TikTok creators who want to upload videos in high quality (without aggressive compression).

---

## ✨ Main Features

- 🖥️ Modern interface with `customtkinter`
- 🎬 Convert videos to 30/60/120 FPS
- 🚀 Automatic GPU acceleration detection (NVIDIA, AMD, Intel QSV)
- 📊 Real-time progress bar during conversion
- 📂 Video metadata analysis (FPS & duration)
- ⚙️ Auto-install FFmpeg if not available

---

## 🛠️ Technologies

- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [ffmpeg](https://ffmpeg.org/)
- threading, subprocess, requests, json, os

---

## 📥 How to Install & Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/urcxpatch.git
cd urcxpatch
```

### 2. Install Python dependencies

```bash
pip install customtkinter requests
```

### 3. Run the application

```bash
python project.py
```

> If `ffmpeg` is not found, the app will automatically download the latest version from GitHub.

---

## ⚠️ Warning for 120 FPS

Converting to 120 FPS:
- Takes much longer processing time
- Uses significantly more RAM and CPU/GPU
- Produces much larger output file sizes

Not recommended for long videos (over 1 minute) unless using GPU acceleration.

---

## 📸 App Interface Preview

![GUI Preview](https://dummyimage.com/800x500/1a1a1a/ffffff&text=URCXPatch+GUI+Preview)

---

## 📋 Development Roadmap (TODO)

- [x] Dark mode GUI
- [x] Auto video analysis & conversion
- [x] Auto GPU detection (NVENC/AMF/QSV)
- [x] Auto FFmpeg installation
- [ ] Drag-and-drop support
- [ ] Resolution options (720p, 1080p, 4K)
- [ ] Multi-video batch processing
- [ ] Presets for TikTok, Reels, YouTube Shorts

---

## 🤝 Contribution

Pull requests and issues are welcome!  
Feel free to fork the repo, make changes, and submit a PR.  
Help with new features, bugfixes, UI improvements, or docs is appreciated.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

**URCXPatch Team**  
📧 Email: -  
📱 TikTok: -
