import cv2
import config

def detect_face_and_save_image():
    # Haarcascades dosyasını yükleyin (daha fazla model: https://github.com/opencv/opencv/tree/master/data/haarcascades)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Kamera bağlantısını açın (0 varsayılan kamera)
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(config.TEST_VIDEO_SOURCE) if config else cv2.VideoCapture(0)

    # kaynakdan görüntü yakalnadığı sürece devam et
    while cap:
        # Kameradan kare al
        ret, frame = cap.read()

        # Gri tonlamaya dönüştür (yüz tespiti daha hızlı yapılır)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüzleri tespit et
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Tespit edilen her yüz için Aksiyon Al
        for (x, y, w, h) in faces:
            # eğer debug açık sa kamera ekran da görünsün ve yüzler çerçeveye alsın
            # değilse ssadece yüz tespit edip görüntü yakalasın
            if config.DEBUG:
                # Yüzü çevreleyen dikdörtgen çizin
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Ekrana yüz tespit edildiğine dair mesaj yazdırın
                cv2.putText(frame, 'Yuz Tespit Edildi!', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # _, buffer = cv2.imencode('.jpg', frame[y:y + h, x:x + w])
            # base64_image = base64.b64encode(buffer).decode('utf-8')

            # Yüzü içeren bölgeyi kaydedin
            # face_roi = frame[y:y+h, x:x+w]
            # cv2.imwrite('yuz_resmi.png', frame)
            print('face dedected')
        # Çerçeveyi göster
        # cv2.imshow('Yuz Tespiti Uygulamasi', frame)

        # 'q' tuşuna basarak uygulamadan çıkın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("cam yok")
    # Kamera bağlantısını ve pencereyi kapatın
    if cap:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_face_and_save_image()
