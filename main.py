import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pynput import keyboard
class KeyRecorder:

    def __init__(self):
        self.recording_active = False
        self.root = tk.Tk()
        self.root.title("Keystroke Recorder")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.root.configure(bg="#53A7C4")

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit?", command=exit)
        self.filemenu.add_separator()

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Actions")

        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text="Keystroke Recorder", font=("Arial", 18), background="#53A7C4")
        self.label.pack(padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="Recording Inactive", font=("Arial", 18), background="#53A7C4")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 16), foreground="white", background="black")
        self.textbox.pack(padx=10, pady=10)

        buttonframe = ttk.Frame(self.root)
        buttonframe.pack()
        buttonframe.rowconfigure(0, weight=1)
        buttonframe.rowconfigure(1, weight=2)
        buttonframe.rowconfigure(2, weight=3)
        buttonframe.rowconfigure(3, weight=4)

        self.recordKeystrokes = ttk.Button(buttonframe, text="Record Keystrokes", command=self.record_keystrokes)
        self.recordKeystrokes.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.clearButton = ttk.Button(buttonframe, text="Clear", command=self.clear_recording)
        self.clearButton.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.quitRecord = ttk.Button(buttonframe, text="Stop", command=self.quit_record)
        self.quitRecord.grid(row=0, column=2, sticky=tk.W+tk.E)

        self.writeButton = ttk.Button(buttonframe, text="Write to File", command=self.write_to_file)
        self.writeButton.grid(row=0, column=3, sticky=tk.W+tk.E)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()

    def close_app(self):
        if messagebox.askyesno(title="Close Application?", message="Are you sure you want to exit?"):
            self.root.destroy()

    def record_keystrokes(self):
        if not self.recording_active:
            if hasattr(self, 'listener') and self.listener.is_alive():
                self.listener.stop()
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()
            self.recording_active = True
            self.update_status("Recording Active")

    def on_key_press(self, key):
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.space:
                self.textbox.insert(tk.END, " ")
                print('Key pressed: Spacebar')
            else:
                self.textbox.insert(tk.END, f"\n{key}\n")
                print(f'Key pressed: {key}')
        else:
            try:
                if key.char and key.char.isalnum():
                    self.textbox.insert(tk.END, key.char)
                    print(f'Alphanumeric Key pressed: {key.char}')
            except AttributeError:
                pass

    def clear_recording(self):
        self.textbox.delete("1.0", tk.END)

    def write_to_file(self):
        text_content = self.textbox.get("1.0", tk.END)
        if text_content.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text_content)

    def update_status(self, status):
        self.status_label.config(text=status)

    def quit_record(self):
        if self.recording_active:
            self.update_status("Recording Inactive")
            self.listener.stop()
            self.recording_active = False





KeyRecorder()
