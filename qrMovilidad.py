import cv2
from pyzbar import pyzbar

def getQrCode(frame):
    barcodes = pyzbar.decode(frame)
    qrTextCode = ''
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #Get barcode
        qrTextCode = barcode.data.decode('utf-8')
        #Put rectangle on qr in frame
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        #Put text link barcode
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, qrTextCode, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #Log data qr
        #with open("barcode_result.txt", mode ='w') as file:
        #    file.write("Recognized Barcode:" + barcode_info)
        print(qrTextCode)
    return frame, qrTextCode

def main():
    #Get video webcam
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #Get frame to fame
    while ret:
        ret, frame = camera.read()
        #Convert gray
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame,qrTextCode = getQrCode(frame)
        #Show frame
        cv2.imshow('QR frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #Free webcam
    camera.release()
    cv2.destroyAllWindows()
#Launch
if __name__ == '__main__':
    main()