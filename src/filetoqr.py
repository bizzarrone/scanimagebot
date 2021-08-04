#!/usr/bin/env python3.7
"""
 filetoqr Bot
 31 Luglio 2021: bot created (Luca Carrozza)
 01 Agosto 2021: encode and decode options
 02 Agosto 2021: watermark (0.6), stats (0.7)
 03 Agosto 2021: added filename inside the QR (0.8)
 04 Agosto 2021: fixed filename and extension, added pages in header
"""
from pyzbar.pyzbar import decode
import io, os, time, string, math
import telepot
import cv2
import numpy as np
import base64
from PIL import Image, ImageDraw, ImageFont
encoded=0
decoded=0

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def read_stat():
 global encoded, decoded
 print ("Statistics:")
 f = open("stats.txt", "r+")
 encoded = int(f.readline())
 decoded = int(f.readline())
 print ("Encoded : "+str(encoded)+"\nDecoded : "+str(decoded))
 f.close()
 
def write_stat():
 f = open("stats.txt", "w")
 f.write(str(encoded)+"\n")
 f.write(str(decoded))
 f.close()

def write_header(text,fname):
 f = open(fname, "w")
 f.write(text+"\n")
 f.close()

def add_watermark(text,npage,totpage,filename,outputfilename):
    #Create an Image Object from an Image
    im = Image.open(filename)
    width, height = im.size
    draw = ImageDraw.Draw(im)
    #text = "sample watermark"
    font = ImageFont.truetype('FreeMono.ttf', 12)
    textwidth, textheight = draw.textsize("filename: "+text, font)
    margin = 0
    x = 34
    y = height - textheight - margin
    draw.text((x, y), text, font=font)

    text2="Image "+npage+"/"+totpage+" - QR generated by @Filetoqr_bot"
    textwidth, textheight = draw.textsize(text2, font)
    margin = 0
    x = 34
    y = 0
    draw.text((x, y), text2, font=font)
    #im.show()
    #Save watermarked image
    im.save(outputfilename)


__version__ = '0.9c'

print ("Started bot file2qr by Luca version "+__version__)

def on_chat_message(msg):
    global encoded, decoded
    path_encode="../files-encode/"
    path_decoded="../files-decoded/"
    path_qr_encoded="../qr-encoded/"
    path_qr_decode="../qr-decode/"
    content_type, chat_type, chat_id = telepot.glance(msg)
    name_id = msg["from"]["first_name"]+"-"+str(msg["from"]["id"])


    # DECODE ############ Receiving a photo, supposed it is a QR and the deooded and sent it back
    if content_type == 'photo':
        filename=path_qr_encoded+name_id+".png"
        filenamedecoded=path_decoded+name_id+"-decoded.bin"
        FILE2QR.download_file(msg['photo'][-1]['file_id'], filename)
        print ("QR image saved as ",filename)
        #FILE2QR.sendMessage(chat_id, "Image saved as "+filename)
        os.system("zbarimg --raw "+filename+" | base64 -d > "+filenamedecoded)
        f = open( filenamedecoded, 'rb')
        header = f.readline()
        header2=str(header.decode('ascii'))
        print ("header: "+str(header))
        print ("header2:"+header2)
        if header2[0:4]=="#QR#":
            print ("it is a qr2file code."+header2)
            originalfilename=header2[10:len(header2)-2]
            print("original filename: "+originalfilename)
            #sed '1d' file.txt > tmpfile
            os.system("sed '1d' "+filenamedecoded+" > "+path_decoded+originalfilename)
            ff = open( path_decoded+originalfilename, 'rb')
            FILE2QR.sendDocument(chat_id, ff, "Here your file decoded.")
            decoded+=1
            write_stat()
        else:
            FILE2QR.sendMessage(chat_id, "Your QR image was not generated by file2qr bot (header missing) or not QR recognized.")
            print("QR code not for FILE2QR or not recognized")


    # ENCODE ################## receiving a document, it is converted into a QR    
    if content_type == 'document':
        filenamereceived=path_encode+name_id+".bin"
        #FILE2QR.download_file(msg['document'][-1]['file_id'], filename)
        file_id = msg['document']['file_id']
        filename = msg['document']['file_name']
        filenamenospaces = filename.replace(' ', '')
        #ext = os.path.splitext(filenamenospaces)[-1].lower()
        original_filename, ext = os.path.splitext(filenamenospaces)
        l=len(filenamenospaces)
        if l>16:
            l2=16
        else:
            l2=l
        filenameshort=original_filename[0:l2]+ext
        print ("filename shorted "+filenameshort)
        filenameencoded=path_encode+name_id+"-encoded.png"
        filenameencodedwm=path_encode+name_id+"-wm-encoded.png"
        fname_header=path_encode+name_id+"_head"
        npage="01"
        totpage="01"
        text_header="#QR#"+npage+"/"+totpage+"#"+filenameshort+"#"
        write_header(text_header,fname_header)
        #FILE2QR.sendMessage(chat_id, "File saved as "+filename)
        FILE2QR.download_file(file_id, filenamereceived)
        print ("File saved as ",filenamereceived)
        """
        message = "Python is fun"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        print(base64_message)
        """
        max_size=2184
        size=os.path.getsize(filenamereceived)
        if (size>max_size) :
            nqr=int (round_up (size/max_size))
            print ("File too big. In future it will split into "+str(nqr)+" QR images.")
            FILE2QR.sendMessage(chat_id, "Your file is too big.\nMax size is 2184 bytes.\nPlease, wait for the next version.\nIn future it will split into "+str(nqr)+" QR images.")
        else :  
            #os.system("echo #QR#"+filenameshort+"#'';`base64 "+filenamereceived+"` |  qrencode -8 -l L  -o "+filenameencoded) 
            filenamereceived2=filenamereceived+".head"
            os.system("cat "+fname_header+" "+filenamereceived +" > "+filenamereceived2)
            os.system("base64 "+filenamereceived2+" |  qrencode -8 -l L  -o "+filenameencoded)
            npage=1
            totpage=1
            add_watermark(filenameshort,str(npage),str(totpage),filenameencoded,filenameencodedwm)
            f = open( filenameencodedwm, 'rb')
            FILE2QR.sendPhoto(chat_id,f)
            encoded+=1
            write_stat()

    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = msg['text']

        if txt.startswith('/stats'):
            read_stat()
            FILE2QR.sendMessage(chat_id, "Stats:\nEncoded: "+str(encoded)+"\nDecoded: "+str(decoded))

        elif txt.startswith('/info'):
                print ("Info")
                message = 'Hello %s!\nI am a bot to convert a binary file into QR code and viceversa.\nJust send me a binary file and I will convert it into QR images.\nSend me a QR code image and I will decode it into the original binary file.\nCurrent maximum file size is 2184 Bytes.\nBigger size in next release.\nAny suggestions are welcome. Contact the developer: bizzarrone@gmail.com'
                message = message + '\nVersion %s '
                message = message % (name, __version__)
                FILE2QR.sendMessage(chat_id, message)


if __name__ == '__main__':
    read_stat()
    TOKEN = os.environ.get('BOT_TOKEN')
    FILE2QR = telepot.Bot(TOKEN)
    FILE2QR.message_loop(on_chat_message)

    while True:
        time.sleep(10)