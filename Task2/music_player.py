#importing reqd modules
import tkinter as tk
from tkinter import filedialog,font
import pygame
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk
import imageio

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#00BCD4")

        pygame.mixer.init()
        
        self.playlist_paths = []  # Initialize the list to store full path
        self.visualizer_gif = None
        
        button_bg_color = "#FF5722"
        button_fg_color = "white"
        button_font = ("Helvetica", 12)

        #Playlist Box
        self.playlist = tk.Listbox(root, 
                                   selectmode=tk.SINGLE, 
                                   bg="black", 
                                   fg="white",
                                   height=10, 
                                   font=("Helvetica", 12))
        self.playlist.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        # Create buttons with appropriate colors
        self.load_button = tk.Button(root, 
                                     text="Load Music", 
                                     command=self.load_music, 
                                     font=button_font, 
                                     bg=button_bg_color, 
                                     fg=button_fg_color)
        self.load_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.play_button = tk.Button(root, 
                                     text="Play", 
                                     command=self.play_music, 
                                     font=button_font, 
                                     bg=button_bg_color, 
                                     fg=button_fg_color)
        self.play_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.pause_button = tk.Button(root, 
                                      text="Pause", 
                                      command=self.pause_music, 
                                      font=button_font, 
                                      bg=button_bg_color, 
                                      fg=button_fg_color)
        self.pause_button.grid(row=1, column=2, padx=20, pady=10, sticky="ew")

        self.stop_button = tk.Button(root, 
                                     text="Stop", 
                                     command=self.stop_music, 
                                     font=button_font, 
                                     bg=button_bg_color, 
                                     fg=button_fg_color)
        self.stop_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.next_button = tk.Button(root, 
                                     text="Next", 
                                     command=self.play_next_track, 
                                     font=button_font, bg=button_bg_color, 
                                     fg=button_fg_color)
        self.next_button.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.prev_button = tk.Button(root, 
                                     text="Previous", 
                                     command=self.play_prev_track, 
                                     font=button_font, 
                                     bg=button_bg_color, 
                                     fg=button_fg_color)
        self.prev_button.grid(row=2, column=2, padx=20, pady=10, sticky="ew")

        self.delete_button = tk.Button(root, 
                                       text="Delete Track", 
                                       command=self.delete_track, 
                                       font=button_font, 
                                       bg=button_bg_color, 
                                       fg=button_fg_color)
        self.delete_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.exit_button = tk.Button(root, 
                                     text="Exit", 
                                     command=root.destroy, 
                                     font=button_font, 
                                     bg="indian red")
        self.exit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=10, sticky="ew")

        #Labels
        bold_font = font.Font(weight="bold", size=12)
        self.current_song_label = tk.Label(root, 
                                           text="Currently Playing:", 
                                           font=bold_font, 
                                           bg="#00BCD4", 
                                           fg=button_fg_color)
        self.current_song_label.grid(row=4, column=0, columnspan=3, padx=20, pady=5, sticky="w")

        
        self.visualizer_label = tk.Label(root)
        self.visualizer_label.grid(row=5, column=0, columnspan=3, padx=20, pady=5)
        

        # Configure the layout to ensure the labels are visible
        root.grid_rowconfigure(4, weight=1)  # Adjust row 4
        root.grid_rowconfigure(5, weight=1)  # Adjust row 5
        root.grid_columnconfigure(0, weight=1)  # Adjust column 0
        root.grid_columnconfigure(1, weight=1)  # Adjust column 1
        root.grid_columnconfigure(2, weight=1)  # Adjust column 2

        self.current_song = None
        self.isPlaying = False
    
    # audio_visualizer gif
    def update_visualizer(self, gif_path):
        self.visualizer_label.image = None 
        gif_frames = imageio.mimread(gif_path, memtest=False)

        def update_frame(frame_idx=0):
            if self.isPlaying:  # Only update if playing
                image = Image.fromarray(gif_frames[frame_idx])
                image = image.resize((350, 150))  # Adjust width and height as needed
                gif_frame = ImageTk.PhotoImage(image=image)

                self.visualizer_label.config(image=gif_frame)
                self.visualizer_label.image = gif_frame

                next_frame_idx = (frame_idx + 1) % len(gif_frames)
                self.root.after(100, update_frame, next_frame_idx)

        update_frame()

    #Play Function
    def play_music(self):
        selected_index = self.playlist.curselection()
        if selected_index:
            selected_song = self.playlist.get(selected_index)
            selected_path = self.playlist_paths[selected_index[0]]  # Get the full path
            if self.current_song != selected_song:
                pygame.mixer.music.load(selected_path)  # Load the full path
                pygame.mixer.music.play()
                self.current_song = selected_song
                self.isPlaying = True
            elif not self.isPlaying:
                pygame.mixer.music.unpause()
                self.isPlaying = True
        self.update_song_info()
        self.update_visualizer("audio_visualizer.gif")

    #Currently Playing 
    def update_song_info(self):
        if self.current_song:
            song_name = os.path.basename(self.current_song)
            bold_font = font.Font(weight="bold",size=12)
            self.current_song_label.config(text=f"Currently Playing: {self.current_song}", font=bold_font)
        else:
            bold_font = font.Font(weight="bold",size=12)
            self.current_song_label.config(text="Currently Playing: ", font=bold_font)
    
    #Pause Function
    def pause_music(self):
        if self.isPlaying:
            pygame.mixer.music.pause()
            self.isPlaying = False
            self.visualizer_label.config(image=None)  # Clear the visualizer
        self.update_song_info()
    
    #Stop Function
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_song = None
        self.isPlaying = False
        self.visualizer_label.config(image=None)  # Clear the visualizer
        self.update_song_info()

    #Next Track Function
    def play_next_track(self):
        selected_index = self.playlist.curselection()
        if selected_index:
            next_index = selected_index[0] + 1
            if next_index < len(self.playlist_paths):  # Use playlist_paths length
                next_song = os.path.basename(self.playlist_paths[next_index])  # Get song name
                pygame.mixer.music.load(self.playlist_paths[next_index])  # Load full path
                pygame.mixer.music.play()
                self.current_song = next_song
                self.isPlaying = True
                self.update_song_info()
                self.update_visualizer("audio_visualizer.gif")
    
    #Prev Track Function
    def play_prev_track(self):
        selected_index = self.playlist.curselection()
        if selected_index:
            prev_index = selected_index[0] - 1
            if prev_index >= 0:
                prev_song = os.path.basename(self.playlist_paths[prev_index])  # Get song name
                pygame.mixer.music.load(self.playlist_paths[prev_index])  # Load full path
                pygame.mixer.music.play()
                self.current_song = prev_song
                self.isPlaying = True
                self.update_song_info()
                self.update_visualizer("audio_visualizer.gif")

    #Load Playlist Function
    def load_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.mp4 *.ogg *.wav")])
        if file_paths:
            for file_path in file_paths:
                song_name = os.path.basename(file_path)  # Get just the song name
                self.playlist.insert(tk.END, song_name)  # Insert the song name
                self.playlist_paths.append(file_path)  # Store the full path
        self.update_song_info()

    def delete_track(self):
        selected_index = self.playlist.curselection()
        if selected_index:
            index_to_delete = selected_index[0]
            self.playlist.delete(index_to_delete)
            self.playlist_paths.pop(index_to_delete)
            self.update_song_info()

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop() 

