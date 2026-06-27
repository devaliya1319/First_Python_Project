import os
import shutil
import tkinter as tk
from tkinter import messagebox

# --- THE CORE LOGIC (From your previous script) ---
def clean_folder():
    user_profile = os.path.expanduser('~')
    track_folder = os.path.join(user_profile, 'Downloads')

    file_types = {
        '.pdf': 'Documents', '.docx': 'Documents', '.txt': 'Documents',
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
        '.zip': 'Compressed', '.mp4': 'Videos', '.exe': 'Installers'
    }

    # Clear the text box in the app before starting
    log_box.delete('1.0', tk.END)
    files_moved_count = 0

    try:
        for filename in os.listdir(track_folder):
            file_path = os.path.join(track_folder, filename)
            
            if os.path.isfile(file_path):
                name, extension = os.path.splitext(filename)
                extension = extension.lower()
                
                if extension in file_types:
                    folder_name = file_types[extension]
                    target_folder = os.path.join(track_folder, folder_name)
                    
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                        
                    destination_path = os.path.join(target_folder, filename)
                    counter = 1
                    
                    while os.path.exists(destination_path):
                        new_filename = f"{name}_{counter}{extension}"
                        destination_path = os.path.join(target_folder, new_filename)
                        counter += 1
                        
                    shutil.move(file_path, destination_path)
                    final_name = os.path.basename(destination_path)
                    
                    # Instead of printing to terminal, log it to the app's visual window
                    log_box.insert(tk.END, f" Moved: {filename} -> {folder_name}/{final_name}\n")
                    files_moved_count += 1

        if files_moved_count == 0:
            log_box.insert(tk.END, " Your Downloads folder is already clean!\n")
            messagebox.showinfo("Done!", "No files needed sorting.")
        else:
            log_box.insert(tk.END, f"\n Success! Organized {files_moved_count} files.")
            messagebox.showinfo("Success!", f"Successfully organized {files_moved_count} files!")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")


# --- THE GUI WINDOW LAYOUT ---
# 1. Initialize the main window
root = tk.Tk()
root.title("Smart File Organizer")
root.geometry("500x400")
root.configure(bg="#f0f4f8") # Clean light grey/blue background

# 2. Title Header Label
title_label = tk.Label(root, text="Downloads Organizer", font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#1a365d")
title_label.pack(pady=15)

# 3. Target Folder Label
user_profile = os.path.expanduser('~')
downloads_path = os.path.join(user_profile, 'Downloads')
path_label = tk.Label(root, text=f"Target: {downloads_path}", font=("Arial", 9, "italic"), bg="#f0f4f8", fg="#4a5568")
path_label.pack(pady=5)

# 4. The BIG Clean Button
# We link it to our clean_folder function using 'command=clean_folder'
clean_button = tk.Button(root, text="🧹 Clean My Folder", font=("Arial", 12, "bold"), 
                         bg="#3182ce", fg="white", padx=20, pady=10, 
                         activebackground="#2b6cb0", activeforeground="white",
                         command=clean_folder)
clean_button.pack(pady=20)

# 5. Activity Log Box (Shows what happened)
log_label = tk.Label(root, text="Activity Log:", font=("Arial", 10, "bold"), bg="#f0f4f8", fg="#2d3748")
log_label.pack(anchor="w", padx=40)

log_box = tk.Text(root, height=8, width=52, font=("Consolas", 9), bg="white", fg="#2d3748", bd=1, relief="solid")
log_box.pack(pady=5)

# 6. Start the infinite visual loop to keep the window open
root.mainloop()