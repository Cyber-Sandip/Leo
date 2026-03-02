import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
from PIL import Image, ImageTk
import cv2
import threading
import psutil
import pyaudio
import numpy as np

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("1400x750")
        self.root.configure(bg='#1e1e2e')
        
        # Variables
        self.chat_history = []
        self.cap = None
        self.gif_frames = []
        self.current_frame = 0
        self.is_running = True
        self.audio_stream = None
        self.audio = None
        
        # Create main container
        main_container = tk.Frame(root, bg='#1e1e2e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel - Chat History
        self.create_left_panel(main_container)
        
        # Middle Panel - GIF Animation & Volume Meter
        self.create_middle_panel(main_container)
        
        # Right Panel - Camera and DateTime and Task Manager
        self.create_right_panel(main_container)
        
        # Start updates
        self.update_datetime()
        self.update_camera()
        self.animate_gif()
        self.update_system_stats()
        self.update_volume_meter()
        
    def create_left_panel(self, parent):
        left_frame = tk.Frame(parent, bg='#2d2d3d', width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        # Title
        title = tk.Label(left_frame, text="Chat History", 
                        font=('Arial', 16, 'bold'), 
                        bg='#2d2d3d', fg='#ffffff')
        title.pack(pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            left_frame, 
            wrap=tk.WORD, 
            font=('Arial', 10),
            bg='#1e1e2e', 
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = tk.Frame(left_frame, bg='#2d2d3d')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_box = tk.Entry(input_frame, font=('Arial', 11),
                                  bg='#1e1e2e', fg='#ffffff',
                                  insertbackground='#ffffff', relief=tk.FLAT)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.input_box.bind('<Return>', self.add_message)
        
        send_btn = tk.Button(input_frame, text="Send", command=self.add_message,
                           bg='#5865f2', fg='#ffffff', font=('Arial', 10, 'bold'),
                           relief=tk.FLAT, padx=15, cursor='hand2')
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
    def create_middle_panel(self, parent):
        middle_frame = tk.Frame(parent, bg='#2d2d3d')
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Status label
        status_label = tk.Label(middle_frame, text="Voice Assistant Active", 
                               font=('Arial', 14, 'bold'), 
                               bg='#2d2d3d', fg='#5865f2')
        status_label.pack(pady=15)
        
        # GIF display
        self.gif_label = tk.Label(middle_frame, bg='#2d2d3d')
        self.gif_label.pack(expand=True)
        
        # Load placeholder GIF
        self.create_placeholder_animation()
        
        # Volume Meter Section
        volume_frame = tk.Frame(middle_frame, bg='#1e1e2e', relief=tk.FLAT)
        volume_frame.pack(fill=tk.X, padx=20, pady=15)
        
        vol_title = tk.Label(volume_frame, text="🎤 Audio Input Level", 
                            font=('Arial', 11, 'bold'), 
                            bg='#1e1e2e', fg='#ffffff')
        vol_title.pack(pady=5)
        
        # Volume bar
        self.volume_canvas = tk.Canvas(volume_frame, height=30, bg='#2d2d3d', 
                                       highlightthickness=0)
        self.volume_canvas.pack(fill=tk.X, padx=10, pady=5)
        
        self.volume_text = tk.Label(volume_frame, text="Volume: 0%", 
                                    font=('Arial', 9), 
                                    bg='#1e1e2e', fg='#aaaaaa')
        self.volume_text.pack(pady=2)
        
        # Control buttons
        btn_frame = tk.Frame(middle_frame, bg='#2d2d3d')
        btn_frame.pack(pady=15)
        
        start_btn = tk.Button(btn_frame, text="🎤 Start Listening", 
                             bg='#3ba55d', fg='#ffffff', font=('Arial', 11, 'bold'),
                             relief=tk.FLAT, padx=20, pady=8, cursor='hand2',
                             command=self.start_listening)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(btn_frame, text="⏹ Stop", 
                            bg='#ed4245', fg='#ffffff', font=('Arial', 11, 'bold'),
                            relief=tk.FLAT, padx=20, pady=8, cursor='hand2',
                            command=self.stop_listening)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
    def create_right_panel(self, parent):
        right_frame = tk.Frame(parent, bg='#2d2d3d', width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        
        # DateTime display
        datetime_frame = tk.Frame(right_frame, bg='#1e1e2e', relief=tk.FLAT)
        datetime_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.time_label = tk.Label(datetime_frame, text="00:00:00", 
                                   font=('Arial', 24, 'bold'), 
                                   bg='#1e1e2e', fg='#5865f2')
        self.time_label.pack(pady=5)
        
        self.date_label = tk.Label(datetime_frame, text="Monday, Jan 01, 2024", 
                                   font=('Arial', 12), 
                                   bg='#1e1e2e', fg='#ffffff')
        self.date_label.pack(pady=5)
        
        # Task Manager Section
        task_frame = tk.Frame(right_frame, bg='#1e1e2e', relief=tk.FLAT)
        task_frame.pack(fill=tk.X, padx=10, pady=10)
        
        task_title = tk.Label(task_frame, text="⚙️ System Monitor", 
                             font=('Arial', 13, 'bold'), 
                             bg='#1e1e2e', fg='#ffffff')
        task_title.pack(pady=8)
        
        # CPU Usage
        cpu_frame = tk.Frame(task_frame, bg='#1e1e2e')
        cpu_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(cpu_frame, text="CPU:", font=('Arial', 10, 'bold'),
                bg='#1e1e2e', fg='#ffffff').pack(side=tk.LEFT)
        self.cpu_label = tk.Label(cpu_frame, text="0%", font=('Arial', 10),
                                 bg='#1e1e2e', fg='#5865f2')
        self.cpu_label.pack(side=tk.LEFT, padx=5)
        
        self.cpu_bar = ttk.Progressbar(cpu_frame, length=200, mode='determinate',
                                       style='Custom.Horizontal.TProgressbar')
        self.cpu_bar.pack(side=tk.LEFT, padx=5)
        
        # Memory Usage
        mem_frame = tk.Frame(task_frame, bg='#1e1e2e')
        mem_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(mem_frame, text="RAM:", font=('Arial', 10, 'bold'),
                bg='#1e1e2e', fg='#ffffff').pack(side=tk.LEFT)
        self.mem_label = tk.Label(mem_frame, text="0%", font=('Arial', 10),
                                 bg='#1e1e2e', fg='#3ba55d')
        self.mem_label.pack(side=tk.LEFT, padx=5)
        
        self.mem_bar = ttk.Progressbar(mem_frame, length=200, mode='determinate',
                                       style='Custom.Horizontal.TProgressbar')
        self.mem_bar.pack(side=tk.LEFT, padx=5)
        
        # Disk Usage
        disk_frame = tk.Frame(task_frame, bg='#1e1e2e')
        disk_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(disk_frame, text="Disk:", font=('Arial', 10, 'bold'),
                bg='#1e1e2e', fg='#ffffff').pack(side=tk.LEFT)
        self.disk_label = tk.Label(disk_frame, text="0%", font=('Arial', 10),
                                  bg='#1e1e2e', fg='#faa61a')
        self.disk_label.pack(side=tk.LEFT, padx=5)
        
        self.disk_bar = ttk.Progressbar(disk_frame, length=200, mode='determinate',
                                        style='Custom.Horizontal.TProgressbar')
        self.disk_bar.pack(side=tk.LEFT, padx=5)
        
        # Additional info
        self.info_label = tk.Label(task_frame, text="", font=('Arial', 8),
                                   bg='#1e1e2e', fg='#aaaaaa', justify=tk.LEFT)
        self.info_label.pack(pady=5)
        
        # Camera view
        camera_title = tk.Label(right_frame, text="📷 Camera View", 
                               font=('Arial', 13, 'bold'), 
                               bg='#2d2d3d', fg='#ffffff')
        camera_title.pack(pady=10)
        
        self.camera_label = tk.Label(right_frame, bg='#1e1e2e')
        self.camera_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Camera controls
        cam_btn_frame = tk.Frame(right_frame, bg='#2d2d3d')
        cam_btn_frame.pack(pady=10)
        
        self.cam_toggle_btn = tk.Button(cam_btn_frame, text="📷 Enable Camera", 
                                       bg='#5865f2', fg='#ffffff', 
                                       font=('Arial', 10, 'bold'),
                                       relief=tk.FLAT, padx=15, pady=5, 
                                       cursor='hand2',
                                       command=self.toggle_camera)
        self.cam_toggle_btn.pack()
        
        # Configure progressbar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.Horizontal.TProgressbar', 
                       background='#5865f2',
                       troughcolor='#2d2d3d',
                       borderwidth=0,
                       thickness=15)
        
    def create_placeholder_animation(self):
        # Create a simple animated circle as placeholder
        for i in range(20):
            img = Image.new('RGB', (300, 300), color='#2d2d3d')
            # Add your GIF loading code here: 
            # gif = Image.open('your_animation.gif')
            self.gif_frames.append(ImageTk.PhotoImage(img))
    
    def animate_gif(self):
        if self.is_running and self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.root.after(50, self.animate_gif)
    
    def update_datetime(self):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %b %d, %Y")
        
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        self.root.after(1000, self.update_datetime)
    
    def update_system_stats(self):
        if self.is_running:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_label.config(text=f"{cpu_percent}%")
            self.cpu_bar['value'] = cpu_percent
            
            # Memory Usage
            mem = psutil.virtual_memory()
            mem_percent = mem.percent
            self.mem_label.config(text=f"{mem_percent}%")
            self.mem_bar['value'] = mem_percent
            
            # Disk Usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            self.disk_label.config(text=f"{disk_percent}%")
            self.disk_bar['value'] = disk_percent
            
            # Additional info
            cpu_count = psutil.cpu_count()
            mem_total = mem.total / (1024**3)  # GB
            info_text = f"CPU Cores: {cpu_count} | RAM: {mem_total:.1f} GB"
            self.info_label.config(text=info_text)
            
            self.root.after(2000, self.update_system_stats)
    
    def update_volume_meter(self):
        if self.is_running:
            try:
                if self.audio_stream is None:
                    self.init_audio()
                
                if self.audio_stream:
                    data = self.audio_stream.read(1024, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    volume = np.abs(audio_data).mean()
                    
                    # Normalize volume (0-100)
                    volume_percent = min(100, (volume / 100) * 100)
                    
                    # Update canvas
                    canvas_width = self.volume_canvas.winfo_width()
                    if canvas_width > 1:
                        self.volume_canvas.delete('all')
                        bar_width = (canvas_width - 20) * (volume_percent / 100)
                        
                        # Color based on volume
                        if volume_percent < 30:
                            color = '#3ba55d'
                        elif volume_percent < 70:
                            color = '#faa61a'
                        else:
                            color = '#ed4245'
                        
                        self.volume_canvas.create_rectangle(10, 5, 10 + bar_width, 25,
                                                           fill=color, outline='')
                        self.volume_text.config(text=f"Volume: {int(volume_percent)}%")
            except Exception as e:
                pass
            
            self.root.after(50, self.update_volume_meter)
    
    def init_audio(self):
        try:
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
        except Exception as e:
            print(f"Audio initialization error: {e}")
    
    def update_camera(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (340, 220))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
        
        self.root.after(30, self.update_camera)
    
    def toggle_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cam_toggle_btn.config(text="📷 Disable Camera", bg='#ed4245')
        else:
            self.cap.release()
            self.cap = None
            self.camera_label.config(image='')
            self.cam_toggle_btn.config(text="📷 Enable Camera", bg='#5865f2')
    
    def add_message(self, event=None):
        message = self.input_box.get().strip()
        if message:
            timestamp = datetime.now().strftime("%H:%M")
            
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n", 'user')
            self.chat_display.insert(tk.END, f"[{timestamp}] Assistant: Processing...\n\n", 'assistant')
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            self.input_box.delete(0, tk.END)
            
            # Here you can add your voice assistant response logic
    
    def start_listening(self):
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] System: Listening...\n", 'system')
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        # Add your voice listening code here
    
    def stop_listening(self):
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] System: Stopped listening.\n\n", 'system')
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def cleanup(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.audio:
            self.audio.terminate()

def main():
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()