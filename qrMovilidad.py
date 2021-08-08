import cv2
from pyzbar import pyzbar
#import urllib3
import mechanize


def getQrCode(frame):
    barcodes = pyzbar.decode(frame)
    qrTextCode = ''
    for barcode in barcodes:
        #x, y , w, h = barcode.rect
        #Get barcode
        qrTextCode = barcode.data.decode('utf-8')
        #Put rectangle on qr in frame
        #cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        #Put text link barcode
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, qrTextCode, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #Log data qr
        #with open("barcode_result.txt", mode ='w') as file:
        #    file.write("Recognized Barcode:" + barcode_info)
        #print(qrTextCode)
    return frame, qrTextCode

def navegate(url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options

    #options = Options()
    #options.headless = True

    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get(url)
    #WebDriverWait(self.drver, 50).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Sign Up')]")))

    try:
        element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//b[contains(text(),'Pase de movilidad HABILITADO')]"))
        )
        if(element.text != ''):
            print(element.text)
            #driver.quit()
            #return element.text
        import time
        time.sleep(5)
        driver.quit()
    except Exception as e:
        print("timepo limite")
    finally:
        driver.quit()


def getPage(url):
    # https://us-central1-scanner-mevacuno.cloudfunctions.net/neogcscanner post {data: {a: "129235417", b: "1621486677", c: "0"}}
    #http = urllib3.PoolManager()
    #r = http.request('GET', url)
    #print(r.data.decode('utf-8'))
    target_url='https://us-central1-scanner-mevacuno.cloudfunctions.net/neogcscanner'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    resp = br.open(url)
    for link in br.links():
        print(link)
        print(link.url)
        # http://www.rfc-editor.org/rfc/rfc2606.txt
        if link.url == target_url:
            print('match found')
            # match found            
            break
    print(resp.info())  # headers
    print(resp.read().decode('utf-8')) # content

def main():
    #Get video webcam
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #Get frame to fame
    while ret:
        ret, frame = camera.read()
        #Convert gray and remove noise
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.bilateralFilter(frame, 11, 17, 17)
        #frame = cv2.GaussianBlur(frame, (3, 3), 0)

        frame,qrTextCode = getQrCode(frame)
        if(qrTextCode!=''):
            #getPage(qrTextCode)
            #qrTextCode = 'https://scanmevacuno.gob.cl/?a=129235417&b=1621486688&c=0'
            navegate(qrTextCode)
            #break
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