# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Signifigant Bit (LSB) encoding.

from PIL import Image
import os

def encode(img, msg):
  pixels = img.load()
  width, height = img.size
  letterSpot = 0
  pixel = 0
  letterBinary = ""
  msgLength = len(msg)
  red, green, blue = pixels[0, 0]
  pixels[0,0] = (msgLength, green, blue)

  for i in range(msgLength * 3):
    x = i % width
    y = i // width

    red, green, blue = pixels[x, y]
    redBinary = numberToBinary(red)
    greenBinary = numberToBinary(green)
    blueBinary = numberToBinary(blue)

    if pixel % 3 == 0:
      letterBinary = numberToBinary(ord(msg[letterSpot]))
      greenBinary = greenBinary[0:7] + letterBinary[0]
      blueBinary = blueBinary[0:7] + letterBinary[1]

    elif pixel % 3 == 1:
      redBinary = redBinary[0:7] + letterBinary[2]
      greenBinary = greenBinary[0:7] + letterBinary[3]
      blueBinary = blueBinary[0:7] + letterBinary[4]

    else:
      redBinary = redBinary[0:7] + letterBinary[5]
      greenBinary = greenBinary[0:7] + letterBinary[6]
      blueBinary = blueBinary[0:7] + letterBinary[7]

      letterSpot = letterSpot + 1

    red = binaryToNumber(redBinary)
    blue = binaryToNumber(blueBinary)
    green = binaryToNumber(greenBinary)

    pixels[x,y] = (red, green, blue)
    pixel = pixel + 1

  img.save("secretImg.png", 'png')


def decode(img):
    """Takes the image file and reads the least significant bit from the RGBA channels.
    Converts that binary to decimal to ASCII."""
    msg = ""

    pixels = img.load()
    red, green, blue = pixels[0, 0]
    msgLength = red
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    x = 0
    y = 0

    while len(msg) < msgLength:
        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]

        elif pixel % 3 == 1:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]

        else:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]
            letterAscii = binaryToNumber(letterBinary)
            letter = chr(letterAscii)
            msg = msg + letter

        pixel = pixel + 1
        x = pixel % width
        y = pixel // width

    return msg


def numberToBinary(num):
    """Takes a base10 number and converts to a binary string with 8 bits"""
    binary = bin(num)[2:]
    return binary.zfill(8)
    return binary


def binaryToNumber(bin):
    """Takes a string binary value and converts it to a base10 integer."""
    return int(bin, 2)
    return decimal


def main():
    choice = input("Would you like to encode or decode? ").strip().lower()
    fileName = input("Enter the image filename (must be PNG): ").strip()
    img = Image.open(fileName)

    if choice == 'encode':
        message = input("Enter the message you want to hide: ")
        encode(img, message)
        print("Message encoded and saved as secretImg.png.")
    elif choice == 'decode':
        secret = decode(img)
        print("Decoded message:", secret)
    else:
        print("Invalid option. Please choose 'encode' or 'decode'.")

    img.close()

"""
  yourImg = Image.open('secretImg.png')
  msg = decode(yourImg)
  print(msg)
  """
    
if __name__ == '__main__':
  main()