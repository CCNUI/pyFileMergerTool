import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

class FileMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("文件合并工具")
        self.geometry("600x400")

        self.output_file_path = None
        self.file_list = []

        self.create_widgets()

    def create_widgets(self):
        self.output_path_label = tk.Label(self, text="输出文件路径：")
        self.output_path_label.pack(pady=10)

        self.output_path_entry = tk.Entry(self, width=50)
        self.output_path_entry.pack(pady=10)

        self.browse_button = tk.Button(self, text="选择输出路径", command=self.browse_output_path)
        self.browse_button.pack(pady=10)

        self.drop_area_label = tk.Label(self, text="拖放文件到此区域", relief="solid", width=50, height=10)
        self.drop_area_label.pack(pady=20)
        self.drop_area_label.drop_target_register(DND_FILES)
        self.drop_area_label.dnd_bind('<<Drop>>', self.handle_drop)

        self.save_button = tk.Button(self, text="保存到TXT文件", command=self.save_to_txt)
        self.save_button.pack(pady=10)

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.output_file_path = file_path
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file):
                self.file_list.append(file)
                self.drop_area_label.config(text="\n".join(self.file_list))

    def save_to_txt(self):
        if not self.output_file_path:
            messagebox.showerror("错误", "请先选择输出文件路径")
            return

        try:
            with open(self.output_file_path, 'a', encoding='utf-8') as outfile:
                for file in self.file_list:
                    with open(file, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(f"文件名: {os.path.basename(file)}\n")
                        outfile.write(content)
                        outfile.write("\n\n")
            messagebox.showinfo("成功", "文件已成功保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件时出错：{e}")

if __name__ == "__main__":
    app = FileMergerApp()
    app.mainloop()
