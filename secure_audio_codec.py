import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib

SAMPLE_RATE = 44100
BIT_DURATION = 0.3

def generate_freq_map(key):
    chars = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789 .,?!"
        "áčďéěíňóřšťúůýž"
        "ÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ"
    )
    np.random.seed(sum(ord(c) for c in key))
    np.random.shuffle(chars)
    freqs = np.linspace(1000, 6000, len(chars))
    return dict(zip(chars, freqs)), dict(zip(freqs, chars))

def encode_message(message, key):
    f_map, _ = generate_freq_map(key)
    audio = []
    for char in message:
        freq = f_map.get(char, 1500)
        t = np.linspace(0, BIT_DURATION, int(SAMPLE_RATE * BIT_DURATION), False)
        tone = 0.5 * np.sin(2 * np.pi * freq * t)
        audio.extend(tone)
    return np.array(audio)

def save_wav(filename, audio):
    sf.write(filename, audio, SAMPLE_RATE)

def decode_audio(filename, key):
    audio, sr = sf.read(filename)
    _, r_map = generate_freq_map(key)
    samples_per_bit = int(BIT_DURATION * sr)
    num_bits = len(audio) // samples_per_bit
    message = ""

    window = np.hanning(samples_per_bit)

    for i in range(num_bits):
        chunk = audio[i * samples_per_bit:(i + 1) * samples_per_bit]
        chunk = chunk * window
        spectrum = np.abs(np.fft.rfft(chunk))
        peak_index = np.argmax(spectrum)

        if 0 < peak_index < len(spectrum) - 1:
            alpha = spectrum[peak_index - 1]
            beta = spectrum[peak_index]
            gamma = spectrum[peak_index + 1]
            p = 0.5 * (alpha - gamma) / (alpha - 2 * beta + gamma)
            freq = (peak_index + p) * sr / len(chunk)
        else:
            freq = peak_index * sr / len(chunk)

        nearest = min(r_map.keys(), key=lambda x: abs(x - freq))
        message += r_map.get(nearest, '?')

    return message

# GUI
def create_gui():
    def generate_sha256():
        dialog = tk.Toplevel(root)
        dialog.title("Generate SHA-256")
        dialog.configure(bg="#212121")
        dialog.grab_set()

        tk.Label(dialog, text="Enter text to hash:", bg="#212121", fg="white").pack(padx=10, pady=(10, 0))
        entry = tk.Entry(dialog, bg="#141414", fg="white", insertbackground="white", width=40)
        entry.pack(padx=10, pady=10)

        def on_ok():
            text = entry.get()
            if text:
                hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
                key_entry.delete(0, tk.END)
                key_entry.insert(0, hashed)
            dialog.destroy()

        tk.Button(dialog, text="OK", command=on_ok, bg="#333333", fg="white").pack(pady=(0, 10))
        dialog.bind('<Return>', lambda e: on_ok())
        entry.focus()

    def switch_mode():
        if mode.get() == "Encrypt":
            output.delete("1.0", tk.END)
            bottom_input.config(state=tk.NORMAL)
        else:
            bottom_input.delete("1.0", tk.END)
            bottom_input.config(state=tk.DISABLED)
            nonlocal decrypt_file_path
            decrypt_file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
            if not decrypt_file_path:
                messagebox.showerror("Error", "No file selected for decryption")

    def process():
        k = key_entry.get()
        if not k:
            messagebox.showerror("Error", "Key is required")
            return
        if mode.get() == "Encrypt":
            msg = bottom_input.get("1.0", tk.END).strip()
            if not msg:
                messagebox.showerror("Error", "Message is empty")
                return
            audio = encode_message(msg, k)
            save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if save_path:
                save_wav(save_path, audio)
                messagebox.showinfo("Done", f"Saved to {save_path}")
        else:
            if not decrypt_file_path:
                messagebox.showerror("Error", "No file selected for decryption")
                return
            try:
                msg = decode_audio(decrypt_file_path, k)
                output.delete("1.0", tk.END)
                output.insert(tk.END, msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    global root
    root = tk.Tk()
    root.title("Secure Audio Encoder/Decoder")
    root.configure(bg="#212121")

    decrypt_file_path = ""

    mode = tk.StringVar(value="Encrypt")
    tk.Label(root, text="Mode:", bg="#212121", fg="white").pack()
    tk.Radiobutton(root, text="Encrypt", variable=mode, value="Encrypt", command=switch_mode, bg="#212121", fg="white", selectcolor="#333333").pack()
    tk.Radiobutton(root, text="Decrypt", variable=mode, value="Decrypt", command=switch_mode, bg="#212121", fg="white", selectcolor="#333333").pack()

    tk.Label(root, text="Secret Key:", bg="#212121", fg="white").pack()
    
    key_frame = tk.Frame(root, bg="#212121")
    key_frame.pack()

    key_entry = tk.Entry(key_frame, width=30, bg="#141414", fg="white", insertbackground="white")
    key_entry.pack(side=tk.LEFT, padx=(0,5))

    gen_button = tk.Button(key_frame, text="Generate SHA-256", command=generate_sha256, bg="#141414", fg="white", activebackground="#333333", activeforeground="white")
    gen_button.pack(side=tk.LEFT)

    tk.Label(root, text="Decrypted Output:", bg="#212121", fg="white").pack()
    output = tk.Text(root, height=5, bg="#141414", fg="white", insertbackground="white")
    output.pack()

    tk.Button(root, text="Run", command=process, bg="#333333", fg="white").pack(pady=10)

    tk.Label(root, text="Message to Encrypt:", bg="#212121", fg="white").pack()
    bottom_input = tk.Text(root, height=2, bg="#141414", fg="white", insertbackground="white")
    bottom_input.pack(fill="x")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
