from tkinter import *
from tkinter import messagebox as mb
from PIL import Image

def generate_data(pixels, data):
    data_in_binary = [format(ord(i), '08b') for i in data]
    image_data = iter(pixels)

    for binary_char in data_in_binary:
        pixels = list(next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3])

        for b in range(8):
            if binary_char[b] == '1':
                pixels[b] |= 1  # Ensure LSB is 1  
            else:
                pixels[b] &= ~1  # Ensure LSB is 0  

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])


def encryption(img, data):
    size = img.size[0]
    (x, y) = (0, 0)

    data_in_binary = [format(ord(i), '08b') for i in data]  # Convert text to binary  
    data_length = len(data_in_binary)
    image_data = iter(img.getdata())

    for a in range(data_length):
        # Extract the next 9 pixels  
        pixels = list(next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3])

        for b in range(8):  
            if data_in_binary[a][b] == '1':
                pixels[b] = pixels[b] | 1  # Ensure the bit is 1  
            else:
                pixels[b] = pixels[b] & ~1  # Ensure the bit is 0  

        # Mark end of message using LSB of last pixel  
        if a == data_length - 1:
            pixels[-1] = pixels[-1] | 1  # Set last pixel to odd for termination  
        else:
            pixels[-1] = pixels[-1] & ~1  # Keep it even otherwise  

        # Save modified pixels  
        img.putpixel((x, y), tuple(pixels[:3]))
        img.putpixel((x+1, y), tuple(pixels[3:6]))
        img.putpixel((x+2, y), tuple(pixels[6:9]))

        # Move to the next pixel position  
        x += 3  
        if x >= size:
            x = 0
            y += 1

def main_encryption(img, text, new_image_name):
    if not img or not text or not new_image_name:
        mb.showerror("Error", "All fields must be filled!")
        return

    image = Image.open(img).convert("RGB")  # Ensure RGB mode
    new_image = image.copy()

    encryption(new_image, text)  # Call the corrected encryption function

    new_image_name += ".png"
    new_image.save(new_image_name, "PNG")
    mb.showinfo("Success", "Image successfully encoded and saved as " + new_image_name)


def main_decryption(img, strvar):
    image = Image.open(img).convert("RGB")
    image_data = iter(image.getdata())

    data = ""
    while True:
        try:
            pixels = list(next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3])
            binary_string = "".join(['0' if i % 2 == 0 else '1' for i in pixels[:8]])

            data += chr(int(binary_string, 2))

            # Stop decoding if the last pixel’s LSB is 1
            if pixels[-1] % 2 != 0:
                break
        except StopIteration:
            break

    print("Decoded message:", data)  # Debugging print
    strvar.set(data)  # Update UI




def encode_image():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='AntiqueWhite')

    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='AntiqueWhite').place(x=220, rely=0)

    Label(encode_wn, text='Image Path:', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=50)
    Label(encode_wn, text='Data to Encode:', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=90)
    Label(encode_wn, text='Output File Name:', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=50)

    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=90)

    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=130)

    Button(encode_wn, text='Encode', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
    main_encryption(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(x=220, y=175)

def decode_image():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='Bisque')

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='Bisque').place(x=220, rely=0)

    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12),
          bg='Bisque').place(x=10, y=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(x=350, y=50)

    text_strvar = StringVar()

    def decode_and_show():
        img_path = img_entry.get()
        if not img_path:
            mb.showerror("Error", "Please enter a valid image path.")
            return

        main_decryption(img_path, text_strvar)

        # Debugging print
        print("Decoded message:", text_strvar.get())

        # Enable the Entry field and insert the text
        text_entry.config(state='normal')
        text_entry.delete(0, END)
        text_entry.insert(0, text_strvar.get())
        text_entry.config(state='disabled')  # Make it read-only again

    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=decode_and_show).place(x=220, y=90)

    Label(decode_wn, text='Decoded Text:', font=("Times New Roman", 12), bg='Bisque').place(x=180, y=130)

    # Text entry should now update properly
    text_entry = Entry(decode_wn, width=94, textvariable=text_strvar, state='disabled')
    text_entry.place(x=15, y=160, height=100)



root = Tk()
root.title('Image Steganography')
root.geometry('300x200')
root.resizable(0, 0)
root.config(bg='NavajoWhite')

Label(root, text='Image Steganography', font=('Comic Sans MS', 15), bg='NavajoWhite').place(x=40, y=0)
Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=encode_image).place(x=30, y=80)
Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=decode_image).place(x=30, y=130)

root.mainloop()
