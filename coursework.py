import tkinter as tk # graphical interface library
from tkinter import ttk, filedialog
import cv2 # OpenCV library
from PIL import Image, ImageTk # PIL image manipulation libraries
import threading
import course as c # importing the course module

class VideoApp:
    
    def update_frames(self):
        if not self.is_playing:
            return
        # read frame from video
        ret, frame = self.capp.read()
        if ret:
            # changing the frame size 
            frame = cv2.resize(frame, (400, 300)) 
            # conversion of frames from RGB to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
            # save the original frame
            self.frame = frame
            # display the original frame on the left
            img_left = Image.fromarray(frame) 
            self.left_photo = ImageTk.PhotoImage(image=img_left)
            self.left_canvas.create_image(0, 0, image=self.left_photo, anchor=tk.NW)
            # original processing
            processed_frame = frame

            # filters depending on the selected checkboxes
            if self.func1_var.get():
                # conversion frames from BGR to RGB
                processed_frame = c.convert_to_rgb(processed_frame)

            if self.func2_var.get():
                # shifting for frames
                try:
                    shear_value = float(self.entry_2.get()) # shift parameter
                except (AttributeError, ValueError):
                    shear_value = 0 # default value for shift
                processed_frame = c.video_shifting(processed_frame, shear_value)

            if self.func3_var.get():
                # canny filter for frames
                processed_frame = c.filter_canny(processed_frame)

            if self.func4_var.get():
                # bilateral filter for frames
                try:
                    d = int(self.entry1.get())
                    sigma_color = int(self.entry2.get())
                    sigma_space = int(self.entry3.get())
                except (AttributeError, ValueError):
                    d, sigma_color, sigma_space = 15, 75, 75 # default values for the Bilateral filter
                processed_frame = c.filter_bilateral(processed_frame, d, sigma_color, sigma_space)
            
            # processed frame on the right
            img_right = Image.fromarray(processed_frame)
            self.right_photo = ImageTk.PhotoImage(image=img_right)
            self.right_canvas.create_image(0, 0, image=self.right_photo, anchor=tk.NW)

        # frame update every 30 ms
        self.root.after(30, self.update_frames)  

    # start the video display
    def start_videos(self):
        if not self.capp or not self.capp.isOpened():
            return
        self.is_playing = True
        self.update_frames()

    # switching pause/resume
    def toggle_pause(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.update_frames()
        self.btn_pause_video.config(text="Pause" if self.is_playing else "Resume")

    # select a video file in the dialogue box
    def choose_video_file(self):
        filetypes = ("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")
        filename = filedialog.askopenfilename(title="Select a video file", filetypes=filetypes)
        if filename:
            if hasattr(self, 'capp') and self.capp:
                self.capp.release()
            self.capp = cv2.VideoCapture(filename)

    # initialising the user interface
    def __init__(self, root):
        # programme operation screen
        self.root = root
        self.root.title("Video comparison")
        self.root.geometry("810x550")
        self.root.configure(bg="pink")

        # label for original video
        self.left_label = tk.Label(root, text="Original video", bg="pink", fg="black", font=("Arial", 12, "bold"), pady=5)
        self.left_label.grid(row=0, column=0, sticky="n")
        # label for filter video
        self.right_label = tk.Label(root, text="Filter video", bg="pink", fg="black", font=("Arial", 12, "bold"), pady=5)
        self.right_label.grid(row=0, column=1, sticky="n")

        # canvas for video display
        self.left_canvas = tk.Canvas(root, width=400, height=300, bg='white')
        self.left_canvas.grid(row=1, column=0)

        self.right_canvas = tk.Canvas(root, width=400, height=300, bg='white')
        self.right_canvas.grid(row=1, column=1)

        # opening a video file
        self.capp = None
        self.is_playing = False

        # variables for the state of the checkboxes
        self.func1_var = tk.BooleanVar()
        self.func2_var = tk.BooleanVar()
        self.func3_var = tk.BooleanVar()
        self.func4_var = tk.BooleanVar()

        # frame for checkboxes and buttons
        self.checkbox_frame = tk.Frame(root, bg="pink")
        self.checkbox_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # video start button
        self.btn_load_left = tk.Button(self.checkbox_frame, text="Load the video", font=("Arial", 10, "bold"), bg="lightblue", fg="black", activebackground="#add8e6", bd=2, relief="raised", command=self.start_videos)
        self.btn_load_left.grid(row=0, column=1, sticky="w")

        # video selection button
        self.btn_choose_video = tk.Button(self.checkbox_frame, text="Select the video", font=("Arial", 10, "bold"), bg="lightgreen", fg="black", activebackground="#90ee90", bd=2, relief="raised", command=self.choose_video_file)
        self.btn_choose_video.grid(row=0, column=0, padx=3)

        # pause and resume video button
        self.btn_pause_video = tk.Button(self.checkbox_frame, text="Pause", font=("Arial", 10, "bold"), bg="orange", fg="black", activebackground="#ffcc80", bd=2, relief="raised", command=self.toggle_pause)
        self.btn_pause_video.grid(row=0, column=2, padx=2)

        # checkboxes for filters
        self.chk_function1 = tk.Checkbutton(self.checkbox_frame, text="Filter RGB", variable=self.func1_var, bg="pink", font=("Arial", 10))
        self.chk_function1.grid(row=1, column=0, sticky="w")

        self.chk_function2 = tk.Checkbutton(self.checkbox_frame, text="Video Shifting", variable=self.func2_var, bg="pink", font=("Arial", 10), command=self.toggle_func2_fields)
        self.chk_function2.grid(row=2, column=0, sticky="w")

        self.chk_function3 = tk.Checkbutton(self.checkbox_frame, text="Filter Canny", variable=self.func3_var, bg="pink", font=("Arial", 10))
        self.chk_function3.grid(row=3, column=0, sticky="w")

        self.chk_function4 = tk.Checkbutton(self.checkbox_frame, text="Filter Bilateral", variable=self.func4_var, bg="pink", font=("Arial", 10), command=self.toggle_func4_fields)
        self.chk_function4.grid(row=4, column=0, sticky="w")
        
    def validate_shear_input(self, value):
        # displaying an error message if the shift parameter is incorrect
        if value == "" or value.replace('.', '', 1).isdigit():  
            self.error_label_2.config(text="", bg="pink")
            return True
        else:
            self.error_label_2.config(text="Error! Try again :)", fg="blue", font=("monospace", 10, "bold"), bg="pink")
            return True

    def toggle_func2_fields(self):
        # display or hide the input field for the shift parameter
        if self.func2_var.get():
            self.label_2 = tk.Label(self.checkbox_frame, text="The shift parameter:", bg="pink")
            self.label_2.grid(row=2, column=1, padx=10)
            vcmd = (self.root.register(self.validate_shear_input), '%P')
            self.entry_2 = tk.Entry(self.checkbox_frame, width=10, validate='key', validatecommand=vcmd)
            self.entry_2.grid(row=2, column=2, padx=5)
            self.error_label_2 = tk.Label(self.checkbox_frame, text="", bg="pink", fg="red")
            self.error_label_2.grid(row=2, column=3, padx=5)
        else:
            if hasattr(self, 'label_2'):
                self.label_2.grid_remove()
            if hasattr(self, 'entry_2'):
                self.entry_2.grid_remove()
            if hasattr(self, 'error_label_2'):
                self.error_label_2.grid_remove()

    def toggle_func4_fields(self):
        # display or hide input fields for Bilateral filter parameters
        if self.func4_var.get():
            self.label1 = tk.Label(self.checkbox_frame, text="The filter diameter (from 5 to 25):", bg="pink")
            self.label1.grid(row=4, column=1, padx=5)
            self.entry1 = tk.Entry(self.checkbox_frame, width=10)
            self.entry1.grid(row=4, column=2, padx=5)

            self.label2 = tk.Label(self.checkbox_frame, text="The sigmaColor value (from 50 to 200):", bg="pink")
            self.label2.grid(row=5, column=1, padx=5)
            self.entry2 = tk.Entry(self.checkbox_frame, width=10)
            self.entry2.grid(row=5, column=2, padx=5)

            self.label3 = tk.Label(self.checkbox_frame, text="The sigmaSpace value (from 50 to 200):", bg="pink")
            self.label3.grid(row=6, column=1, padx=5)
            self.entry3 = tk.Entry(self.checkbox_frame, width=10)
            self.entry3.grid(row=6, column=2, padx=5)
        else:
            if hasattr(self, 'label1'):
                self.label1.grid_remove()
            if hasattr(self, 'entry1'):
                self.entry1.grid_remove()
            if hasattr(self, 'label2'):
                self.label2.grid_remove()
            if hasattr(self, 'entry2'):
                self.entry2.grid_remove()
            if hasattr(self, 'label3'):
                self.label3.grid_remove()
            if hasattr(self, 'entry3'):
                self.entry3.grid_remove()

# start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()

import cv2 # import library for working with videos
import numpy as np # import library for working with mathematical expressions and matrices

def load_video(source=0):  # open the video stream from the specified source (file or webcam)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():  # checking the opening of a video
        print("Error: Could not open video source")
        return None
    return cap
# converting a frame to RGB
def convert_to_rgb(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb
# shifting for frames
def video_shifting(frame, shear_factor=0.2): 
    height, width = frame.shape[:2]
    shear_matrix = np.float32([[1, shear_factor, 0], [0, 1, 0]])
    new_width = int(width + abs(shear_factor) * height)
    sheared_frame = cv2.warpAffine(frame, shear_matrix, (new_width, height))
    return sheared_frame
# canny filter for frames
def filter_canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges_low = cv2.Canny(gray, 50, 150)
    edges_mid = cv2.Canny(gray, 100, 200)
    edges_high = cv2.Canny(gray, 150, 250)
    combined = cv2.hconcat([edges_low, edges_mid, edges_high])
    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)
    return combined_rgb
# bilateral filter for frames
def filter_bilateral(frame, diameter=15, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(frame, diameter, sigma_color, sigma_space)

def play_video(source=0):
    cap = load_video(source) # open the video stream from the specified source (file or webcam)
    if cap is None:
        return
