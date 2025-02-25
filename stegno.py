import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def embed_message():
    global img
    msg = entry_message.get()
    password = entry_password.get()

    if not msg or not password:
        messagebox.showerror("Error", "Please enter both a message and a passcode!")
        return

    if len(msg) * 3 > img.size:
        messagebox.showerror("Error", "Message too long to fit in the image!")
        return

    m, n, z = 0, 0, 0
    for char in msg:
        img[n, m, z] = ord(char)
        n += 1
        m += 1
        z = (z + 1) % 3
    encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if encrypted_image_path:
        cv2.imwrite(encrypted_image_path, img)
        messagebox.showinfo("Success", f"Message embedded successfully! Encrypted image saved as {encrypted_image_path}")

def decrypt_message():
    global img
    pas = entry_decrypt_password.get()

    if not pas:
        messagebox.showerror("Error", "Please enter the passcode for decryption!")
        return

    if pas != entry_password.get():
        messagebox.showerror("Error", "YOU ARE NOT AUTHORIZED!")
        return

    m, n, z = 0, 0, 0
    decrypted_message = ""
    for _ in range(len(entry_message.get())):
        decrypted_message += chr(img[n, m, z])
        n += 1
        m += 1
        z = (z + 1) % 3

    messagebox.showinfo("Decrypted Message", f"Decrypted message: {decrypted_message}")

def load_image():
    global img, img_display
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Failed to load the image!")
            return

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_pil.thumbnail((300, 300))
        img_display = ImageTk.PhotoImage(img_pil)
        label_image.config(image=img_display)
        label_image.image = img_display

root = tk.Tk()
root.title("Image Steganography")
root.geometry("400x500")

button_load = tk.Button(root, text="Load Image", command=load_image)
button_load.pack(pady=10)

label_image = tk.Label(root)
label_image.pack()

label_message = tk.Label(root, text="Enter Secret Message:")
label_message.pack(pady=5)
entry_message = tk.Entry(root, width=40)
entry_message.pack()

label_password = tk.Label(root, text="Enter Passcode:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, width=40, show="*")
entry_password.pack()

button_embed = tk.Button(root, text="Embed Message", command=embed_message)
button_embed.pack(pady=10)

label_decrypt_password = tk.Label(root, text="Enter Passcode for Decryption:")
label_decrypt_password.pack(pady=5)
entry_decrypt_password = tk.Entry(root, width=40, show="*")
entry_decrypt_password.pack()

button_decrypt = tk.Button(root, text="Decrypt Message", command=decrypt_message)
button_decrypt.pack(pady=10)

root.mainloop()