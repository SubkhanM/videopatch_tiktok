# Impor library yang dibutuhkan
import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import zipfile
import requests
import sys
from pathlib import Path
import re
import json
import time
from datetime import datetime

# Mengatur tema default untuk GUI menggunakan customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class URCXPatchApp:
    """
    Kelas utama untuk aplikasi URCXPatch dengan optimisasi performa tinggi.
    """
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("URCXPatch v1.3 - Advanced Optimized")
        self.app.geometry("700x650")
        self.app.resizable(False, False)
        
        self.selected_file = ctk.StringVar()
        self.ffmpeg_path = None
        self.ffprobe_path = None
        self.video_duration = 0
        self.video_fps = 0
        self.has_nvidia_gpu = False
        self.has_amd_gpu = False
        self.current_process = None
        self.processing_start_time = None
        
        self.setup_gui()
        self.check_ffmpeg_on_startup()
        self.check_gpu_support()
        
    def setup_gui(self):
        """Membangun antarmuka pengguna yang dioptimisasi."""
        # --- Judul Aplikasi ---
        title = ctk.CTkLabel(self.app, text="URCXPatch v1.3 — Advanced TikTok FPS Booster", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # --- Frame untuk Pemilihan File ---
        file_frame = ctk.CTkFrame(self.app)
        file_frame.pack(pady=10, padx=20, fill="x")
        
        browse_btn = ctk.CTkButton(file_frame, text="📁 Pilih Video", command=self.browse_file, height=35)
        browse_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.path_label = ctk.CTkEntry(file_frame, textvariable=self.selected_file, width=400, state="readonly")
        self.path_label.grid(row=0, column=1, padx=10, pady=10)
        
        # --- Frame untuk Info Video ---
        info_frame = ctk.CTkFrame(self.app)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        info_title = ctk.CTkLabel(info_frame, text="📊 Video Information", font=ctk.CTkFont(size=14, weight="bold"))
        info_title.grid(row=0, column=0, columnspan=4, pady=(10, 5))
        
        # Row 1: FPS dan Duration
        fps_label = ctk.CTkLabel(info_frame, text="Current FPS:")
        fps_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.original_fps_entry = ctk.CTkEntry(info_frame, width=80, justify="center")
        self.original_fps_entry.insert(0, "N/A")
        self.original_fps_entry.configure(state="disabled")
        self.original_fps_entry.grid(row=1, column=1, padx=10, pady=5)
        
        duration_label = ctk.CTkLabel(info_frame, text="Duration:")
        duration_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        self.duration_entry = ctk.CTkEntry(info_frame, width=80, justify="center")
        self.duration_entry.insert(0, "N/A")
        self.duration_entry.configure(state="disabled")
        self.duration_entry.grid(row=1, column=3, padx=10, pady=5)
        
        # Row 2: GPU Status
        gpu_label = ctk.CTkLabel(info_frame, text="GPU Acceleration:")
        gpu_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.gpu_status = ctk.CTkLabel(info_frame, text="🔍 Checking...", font=ctk.CTkFont(size=11))
        self.gpu_status.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="w")
        
        # --- Frame untuk Opsi Kualitas ---
        quality_frame = ctk.CTkFrame(self.app)
        quality_frame.pack(pady=10, padx=20, fill="x")
        
        quality_label = ctk.CTkLabel(quality_frame, text="⚙️ Quality Settings", font=ctk.CTkFont(size=14, weight="bold"))
        quality_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        preset_label = ctk.CTkLabel(quality_frame, text="Encoding Preset:")
        preset_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.quality_var = ctk.StringVar(value="medium")
        quality_options = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower"]
        self.quality_menu = ctk.CTkOptionMenu(quality_frame, variable=self.quality_var, values=quality_options, width=150)
        self.quality_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # CRF Setting
        crf_label = ctk.CTkLabel(quality_frame, text="Quality (CRF):")
        crf_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.crf_var = ctk.StringVar(value="23")
        self.crf_entry = ctk.CTkEntry(quality_frame, textvariable=self.crf_var, width=50, justify="center")
        self.crf_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        crf_info = ctk.CTkLabel(quality_frame, text="(18-28: Lower = Better Quality, Higher Size)", 
                               font=ctk.CTkFont(size=10), text_color="gray")
        crf_info.grid(row=2, column=1, padx=(60, 10), pady=5, sticky="w")
        
        # --- Frame untuk Tombol Aksi ---
        button_frame = ctk.CTkFrame(self.app)
        button_frame.pack(pady=10, padx=20, fill="x")
        
        button_title = ctk.CTkLabel(button_frame, text="🎬 FPS Conversion Options", font=ctk.CTkFont(size=14, weight="bold"))
        button_title.pack(pady=(10, 5))
        
        self.patch_btn = ctk.CTkButton(button_frame, text="📈 Convert to 30 FPS (Fast)", 
                                       command=self.patch_to_30fps, height=40, 
                                       hover_color="#2D5A27")
        self.patch_btn.pack(pady=5, fill="x", padx=10)
        
        self.patch60_btn = ctk.CTkButton(button_frame, text="🚀 Convert to 60 FPS (Recommended)", 
                                         command=self.patch_to_60fps, height=40,
                                         hover_color="#1f4c96")
        self.patch60_btn.pack(pady=5, fill="x", padx=10)
        
        self.patch120_btn = ctk.CTkButton(button_frame, text="⚡ Convert to 120 FPS (Expert Mode)", 
                                          command=self.patch_to_120fps, height=40,
                                          hover_color="#8B4513")
        self.patch120_btn.pack(pady=5, fill="x", padx=10)
        
        # Cancel Button
        self.cancel_btn = ctk.CTkButton(button_frame, text="❌ Cancel Processing", 
                                       command=self.cancel_processing, height=35,
                                       fg_color="#cc0000", hover_color="#990000")
        self.cancel_btn.pack(pady=5, fill="x", padx=10)
        self.cancel_btn.pack_forget()
        
        # --- Enhanced Progress Section ---
        progress_frame = ctk.CTkFrame(self.app)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress_title = ctk.CTkLabel(progress_frame, text="📊 Processing Progress", 
                                          font=ctk.CTkFont(size=14, weight="bold"))
        self.progress_title.pack(pady=(10, 5))
        
        # Main Progress Bar
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=500, height=20)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)
        
        # Progress Labels
        progress_info_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_info_frame.pack(pady=5, fill="x")
        
        self.progress_label = ctk.CTkLabel(progress_info_frame, text="Ready to start", 
                                          font=ctk.CTkFont(size=12))
        self.progress_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(progress_info_frame, text="", 
                                      font=ctk.CTkFont(size=12))
        self.time_label.pack(side="right", padx=10)
        
        # ETA and Speed Info
        self.eta_label = ctk.CTkLabel(progress_frame, text="", 
                                     font=ctk.CTkFont(size=10), text_color="gray")
        self.eta_label.pack(pady=2)
        
        progress_frame.pack_forget()  # Sembunyikan pada awalnya
        self.progress_frame = progress_frame
        
        # --- Status dan Footer ---
        self.status_label = ctk.CTkLabel(self.app, text="🟢 Ready", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)
        
        # --- Frame untuk Status FFmpeg ---
        ffmpeg_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        ffmpeg_frame.pack(pady=10, side="bottom", fill="x", padx=20)
        
        self.ffmpeg_status = ctk.CTkLabel(ffmpeg_frame, text="🔍 Checking FFmpeg...", 
                                          font=ctk.CTkFont(size=12))
        self.ffmpeg_status.pack(pady=5)
        
        self.install_ffmpeg_btn = ctk.CTkButton(ffmpeg_frame, text="📥 Install FFmpeg", 
                                                command=self.install_ffmpeg, height=35)
        self.install_ffmpeg_btn.pack(pady=5)
        self.install_ffmpeg_btn.pack_forget()
        
        footer = ctk.CTkLabel(self.app, text="Made for TikTok Creators | URCXService 2025 - Advanced Edition", 
                              font=ctk.CTkFont(size=10))
        footer.pack(side="bottom", pady=10)
    
    def check_gpu_support(self):
        """Memeriksa dukungan GPU untuk hardware acceleration."""
        def check_gpu_async():
            try:
                if self.ffmpeg_path:
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    
                    # Check available encoders
                    result = subprocess.run([self.ffmpeg_path, '-hide_banner', '-encoders'], 
                                          capture_output=True, text=True, startupinfo=startupinfo)
                    
                    gpu_info = []
                    if 'h264_nvenc' in result.stdout:
                        self.has_nvidia_gpu = True
                        gpu_info.append("NVIDIA")
                    
                    if 'h264_amf' in result.stdout:
                        self.has_amd_gpu = True
                        gpu_info.append("AMD")
                    
                    if 'h264_qsv' in result.stdout:
                        gpu_info.append("Intel QSV")
                    
                    # Update GUI
                    if gpu_info:
                        gpu_text = f"✅ {'/'.join(gpu_info)} GPU Acceleration"
                        self.app.after(0, lambda: self.gpu_status.configure(text=gpu_text, text_color="lightgreen"))
                    else:
                        self.app.after(0, lambda: self.gpu_status.configure(text="⚠️ CPU Only (Slower)", text_color="orange"))
                        
            except Exception as e:
                print(f"Error checking GPU: {e}")
                self.app.after(0, lambda: self.gpu_status.configure(text="❓ Unknown", text_color="gray"))
        
        if self.ffmpeg_path:
            thread = threading.Thread(target=check_gpu_async)
            thread.daemon = True
            thread.start()
    
    def check_ffmpeg_on_startup(self):
        """Memeriksa ketersediaan FFmpeg saat aplikasi dimulai."""
        if self.check_ffmpeg():
            self.ffmpeg_status.configure(text="✅ FFmpeg Ready", text_color="lightgreen")
            self.enable_buttons()
        else:
            self.ffmpeg_status.configure(text="❌ FFmpeg Not Found - Install Required", text_color="#FF6666")
            self.install_ffmpeg_btn.pack(pady=5)
            self.disable_buttons()
    
    def check_ffmpeg(self):
        """Mengecek apakah FFmpeg ada di sistem."""
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Check system FFmpeg
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, startupinfo=startupinfo)
            self.ffmpeg_path = "ffmpeg"
            self.ffprobe_path = "ffprobe"
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Check local FFmpeg
            local_ffmpeg = Path("ffmpeg/bin/ffmpeg.exe")
            local_ffprobe = Path("ffmpeg/bin/ffprobe.exe")
            
            if local_ffmpeg.exists() and local_ffprobe.exists():
                self.ffmpeg_path = str(local_ffmpeg.absolute())
                self.ffprobe_path = str(local_ffprobe.absolute())
                return True
            return False
    
    def install_ffmpeg(self):
        """Mengunduh dan menginstal FFmpeg ke folder lokal."""
        def download_and_install():
            try:
                self.app.after(0, lambda: self.install_ffmpeg_btn.configure(text="⏳ Downloading...", state="disabled"))
                self.app.after(0, lambda: self.status_label.configure(text="📥 Downloading FFmpeg... Please wait"))
                
                url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
                
                # Download dengan progress
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                
                if response.status_code == 200:
                    downloaded = 0
                    with open("ffmpeg_temp.zip", "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    progress = downloaded / total_size
                                    self.app.after(0, lambda p=progress: self.status_label.configure(
                                        text=f"📥 Downloading FFmpeg... {int(p*100)}%"))
                    
                    self.app.after(0, lambda: self.status_label.configure(text="📦 Extracting FFmpeg..."))
                    
                    with zipfile.ZipFile("ffmpeg_temp.zip", 'r') as zip_ref:
                        zip_ref.extractall(".")
                    
                    # Rename folder
                    for item in os.listdir("."):
                        if item.startswith("ffmpeg-master-latest-win64-gpl"):
                            if os.path.exists("ffmpeg"):
                                import shutil
                                shutil.rmtree("ffmpeg")
                            os.rename(item, "ffmpeg")
                            break
                    
                    os.remove("ffmpeg_temp.zip")
                    
                    self.app.after(0, lambda: self.ffmpeg_status.configure(text="✅ FFmpeg Installed Successfully", text_color="lightgreen"))
                    self.app.after(0, lambda: self.install_ffmpeg_btn.pack_forget())
                    self.app.after(0, lambda: self.status_label.configure(text="🎉 FFmpeg installed successfully!"))
                    self.app.after(0, self.check_ffmpeg_on_startup)
                    self.app.after(0, self.check_gpu_support)
                else:
                    self.app.after(0, lambda: messagebox.showerror("Error", f"Failed to download FFmpeg. Status Code: {response.status_code}"))
            except Exception as e:
                self.app.after(0, lambda msg=f"Failed to install FFmpeg: {str(e)}": messagebox.showerror("Error", msg))
            finally:
                self.app.after(0, lambda: self.install_ffmpeg_btn.configure(text="📥 Install FFmpeg", state="normal"))

        if messagebox.askyesno("Install FFmpeg", 
                              "FFmpeg is required for video processing.\n\n"
                              "📦 Size: ~100MB\n"
                              "📁 Location: Local folder\n"
                              "🔒 Safe: Official build from GitHub\n\n"
                              "Continue installation?"):
            thread = threading.Thread(target=download_and_install)
            thread.daemon = True
            thread.start()
    
    def enable_buttons(self):
        """Mengaktifkan semua tombol patch."""
        self.patch_btn.configure(state="normal")
        self.patch60_btn.configure(state="normal")
        self.patch120_btn.configure(state="normal")
        
    def disable_buttons(self):
        """Menonaktifkan semua tombol patch."""
        self.patch_btn.configure(state="disabled")
        self.patch60_btn.configure(state="disabled")
        self.patch120_btn.configure(state="disabled")
    
    def browse_file(self):
        """Memilih file video."""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.mov *.avi *.mkv *.webm *.flv *.m4v *.wmv"),
                ("MP4 Files", "*.mp4"),
                ("MOV Files", "*.mov"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.selected_file.set(file_path)
            self.analyze_video(file_path)
    
    def analyze_video(self, file_path):
        """Menganalisis video secara lengkap."""
        try:
            if not self.ffprobe_path:
                self.ffprobe_path = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
            
            cmd = [
                self.ffprobe_path, '-v', 'quiet', '-print_format', 'json',
                '-show_streams', '-show_format', '-select_streams', 'v:0', file_path
            ]
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            result = subprocess.run(cmd, capture_output=True, text=True, startupinfo=startupinfo)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # Get video stream info
                video_stream = None
                for stream in data['streams']:
                    if stream['codec_type'] == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    # Extract FPS
                    fps = self.extract_fps(video_stream)
                    if fps:
                        self.video_fps = fps
                        self.original_fps_entry.configure(state="normal")
                        self.original_fps_entry.delete(0, "end")
                        self.original_fps_entry.insert(0, f"{fps:.2f}")
                        self.original_fps_entry.configure(state="disabled")
                    
                    # Extract duration
                    duration = 0
                    if 'duration' in video_stream:
                        duration = float(video_stream['duration'])
                    elif 'duration' in data['format']:
                        duration = float(data['format']['duration'])
                    
                    if duration > 0:
                        self.video_duration = duration
                        duration_str = self.format_duration(duration)
                        self.duration_entry.configure(state="normal")
                        self.duration_entry.delete(0, "end")
                        self.duration_entry.insert(0, duration_str)
                        self.duration_entry.configure(state="disabled")
                    
                    # Update status
                    self.status_label.configure(text=f"📹 Video loaded: {fps:.1f}fps, {duration_str}")
                    return
            
            raise ValueError("Could not analyze video")
            
        except Exception as e:
            print(f"Error analyzing video: {e}")
            self.original_fps_entry.configure(state="normal")
            self.original_fps_entry.delete(0, "end")
            self.original_fps_entry.insert(0, "Error")
            self.original_fps_entry.configure(state="disabled")
            
            self.status_label.configure(text="⚠️ Could not analyze video")
    
    def extract_fps(self, stream):
        """Ekstrak FPS dari stream video."""
        try:
            # Try r_frame_rate first
            if 'r_frame_rate' in stream and stream['r_frame_rate'] != '0/0':
                fps_str = stream['r_frame_rate']
                if '/' in fps_str:
                    num, den = map(int, fps_str.split('/'))
                    return num / den if den != 0 else 0
                else:
                    return float(fps_str)
            
            # Try avg_frame_rate
            if 'avg_frame_rate' in stream and stream['avg_frame_rate'] != '0/0':
                fps_str = stream['avg_frame_rate']
                if '/' in fps_str:
                    num, den = map(int, fps_str.split('/'))
                    return num / den if den != 0 else 0
                else:
                    return float(fps_str)
            
            return 0
        except:
            return 0
    
    def format_duration(self, seconds):
        """Format durasi ke format yang mudah dibaca."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def update_status(self, message, is_processing=False):
        """Memperbarui status aplikasi."""
        self.status_label.configure(text=message)
        
        if is_processing:
            self.disable_buttons()
            self.progress_frame.pack(pady=10, padx=20, fill="x")
            self.cancel_btn.pack(pady=5, fill="x", padx=10)
            self.processing_start_time = time.time()
        else:
            self.enable_buttons()
            self.progress_frame.pack_forget()
            self.cancel_btn.pack_forget()
            self.progress_bar.set(0)
            self.current_process = None

    def update_progress(self, value, current_time=None, speed=None):
        """Memperbarui progress bar dengan informasi detail."""
        self.progress_bar.set(value)
        
        # Update progress percentage
        percentage = int(value * 100)
        self.progress_label.configure(text=f"Processing... {percentage}%")
        
        # Update time info
        if self.processing_start_time:
            elapsed = time.time() - self.processing_start_time
            elapsed_str = self.format_duration(elapsed)
            
            if value > 0.01:  # Avoid division by zero
                estimated_total = elapsed / value
                remaining = estimated_total - elapsed
                eta_str = self.format_duration(remaining)
                
                self.time_label.configure(text=f"Elapsed: {elapsed_str}")
                self.eta_label.configure(text=f"ETA: {eta_str} | Speed: {speed or 'N/A'}")
            else:
                self.time_label.configure(text=f"Elapsed: {elapsed_str}")

    def cancel_processing(self):
        """Membatalkan proses yang sedang berjalan."""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process = None
                self.update_status("❌ Processing cancelled", False)
                messagebox.showinfo("Cancelled", "Processing has been cancelled.")
            except:
                pass

    def build_ffmpeg_command(self, input_file, output_file, target_fps, method="fast"):
        """Membangun command FFmpeg yang dioptimisasi."""
        base_cmd = [self.ffmpeg_path, '-y']
        
        # Hardware acceleration (sebelum input)
        if self.has_nvidia_gpu:
            base_cmd.extend(['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda'])
        elif self.has_amd_gpu:
            base_cmd.extend(['-hwaccel', 'dxva2'])
        
        # Input file
        base_cmd.extend(['-i', input_file])
        
        # Video filter berdasarkan method
        if method == "fast":
            # Simple fps filter - paling cepat
            video_filter = f'fps={target_fps}'
        elif method == "interpolate":
            # Motion interpolation dengan blend
            video_filter = f'minterpolate=fps={target_fps}:mi_mode=blend'
        else:  # method == "advanced"
            # Advanced motion interpolation
            video_filter = f'minterpolate=fps={target_fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1'
        
        base_cmd.extend(['-filter:v', video_filter])
        
        # Encoder selection
        try:
            crf_value = int(self.crf_var.get())
            crf_value = max(15, min(30, crf_value))  # Clamp between 15-30
        except:
            crf_value = 23
        
        if self.has_nvidia_gpu:
            base_cmd.extend(['-c:v', 'h264_nvenc'])
            base_cmd.extend(['-preset', 'medium'])
            base_cmd.extend(['-cq', str(crf_value)])
            base_cmd.extend(['-profile:v', 'high'])
        else:
            base_cmd.extend(['-c:v', 'libx264'])
            base_cmd.extend(['-preset', self.quality_var.get()])
            base_cmd.extend(['-crf', str(crf_value)])
            base_cmd.extend(['-profile:v', 'high'])
        
        # Audio handling
        base_cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
        
        # Additional optimizations
        base_cmd.extend(['-movflags', '+faststart'])  # For web streaming
        base_cmd.extend(['-pix_fmt', 'yuv420p'])     # Compatibility
        
        # Output file
        base_cmd.append(output_file)
        
        return base_cmd

    def process_video(self, input_file, output_file, command, fps_type):
        """Memproses video dengan monitoring progress yang akurat."""
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Start FFmpeg process
            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='ignore',
                startupinfo=startupinfo
            )
            
            # Progress monitoring patterns
            time_pattern = re.compile(r'time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})')
            speed_pattern = re.compile(r'speed=\s*(\d+\.?\d*)x')
            
            last_update = time.time()
            
            for line in self.current_process.stdout:
                if self.current_process.poll() is not None:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Extract time progress
                time_match = time_pattern.search(line)
                if time_match and self.video_duration > 0:
                    hours = int(time_match.group(1))
                    minutes = int(time_match.group(2))
                    seconds = int(time_match.group(3))
                    
                    current_time = hours * 3600 + minutes * 60 + seconds
                    progress = min(current_time / self.video_duration, 1.0)
                    
                    # Extract speed
                    speed_match = speed_pattern.search(line)
                    speed_text = f"{speed_match.group(1)}x" if speed_match else "N/A"
                    
                    # Update UI (throttled to avoid too frequent updates)
                    now = time.time()
                    if now - last_update > 0.5:  # Update every 0.5 seconds
                        self.app.after(0, lambda p=progress, s=speed_text: self.update_progress(p, current_time, s))
                        last_update = now
            
            # Wait for process to complete
            self.current_process.wait()
            
            if self.current_process.returncode == 0:
                # Success
                self.app.after(0, lambda: self.update_progress(1.0))
                self.app.after(0, lambda: self.update_status("✅ Conversion completed successfully!", False))
                
                # Show success message with file info
                file_size = os.path.getsize(output_file) / (1024*1024)  # MB
                success_msg = (f"🎉 Video successfully converted to {fps_type} FPS!\n\n"
                              f"📁 Output: {os.path.basename(output_file)}\n"
                              f"📊 Size: {file_size:.1f} MB\n"
                              f"📂 Location: {os.path.dirname(output_file)}")
                
                self.app.after(0, lambda: messagebox.showinfo("Success", success_msg))
                
                # Ask if user wants to open output folder
                if messagebox.askyesno("Open Folder", "Would you like to open the output folder?"):
                    os.startfile(os.path.dirname(output_file))
                    
            else:
                # Error
                self.app.after(0, lambda: self.update_status("❌ Conversion failed", False))
                self.app.after(0, lambda: messagebox.showerror("Error", 
                    "Conversion failed. Please check:\n"
                    "• Video file is not corrupted\n"
                    "• Sufficient disk space\n"
                    "• Try different quality settings"))
                
        except Exception as e:
            self.app.after(0, lambda: self.update_status("❌ An error occurred", False))
            self.app.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            self.current_process = None

    def start_processing(self, target_fps, method="fast"):
        """Memulai proses konversi video."""
        input_file = self.selected_file.get()
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid video file first.")
            return
        
        if not self.ffmpeg_path:
            messagebox.showerror("Error", "FFmpeg is not available. Please install it first.")
            return
        
        # Validate CRF value
        try:
            crf_value = int(self.crf_var.get())
            if crf_value < 15 or crf_value > 30:
                messagebox.showerror("Error", "CRF value must be between 15-30")
                return
        except ValueError:
            messagebox.showerror("Error", "CRF value must be a number")
            return
        
        # Check current FPS
        current_fps_text = self.original_fps_entry.get()
        if current_fps_text != "N/A" and current_fps_text != "Error":
            try:
                current_fps = float(current_fps_text)
                if current_fps == target_fps:
                    if not messagebox.askyesno("Same FPS", 
                        f"Video already has {target_fps} FPS. Continue anyway?\n\n"
                        "This will re-encode the video with your quality settings."):
                        return
                elif current_fps > target_fps:
                    # Downsampling - use fast method
                    method = "fast"
                    messagebox.showinfo("Info", 
                        f"Video will be downsampled from {current_fps:.1f} FPS to {target_fps} FPS.\n"
                        "Using fast method for optimal quality.")
                else:
                    # Upsampling - confirm method
                    if method == "advanced" and not messagebox.askyesno("Slow Process Warning",
                        f"Converting from {current_fps:.1f} to {target_fps} FPS with advanced interpolation.\n\n"
                        "⚠️ This will be VERY SLOW and resource intensive!\n"
                        "💡 Consider using 60 FPS option instead.\n\n"
                        "Continue with advanced interpolation?"):
                        return
            except ValueError:
                pass
        
        # Check available disk space
        free_space = self.get_free_space(os.path.dirname(input_file))
        input_size = os.path.getsize(input_file) / (1024*1024)  # MB
        
        if free_space < input_size * 2:  # Need at least 2x input size
            if not messagebox.askyesno("Low Disk Space", 
                f"Warning: Low disk space detected.\n\n"
                f"Available: {free_space:.1f} MB\n"
                f"Recommended: {input_size*2:.1f} MB\n\n"
                "Continue anyway?"):
                return
        
        # Generate output filename
        base_name = os.path.splitext(input_file)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{base_name}_{target_fps}fps_{timestamp}.mp4"
        
        # Ensure output file doesn't exist
        counter = 1
        while os.path.exists(output_file):
            output_file = f"{base_name}_{target_fps}fps_{timestamp}_{counter}.mp4"
            counter += 1
        
        # Build command
        command = self.build_ffmpeg_command(input_file, output_file, target_fps, method)
        
        # Debug: log command
        print("FFmpeg command:", ' '.join(command))
        
        # Show processing info
        method_names = {
            "fast": "Fast (Simple FPS conversion)",
            "interpolate": "Interpolation (Motion blend)",
            "advanced": "Advanced (Motion estimation)"
        }
        
        processing_info = (f"🎬 Starting conversion:\n\n"
                          f"📄 Input: {os.path.basename(input_file)}\n"
                          f"🎯 Target FPS: {target_fps}\n"
                          f"⚙️ Method: {method_names.get(method, method)}\n"
                          f"🎛️ Quality: {self.quality_var.get()} (CRF {self.crf_var.get()})\n"
                          f"🔧 Encoder: {'NVIDIA GPU' if self.has_nvidia_gpu else 'CPU'}")
        
        self.update_status(processing_info, True)
        
        # Start processing in thread
        thread = threading.Thread(
            target=self.process_video,
            args=(input_file, output_file, command, target_fps),
            daemon=True
        )
        thread.start()
    
    def get_free_space(self, path):
        """Mendapatkan ruang disk yang tersedia dalam MB."""
        try:
            import shutil
            total, used, free = shutil.disk_usage(path)
            return free / (1024*1024)  # Convert to MB
        except:
            return float('inf')  # Assume unlimited if can't check

    def patch_to_30fps(self):
        """Konversi ke 30 FPS dengan metode cepat."""
        self.start_processing(30, "fast")
    
    def patch_to_60fps(self):
        """Konversi ke 60 FPS dengan metode interpolasi."""
        self.start_processing(60, "interpolate")
    
    def patch_to_120fps(self):
        """Konversi ke 120 FPS dengan peringatan."""
        warning_msg = (
            "⚠️ 120 FPS Conversion Warning ⚠️\n\n"
            "This process is EXTREMELY resource intensive:\n\n"
            "⏱️ Time: 10-30x longer than video duration\n"
            "🧠 RAM: High memory usage (4GB+ recommended)\n"
            "💾 Storage: 3-5x larger output file\n"
            "🔥 CPU/GPU: Will run at high load\n\n"
            "📱 TikTok typically caps at 60 FPS anyway.\n\n"
            "💡 Recommended for videos under 1 minute only.\n\n"
            "Continue with 120 FPS conversion?"
        )
        
        if not messagebox.askyesno("120 FPS Warning", warning_msg):
            return
        
        self.start_processing(120, "advanced")
    
    def run(self):
        """Menjalankan aplikasi."""
        try:
            self.app.mainloop()
        except KeyboardInterrupt:
            if self.current_process:
                self.current_process.terminate()
            self.app.quit()

# Error handling untuk dependency
def check_dependencies():
    """Memeriksa dependency yang diperlukan."""
    missing_deps = []
    
    try:
        import customtkinter
    except ImportError:
        missing_deps.append("customtkinter")
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    if missing_deps:
        print("Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nInstall with: pip install " + " ".join(missing_deps))
        return False
    
    return True

if __name__ == "__main__":
    if not check_dependencies():
        input("Press Enter to exit...")
        sys.exit(1)
    
    try:
        app = URCXPatchApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)