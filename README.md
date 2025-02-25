# Secure-data-hiding-in-image-using-steganography

Overview
This project implements Image Steganography using the Least Significant Bit (LSB) algorithm to securely hide text data inside an image. The system allows users to encode and decode messages within images without altering their appearance, providing a safe and invisible method of data transmission.

Features
Encode Secret Messages: Hide text inside an image without visible changes.
Decode Messages: Extract hidden messages from encoded images.
User-Friendly GUI: Built using Tkinter for a simple and intuitive experience.
Supports PNG & JPEG Images: Works with common image formats.
100% Accurate Retrieval: Ensures no data loss during encoding and decoding.

Technologies Used
Python: Core programming language.
Tkinter: For building the graphical user interface (GUI).
PIL (Pillow): For image processing and pixel manipulation.
Least Significant Bit (LSB) Algorithm: For embedding secret data into images.

Installation
1.Clone the Repository
git clone https://github.com/your-repo/image-steganography.git
cd image-steganography

2.Install Dependencies
pip install pillow

3.Run the Application
python app1.py

Usage
1.Encoding a Message:
Open the application.
Enter the path of the image file.
Input the text to hide.
Provide an output filename.
Click "Encode the Image" to save the steganographic image.

2.Decoding a Message:
Open the application.
Enter the path of the encoded image.
Click "Decode the Image" to reveal the hidden text.

Expected Output
The encoded image appears visually unchanged.
The original message is extracted correctly from the encoded image.

Future Enhancements
Add encryption before embedding for an extra layer of security.
Expand to audio and video steganography.
Create a web and mobile version for cross-platform accessibility.
