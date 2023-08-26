
import tkinter as tk
from tkinter import filedialog, ttk

def select_mkv_file():
    """MKVファイルを選択するためのダイアログを表示"""
    filepath = filedialog.askopenfilename(filetypes=[("MKV files", "*.mkv")])
    mkv_file_label.config(text=f"Selected MKV: {filepath}")

def select_save_folder():
    """保存先フォルダを選択するためのダイアログを表示"""
    folderpath = filedialog.askdirectory()
    save_folder_label.config(text=f"Save to: {folderpath}")

# 以下、変換開始の処理は未実装
def start_conversion():
    """変換を開始する処理"""
    pass

# Tkinterのウィンドウを作成
root = tk.Tk()
root.title("MKV to MP4 Converter")

# レイアウトのフレームを作成
top_frame = tk.Frame(root)
middle_frame = tk.Frame(root)
bottom_frame = tk.Frame(root)

top_frame.pack(side=tk.TOP, fill=tk.X)
middle_frame.pack(side=tk.TOP, fill=tk.X)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# MKVファイル選択ボタン（上部）
select_mkv_button = tk.Button(top_frame, text="Select MKV File", command=select_mkv_file)
select_mkv_button.pack(side=tk.LEFT)

# 選択されたMKVファイルのパスを表示するラベル（上部）
mkv_file_label = tk.Label(top_frame, text="Selected MKV: None")
mkv_file_label.pack(side=tk.LEFT)

# 保存先選択ボタン（上部）
select_save_button = tk.Button(top_frame, text="Select Save Folder", command=select_save_folder)
select_save_button.pack(side=tk.LEFT)

# 選択された保存先のパスを表示するラベル（上部）
save_folder_label = tk.Label(top_frame, text="Save to: None")
save_folder_label.pack(side=tk.LEFT)

# 出力ファイル名指定（中央）
output_name_label = tk.Label(middle_frame, text="Output Name: ")
output_name_label.pack(side=tk.LEFT)
output_name_entry = tk.Entry(middle_frame)
output_name_entry.pack(side=tk.LEFT)

# マルチスレッドオプション（中央）
use_multithread = tk.BooleanVar()
use_multithread_checkbox = tk.Checkbutton(middle_frame, text="Use Multithreading", variable=use_multithread)
use_multithread_checkbox.pack(side=tk.LEFT)

# GPUオプション（中央）
use_gpu = tk.BooleanVar()
use_gpu_checkbox = tk.Checkbutton(middle_frame, text="Use GPU", variable=use_gpu)
use_gpu_checkbox.pack(side=tk.LEFT)

# 変換開始ボタン（下部）
start_button = tk.Button(bottom_frame, text="Start Conversion", command=start_conversion)
start_button.pack(side=tk.TOP)

# ウィンドウのイベントループを開始
root.mainloop()
