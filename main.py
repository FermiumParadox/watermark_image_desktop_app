import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageTk

# create window
root = tk.Tk()
# window title
root.title("Watermark App")
# window size
root.geometry("500x400")

# Grid layout setup
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.rowconfigure(0, weight=6)  # image
root.rowconfigure(1, weight=0)  # entry
root.rowconfigure(2, weight=0)  # buttons


# label to show selected image
image_frame = tk.Frame(root, bd=2, relief="groove")
image_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
image_label = tk.Label(image_frame, text="No Image Selected")
image_label.pack(expand=True)

# create watermark
watermark_entry = tk.Entry(root, width=30)
watermark_entry.grid(row=1, column=0, columnspan=2, pady=2)
watermark_entry.insert(0, "Enter watermark text...")
watermark_entry.config(fg="gray")

# upload button
upload_btn = tk.Button(root, text="Upload Image")
upload_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

# save button
save_btn = tk.Button(root, text="Save Image")
save_btn.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

# create a function to handle upload button action
image_path = ""
def upload_image():
    global image_path, tk_image

    file = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png *.jpeg")]
    )

    if file:
        image_path = file
        print("Selected:", image_path)

        # Open image
        image = Image.open(image_path)


        # Resize image (so it fits in window)
        max_width = 300
        max_height = 300
        image.thumbnail((max_width, max_height), Image.LANCZOS)

        # Convert to Tkinter format
        tk_image = ImageTk.PhotoImage(image)

        # Show in label
        image_label.config(image=tk_image)


# create a function to create a watermark and add the save button action
def add_watermark():
    if not image_path:
        print("No image selected")
        return

    text = watermark_entry.get()

    if text == "Enter watermark text...":
        print("Enter valid text")
        return

    image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)

    # dynamic text position
    width, height = image.size
    max_width = width - 20

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    # Draw lines from bottom
    y_offset = height - 10

    for line in reversed(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = width - text_width - 10
        y_offset -= text_height

        draw.text((x, y_offset), line, font=font, fill=(255, 255, 255, 100))

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile="watermarked_image.png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        image = Image.alpha_composite(image, overlay)
        image.save(file_path)
        print("Saved to:", file_path)

    print("Saved!")

def preview_watermark(event=None):
    global tk_image

    if not image_path:
        print("No image selected")
        return

    text = watermark_entry.get()

    if text == "Enter watermark text...":
        return

    image = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)

    # dynamic text position
    width, height = image.size
    max_width = width - 20

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    # Draw lines from bottom
    y_offset = height - 10

    for line in reversed(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = width - text_width - 10
        y_offset -= text_height

        draw.text((x, y_offset), line, font=font, fill=(255, 255, 255, 100))

    image = Image.alpha_composite(image, overlay)
    image.thumbnail((300, 300), Image.LANCZOS)

    tk_image = ImageTk.PhotoImage(image)

    image_label.config(image=tk_image)
    image_label.image = tk_image

# add action to the buttons click through command
upload_btn.config(command=upload_image)
save_btn.config(command=add_watermark)

def on_entry_click(event):
    if watermark_entry.get() == "Enter watermark text...":
        watermark_entry.delete(0, tk.END)
        watermark_entry.config(fg="black")

def on_focus_out(event):
    if watermark_entry.get() == "":
        watermark_entry.insert(0, "Enter watermark text...")
        watermark_entry.config(fg="gray")

watermark_entry.bind("<FocusIn>", on_entry_click)
watermark_entry.bind("<FocusOut>", on_focus_out)
watermark_entry.bind("<Return>", preview_watermark)

root.mainloop()