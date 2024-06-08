import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import datetime
import chardet

class FileMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("文件合并工具")
        self.geometry("620x420")

        # 获取当前用户的UserProfile目录
        user_profile = os.path.expanduser("~")
        self.default_path = os.path.join(user_profile, "Documents", "AIChat", "FileMerge")
        self.default_filename_template = "Prompt-unnamed_{}.txt".format(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.output_file_path = os.path.join(self.default_path, self.default_filename_template)
        self.file_list = []
        self.confirm_delete = True
        self.save_mode = tk.StringVar(value="newfile")

        self.create_widgets()

    def create_widgets(self):
        self.output_path_frame = tk.LabelFrame(self, text="输出文件路径设置")
        self.output_path_frame.pack(pady=10, fill="x")

        self.custom_frame = tk.Frame(self.output_path_frame)
        self.custom_frame.pack(fill="x")

        self.custom_path_entry = tk.Entry(self.custom_frame, width=50)
        self.custom_path_entry.pack(side="left", padx=5)
        self.browse_button = tk.Button(self.custom_frame, text="选择输出路径", command=self.browse_output_path)
        self.browse_button.pack(side="left", padx=5)

        self.custom_filename_label = tk.Label(self.custom_frame, text="文件主题(默认unnamed)：")
        self.custom_filename_label.pack(anchor="w", padx=5)
        self.custom_filename_entry = tk.Entry(self.custom_frame, width=50)
        self.custom_filename_entry.pack(anchor="w", padx=5)
        self.custom_filename_entry.bind("<KeyRelease>", self.update_output_file_path)

        self.auto_rename_button = tk.Button(self.custom_frame, text="自动重命名", command=self.auto_rename)
        self.auto_rename_button.pack(side="left", padx=5)
        self.reset_to_default_button = tk.Button(self.custom_frame, text="回默认地址", command=self.reset_to_default)
        self.reset_to_default_button.pack(side="left", padx=5)

        self.drop_area_label = tk.Label(self, text="拖放文件到此区域", relief="solid", width=50, height=10)
        self.drop_area_label.pack(pady=20)
        self.drop_area_label.drop_target_register(DND_FILES)
        self.drop_area_label.dnd_bind('<<Drop>>', self.handle_drop)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10, fill="x")

        self.save_mode_frame = tk.Frame(self.buttons_frame)
        self.save_mode_frame.pack(side="left", padx=5)

        self.append_radio = tk.Radiobutton(self.save_mode_frame, text="追加", variable=self.save_mode, value="append")
        self.append_radio.pack(side="left")
        self.overwrite_radio = tk.Radiobutton(self.save_mode_frame, text="覆盖", variable=self.save_mode, value="overwrite")
        self.overwrite_radio.pack(side="left")
        self.newfile_radio = tk.Radiobutton(self.save_mode_frame, text="新建文件", variable=self.save_mode, value="newfile")
        self.newfile_radio.pack(side="left")
        self.newfile_radio.select()

        self.save_button = tk.Button(self.buttons_frame, text="保存到TXT文件", command=self.save_to_txt)
        self.save_button.pack(side="left", padx=5)
        self.open_button = tk.Button(self.buttons_frame, text="打开当前文件", command=self.open_current_file)
        self.open_button.pack(side="left", padx=5)

        # 添加info图标按钮到右侧
        self.info_button = tk.Button(self.buttons_frame, text="info...", command=self.show_info)
        self.info_button.pack(side="right", padx=5)

        self.log_text = tk.Text(self, height=10, state="disabled")
        self.log_text.pack(pady=10, fill="x")

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.output_file_path = file_path
            self.custom_path_entry.delete(0, tk.END)
            self.custom_path_entry.insert(0, file_path)
            self.custom_path_entry.xview_moveto(1)  # 将光标移动到文本的最右边

    def auto_rename(self):
        subject = self.custom_filename_entry.get() or "unnamed"
        filename = f"Prompt-{subject}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        self.output_file_path = os.path.join(os.path.dirname(self.output_file_path), filename)
        self.custom_path_entry.delete(0, tk.END)
        self.custom_path_entry.insert(0, self.output_file_path)
        self.custom_path_entry.xview_moveto(1)  # 将光标移动到文本的最右边

    def reset_to_default(self):
        subject = self.custom_filename_entry.get() or "unnamed"
        filename = f"Prompt-{subject}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        self.output_file_path = os.path.join(self.default_path, filename)
        self.custom_path_entry.delete(0, tk.END)
        self.custom_path_entry.insert(0, self.output_file_path)
        self.custom_path_entry.xview_moveto(1)  # 将光标移动到文本的最右边

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

            with open(self.output_file_path, mode, encoding='utf-16') as outfile:
                for file in self.file_list:
                    with open(file, 'rb') as infile:
                        raw_data = infile.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding']
                        content = raw_data.decode(encoding)
                    outfile.write(f"文件名: {os.path.basename(file)}\n")
                    outfile.write(content)
                    outfile.write("\n\n")
            self.log(f"{datetime.datetime.now().strftime('%H:%M:%S')} 文件{self.save_mode.get()} 成功，{self.output_file_path}")
            # messagebox.showinfo("成功", "文件已成功保存")
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

    def update_output_file_path(self, event=None):
        subject = self.custom_filename_entry.get() or "unnamed"
        filename = f"Prompt-{subject}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        self.output_file_path = os.path.join(os.path.dirname(self.custom_path_entry.get()), filename)
        self.custom_path_entry.delete(0, tk.END)
        self.custom_path_entry.insert(0, self.output_file_path)
        self.custom_path_entry.xview_moveto(1)  # 将光标移动到文本的最右边

    def show_info(self):
        info_text = (
            "软件名：文件合并工具\n"
            "软件简介：用于合并多个文件内容到一个TXT文件中\n"
            "版本: v3.0\n"
            "制作：CCNUI\n"
            "licence：Apache GPL 2.0\n"
            "项目gitHub链接：https://github.com/ccnui/文件合并工具\n"
            "帮助文档：https://uzt.cc/文件合并工具/helpfile\n"
            "文档编写日期：2024-6-8\n"
            "---\n"
            "使用说明：\n"
            "1. 点击“选择输出路径”按钮选择或输入输出文件的路径。\n"
            "2. 在“文件主题”输入框中输入文件主题（可选）。\n"
            "3. 将要合并的文件拖放到“拖放文件到此区域”。\n"
            "4. 选择保存模式（追加、覆盖、新建文件）。\n"
            "5. 点击“保存到TXT文件”按钮保存合并后的文件。\n"
            "6. 点击“打开当前文件”按钮查看合并后的文件。"
        )
        info_window = tk.Toplevel(self)
        info_window.title("作者声明")
        info_label = tk.Label(info_window, text=info_text, justify="left")
        info_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    app = FileMergerApp()
    app.mainloop()
