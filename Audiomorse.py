import tkinter as tk
from tkinter import ttk,messagebox, filedialog
import wave
import pyaudio
from pydub import AudioSegment
import threading
import time
from MorseTranslator import MorseTranslator
import os

class MorseGUIAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Translator")
        self.root.geometry("400x300")

        self.setup_gui()
        self.p = pyaudio.PyAudio()
        self.tmp_wav_file = "temp.wav"

    def setup_gui(self):
        self.text_frame = ttk.LabelFrame(self.root, text="Text to Morse")
        self.text_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.text_label = ttk.Label(self.text_frame, text="Enter Text:")
        self.text_label.grid(row=0, column=0, padx=10, pady=5)

        self.text_entry = ttk.Entry(self.text_frame, width=40)
        self.text_entry.grid(row=0, column=1, padx=10, pady=5)

        self.morse_label = ttk.Label(self.text_frame, text="Morse Code:")
        self.morse_label.grid(row=1, column=0, padx=10, pady=5)

        self.morse_entry = ttk.Entry(self.text_frame, width=40)
        self.morse_entry.grid(row=1, column=1, padx=10, pady=5)

        self.translate_button = ttk.Button(self.text_frame, text="Translate", command=self.translate_text)
        self.translate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.listen_frame = ttk.LabelFrame(self.root, text="Listen")
        self.listen_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.listen_realtime_button = ttk.Button(self.listen_frame, text="Listen Real-time",
                                                 command=self.listen_realtime)
        self.listen_realtime_button.grid(row=0, column=0, padx=10, pady=5)

        self.file_entry = ttk.Entry(self.listen_frame, width=30)
        self.file_entry.grid(row=0, column=1, padx=10, pady=5)

        self.browse_button = ttk.Button(self.listen_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        self.listen_file_button = ttk.Button(self.listen_frame, text="Listen File", command=self.listen_file)
        self.listen_file_button.grid(row=1, column=0, columnspan=3, pady=10)

    def translate_text(self):
        text = self.text_entry.get()
        morse = self.morse_entry.get()

        translator = MorseTranslator()

        if text:
            morse_translation = translator.text_to_morse(text)
            self.morse_entry.delete(0, tk.END)
            self.morse_entry.insert(tk.END, morse_translation)
        elif morse:
            text_translation = translator.morse_to_text(morse)
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(tk.END, text_translation)
        else:
            messagebox.showinfo("Error", "Please enter either text or Morse code!")


    def listen_realtime(self):
        t = threading.Thread(target=self.listen_audio_realtime)
        t.start()

    def listen_file(self):
        file_path = self.file_entry.get()

        if not file_path:
            messagebox.showinfo("Error", "Please enter a file path.")
            return

        # Start a new thread to listen to the selected audio file
        t = threading.Thread(target=self.listen_audio_file, args=(file_path,))
        t.start()

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("Audio files", "*.mp3 *.wav")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(tk.END, file_path)

    def listen_audio_realtime(self):
        try:
            stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            morse_code = ""
            listening = True
            while listening:
                data = stream.read(1024)
                if any(abs(x) > 1500 for x in data):
                    morse_code += "."
                else:
                    morse_code += "-"
                time.sleep(0.05)  # Adjust this value to control the Morse code speed
        except Exception as e:
            print(e)
        finally:
            stream.stop_stream()
            stream.close()
            self.p.terminate()
            decoded_text = MorseTranslator.morse_to_text(morse_code)
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(tk.END, decoded_text)

    def listen_audio_file(self, file_path):
        try:
            if file_path.endswith(".mp3"):
                audio = AudioSegment.from_mp3(file_path)
                audio.export(self.tmp_wav_file, format="wav")
                file_path = self.tmp_wav_file

            wf = wave.open(file_path, 'rb')
            data = wf.readframes(1024)
            morse_code = ""
            while data:
                if any(abs(x) > 1000 for x in data):
                    morse_code += "."
                else:
                    morse_code += " "
                data = wf.readframes(1024)
        except Exception as e:
            print(e)
        finally:
            wf.close()
            if file_path == self.tmp_wav_file and os.path.exists(self.tmp_wav_file):
                os.remove(self.tmp_wav_file)
            decoded_text = MorseTranslator.morse_to_text(morse_code)
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(tk.END, decoded_text)

if __name__=="__main__":
    root = tk.Tk()
    app = MorseGUIAudio(root)
    root.mainloop()

