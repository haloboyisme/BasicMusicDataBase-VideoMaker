import moviepy.editor as mp
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("JPEG files", "*.jpg")])
    image_textbox.delete(0, tk.END)
    image_textbox.insert(0, image_path)

def select_audio():
    global audio_path
    audio_path = filedialog.askopenfilename(title="Select Audio", filetypes=[("WAV files", "*.wav")])
    audio_textbox.delete(0, tk.END)
    audio_textbox.insert(0, audio_path)

def select_output():
    global output_path
    output_path = filedialog.asksaveasfilename(title="Save Video As", defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    output_textbox.delete(0, tk.END)
    output_textbox.insert(0, output_path)

def make_video():
    if image_path and audio_path and output_path:
        # read in image and audio files
        image_clip = mp.ImageClip(image_path)
        audio_clip = mp.AudioFileClip(audio_path)

        # create video clip with image and audio
        video_clip = image_clip.set_audio(audio_clip).set_duration(audio_clip.duration)

        # write video file to output path
        video_clip.write_videofile(output_path, fps=60, codec="libx264", audio_codec="aac", bitrate="50M")
        
        # show pop-up message when rendering is complete
        messagebox.showinfo(title="Rendering Complete", message="Video rendering is complete.")

# create GUI
root = tk.Tk()
root.title("Create Video")
root.geometry("500x250")

# create image input
image_label = tk.Label(root, text="Image:")
image_label.grid(row=0, column=0)

image_textbox = tk.Entry(root, width=50)
image_textbox.grid(row=0, column=1)

image_button = tk.Button(root, text="Select Image", command=select_image)
image_button.grid(row=0, column=2)

# create audio input
audio_label = tk.Label(root, text="Audio:")
audio_label.grid(row=1, column=0)

audio_textbox = tk.Entry(root, width=50)
audio_textbox.grid(row=1, column=1)

audio_button = tk.Button(root, text="Select Audio", command=select_audio)
audio_button.grid(row=1, column=2)

# create output path input
output_label = tk.Label(root, text="Output:")
output_label.grid(row=2, column=0)

output_textbox = tk.Entry(root, width=50)
output_textbox.grid(row=2, column=1)

output_button = tk.Button(root, text="Select Output", command=select_output)
output_button.grid(row=2, column=2)

# create "Make Video" button
make_video_button = tk.Button(root, text="Make Video", command=make_video)
make_video_button.grid(row=3, column=1)

root.mainloop()
