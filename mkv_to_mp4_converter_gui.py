
# 必要なライブラリをインポート
from tkinter import Tk, Label, Button, Entry, filedialog, OptionMenu, StringVar, Checkbutton, IntVar
import subprocess
import os

# 主要なGUIクラス
class MKVtoMP4Converter:
    def __init__(self, master):
        self.master = master
        master.title("MKV to MP4 Converter")
        
        self.language = StringVar(master)
        self.language.set("日本語")  # デフォルトを日本語に設定
        self.language.trace_add("write", self.update_language)
        
        self.language_menu = OptionMenu(master, self.language, "日本語", "English")
        self.language_menu.grid(row=0, column=3)
        
        self.label1 = Label(master, text="MKV File Path:")
        self.label1.grid(row=1, column=0)
        self.entry1 = Entry(master)
        self.entry1.grid(row=1, column=1)
        
        self.browse_button1 = Button(master, text="Browse", command=self.browse_file)
        self.browse_button1.grid(row=1, column=2)
        
        self.label2 = Label(master, text="Save Location:")
        self.label2.grid(row=2, column=0)
        self.entry2 = Entry(master)
        self.entry2.grid(row=2, column=1)
        
        self.browse_button2 = Button(master, text="Browse", command=self.browse_location)
        self.browse_button2.grid(row=2, column=2)
        
        self.label3 = Label(master, text="Output Filename:")
        self.label3.grid(row=3, column=0)
        self.entry3 = Entry(master)
        self.entry3.grid(row=3, column=1)
        
        self.use_multithread = IntVar()
        self.multithread_check = Checkbutton(master, text="Use Multi-threading", variable=self.use_multithread)
        self.multithread_check.grid(row=4, column=0)
        
        self.use_gpu = IntVar()
        self.gpu_check = Checkbutton(master, text="Use GPU", variable=self.use_gpu)
        self.gpu_check.grid(row=4, column=1)
        
        self.convert_button = Button(master, text="Start Conversion", command=self.convert)
        self.convert_button.grid(row=5, columnspan=3)
        
        # プログラムが起動したときに、update_language メソッドを呼び出す
        self.update_language()
        
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.entry1.delete(0, 'end')
        self.entry1.insert(0, file_path)
        
    def browse_location(self):
        location = filedialog.askdirectory()
        self.entry2.delete(0, 'end')
        self.entry2.insert(0, location)
        
    def convert(self):
        # ユーザーが指定したMKVファイルのパスと保存先を取得
        input_file_path = self.entry1.get()
        output_location = self.entry2.get()
        output_filename = self.entry3.get() if self.entry3.get() else os.path.splitext(os.path.basename(input_file_path))[0] + "_No"
        output_file_path = f"{output_location}/{output_filename}.mp4"
        
        # ffmpegのコマンドライン引数を設定
        cmd_args = ["ffmpeg", "-i", input_file_path, "-c:v", "libx265", "-crf", "28", "-map_chapters", "-1"]
        
        # マルチスレッドの使用
        if self.use_multithread.get() == 1:
            cmd_args.extend(["-threads", "0"])
            
        # GPUの使用
        if self.use_gpu.get() == 1:
            cmd_args.extend(["-vf", "format=yuv420p10le,hwupload,tonemap_vaapi=format=nv12,hwdownload"])
        
        cmd_args.append(output_file_path)
        
        # ffmpegをサブプロセスとして実行
        # チャプター情報を取得
        cmd_args_chapter = ["ffmpeg", "-hide_banner", "-i", input_file_path]
        result = subprocess.run(cmd_args_chapter, stderr=subprocess.PIPE, text=True)
        chapter_info = result.stderr
        chapter_count = chapter_info.count('Chapter #')
        
        # チャプター毎にファイルを分割して保存
        for i in range(chapter_count):
            output_file_chapter = f"{output_file_path.rsplit('.', 1)[0]}_Chapter{i+1}.mp4"
            cmd_args_chapter_convert = cmd_args.copy()
            cmd_args_chapter_convert.extend(["-ss", f"{i*duration/chapter_count}", "-to", f"{(i+1)*duration/chapter_count}", "-an"])
            cmd_args_chapter_convert.append(output_file_chapter)
            subprocess.run(cmd_args_chapter_convert)

        subprocess.run(cmd_args)
        
    def update_language(self, *args):
        selected_language = self.language.get()
        if selected_language == "日本語":
            self.label1.config(text="MKVファイルのパス:")
            self.label2.config(text="保存先:")
            self.label3.config(text="出力ファイル名:")
            self.browse_button1.config(text="参照")
            self.browse_button2.config(text="参照")
            self.multithread_check.config(text="マルチスレッドを使用")
            self.gpu_check.config(text="GPUを使用")
            self.convert_button.config(text="変換開始")
        else:
            self.label1.config(text="MKV File Path:")
            self.label2.config(text="Save Location:")
            self.label3.config(text="Output Filename:")
            self.browse_button1.config(text="Browse")
            self.browse_button2.config(text="Browse")
            self.multithread_check.config(text="Use Multi-threading")
            self.gpu_check.config(text="Use GPU")
            self.convert_button.config(text="Start Conversion")

if __name__ == "__main__":
    root = Tk()
    my_converter = MKVtoMP4Converter(root)
    root.mainloop()
