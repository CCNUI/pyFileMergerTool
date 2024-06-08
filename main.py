import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import datetime

class FileMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("文件合并工具")
        self.geometry("600x600")

        self.default_path = "C:\\Users\\HDR10\\Documents\\AIChat\\FileMerge\\"
        self.default_filename_template = "Prompt-$a_{}.txt".format(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.output_file_path = os.path.join(self.default_path, self.default_filename_template)
        self.file_list = []
        self.confirm_delete = True
        self.save_mode = tk.StringVar(value="append")

        self.create_widgets()

    def create_widgets(self):
        self.output_path_frame = tk.LabelFrame(self, text="输出文件路径设置")
        self.output_path_frame.pack(pady=10, fill="x")

        self.default_radio = tk.Radiobutton(self.output_path_frame, text="默认", value="default", command=self.use_default_path)
        self.default_radio.pack(anchor="w")
        self.default_radio.select()

        self.custom_radio = tk.Radiobutton(self.output_path_frame, text="自定义", value="custom", command=self.use_custom_path)
        self.custom_radio.pack(anchor="w")

        self.default_frame = tk.Frame(self.output_path_frame)
        self.default_frame.pack(fill="x")

        self.default_filename_label = tk.Label(self.default_frame, text="文件命名：Prompt-$a_YYYY-MM-DD.txt")
        self.default_filename_label.pack(anchor="w")

        self.default_filename_entry = tk.Entry(self.default_frame, width=20)
        self.default_filename_entry.pack(anchor="w")
        self.default_filename_entry.insert(0, "$a")
        self.default_filename_entry.bind("<KeyRelease>", self.sync_custom_filename)

        self.default_path_label = tk.Label(self.default_frame, text=f"默认保存路径: {self.default_path}")
        self.default_path_label.pack(anchor="w")

        self.custom_frame = tk.Frame(self.output_path_frame)
        self.custom_frame.pack(fill="x")
        self.custom_frame.pack_forget()

        self.custom_path_entry = tk.Entry(self.custom_frame, width=50)
        self.custom_path_entry.pack(side="left", padx=5)
        self.browse_button = tk.Button(self.custom_frame, text="选择输出路径", command=self.browse_output_path)
        self.browse_button.pack(side="left", padx=5)

        self.custom_filename_label = tk.Label(self.custom_frame, text="文件主题(可不填)：")
        self.custom_filename_label.pack(anchor="w", padx=5)
        self.custom_filename_entry = tk.Entry(self.custom_frame, width=50)
        self.custom_filename_entry.pack(anchor="w", padx=5)
        self.custom_filename_entry.bind("<KeyRelease>", self.sync_default_filename)

        self.auto_rename_button = tk.Button(self.custom_frame, text="自动重命名", command=self.auto_rename)
        self.auto_rename_button.pack(side="left", padx=5)
        self.reset_to_default_button = tk.Button(self.custom_frame, text="改回默认地址", command=self.reset_to_default)
        self.reset_to_default_button.pack(side="left", padx=5)

        self.drop_area_label = tk.Label(self, text="拖放文件到此区域", relief="solid", width=50, height=10)
        self.drop_area_label.pack(pady=20)
        self.drop_area_label.drop_target_register(DND_FILES)
        self.drop_area_label.dnd_bind('<<Drop>>', self.handle_drop)

        self.save_mode_frame = tk.LabelFrame(self, text="保存模式")
        self.save_mode_frame.pack(pady=10, fill="x")

        self.append_radio = tk.Radiobutton(self.save_mode_frame, text="追加", variable=self.save_mode, value="append")
        self.append_radio.pack(anchor="w")
        self.overwrite_radio = tk.Radiobutton(self.save_mode_frame, text="覆盖", variable=self.save_mode, value="overwrite")
        self.overwrite_radio.pack(anchor="w")
        self.newfile_radio = tk.Radiobutton(self.save_mode_frame, text="新建文件", variable=self.save_mode, value="newfile")
        self.newfile_radio.pack(anchor="w")

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        self.save_button = tk.Button(self.buttons_frame, text="保存到TXT文件", command=self.save_to_txt)
        self.save_button.pack(side="left", padx=5)
        self.open_button = tk.Button(self.buttons_frame, text="打开当前文件", command=self.open_current_file)
        self.open_button.pack(side="left", padx=5)

        self.log_text = tk.Text(self, height=10, state="disabled")
        self.log_text.pack(pady=10, fill="x")

    def use_default_path(self):
        self.custom_frame.pack_forget()
        self.default_frame.pack(fill="x")
        self.update_output_file_path()

    def use_custom_path(self):
        self.default_frame.pack_forget()
        self.custom_frame.pack(fill="x")
        self.update_output_file_path()

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.output_file_path = file_path
            self.custom_path_entry.delete(0, tk.END)
            self.custom_path_entry.insert(0, file_path)

    def auto_rename(self):
        if self.custom_filename_entry.get():
            filename = f"Prompt-{self.custom_filename_entry.get()}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
            self.output_file_path = os.path.join(os.path.dirname(self.output_file_path), filename)
            self.custom_path_entry.delete(0, tk.END)
            self.custom_path_entry.insert(0, self.output_file_path)

    def reset_to_default(self):
        self.output_file_path = os.path.join(self.default_path, self.default_filename_template)
        self.custom_path_entry.delete(0, tk.END)
        self.custom_path_entry.insert(0, self.output_file_path)

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file):
                self.file_list.append(file)
                self.drop_area_label.config(text="\n".join(self.file_list))

    def confirm_delete_file(self, file):
        if self.confirm_delete:
            confirm_dialog = tk.Toplevel(self)
            confirm_dialog.title("确认删除")
            tk.Label(confirm_dialog, text=f"将删除 {os.path.basename(file)}，确认？").pack(pady=10)
            confirm_var = tk.BooleanVar(value=False)
            confirm_checkbox = tk.Checkbutton(confirm_dialog, text="本次运行不再弹出", variable=confirm_var)
            confirm_checkbox.pack(pady=5)

            def on_confirm():
                self.confirm_delete = not confirm_var.get()
                self.file_list.remove(file)
                self.drop_area_label.config(text="\n".join(self.file_list))
                confirm_dialog.destroy()

            def on_cancel():
                confirm_dialog.destroy()

            tk.Button(confirm_dialog, text="确认", command=on_confirm).pack(side="left", padx=10, pady=10)
            tk.Button(confirm_dialog, text="取消", command=on_cancel).pack(side="right", padx=10, pady=10)

            confirm_dialog.transient(self)
            confirm_dialog.grab_set()
            self.wait_window(confirm_dialog)
        else:
            self.file_list.remove(file)
            self.drop_area_label.config(text="\n".join(self.file_list))

    def save_to_txt(self):
        if not self.output_file_path:
            messagebox.showerror("错误", "请先选择输出文件路径")
            return

        try:
            if self.save_mode.get() == "append":
                mode = 'a'
            elif self.save_mode.get() == "overwrite":
                mode = 'w'
            elif self.save_mode.get() == "newfile":
                base, ext = os.path.splitext(self.output_file_path)
                counter = 1
                while os.path.exists(self.output_file_path):
                    self.output_file_path = f"{base}_{counter}{ext}"
                    counter += 1
                mode = 'w'
            else:
                raise ValueError("未知的保存模式")

            if not os.path.exists(os.path.dirname(self.output_file_path)):
                os.makedirs(os.path.dirname(self.output_file_path))

            with open(self.output_file_path, mode, encoding='utf-8') as outfile:
                for file in self.file_list:
                    try:
                        with open(file, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                    except UnicodeDecodeError:
                        with open(file, 'r', encoding='latin1') as infile:
                            content = infile.read()
                    outfile.write(f"文件名: {os.path.basename(file)}\n")
                    outfile.write(content)
                    outfile.write("\n\n")
            self.log(f"{datetime.datetime.now().strftime('%H:%M:%S')} 文件{self.save_mode.get()} 成功，{self.output_file_path}")
            messagebox.showinfo("成功", "文件已成功保存")
        except Exception as e:
            self.log(f"{datetime.datetime.now().strftime('%H:%M:%S')} 错误：{e}")
            messagebox.showerror("错误", f"保存文件时出错：{e}")

    def open_current_file(self):
        if os.path.exists(self.output_file_path):
            os.startfile(self.output_file_path)
        else:
            messagebox.showerror("错误", "文件不存在")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")

    def sync_custom_filename(self, event):
        self.custom_filename_entry.delete(0, tk.END)
        self.custom_filename_entry.insert(0, self.default_filename_entry.get())
        self.update_output_file_path()

    def sync_default_filename(self, event):
        self.default_filename_entry.delete(0, tk.END)
        self.default_filename_entry.insert(0, self.custom_filename_entry.get())
        self.update_output_file_path()

    def update_output_file_path(self):
        if self.default_radio.select():
            filename = f"Prompt-{self.default_filename_entry.get()}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
            self.output_file_path = os.path.join(self.default_path, filename)
        else:
            filename = f"Prompt-{self.custom_filename_entry.get()}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
            self.output_file_path = os.path.join(os.path.dirname(self.custom_path_entry.get()), filename)

if __name__ == "__main__":
    app = FileMergerApp()
    app.mainloop()
