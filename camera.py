import base64
import cv2
import config


def detect_face_and_save_image():
    count = 0
    #  30 karede 1 kez resim al
    frame_pass_count = 30
    detected_faces_list: list = []
    # Haarcascades dosyasını yükleyin (daha fazla model: https://github.com/opencv/opencv/tree/master/data/haarcascades)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Kamera bağlantısını açın (0 varsayılan kamera)
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(config.TEST_VIDEO_SOURCE) if config else cv2.VideoCapture(0)
    # cap.set()
    # kaynakdan görüntü yakalnadığı sürece devam et
    while cap:
        # Kameradan kare al
        ret, frame = cap.read()
        if config.BROWSER.is_stop() or not ret:
            print("aldım")
            print(ret)
            print(config.BROWSER.is_stop)
            break

        # frame = cv2.resize(frame, (1920 , 1080 ))
        frame = cv2.resize(frame, (1920 // 2, 1080 // 2))

        # Gri tonlamaya dönüştür (yüz tespiti daha hızlı yapılır)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # Yüzleri tespit et
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        # frame_count

        count += 1
        # yüz var ise ve 30 farem atlanmış ise
        if len(faces) > 0 and not (count % frame_pass_count):

            # Tespit edilen her yüz için Aksiyon Al
            (x, y, w, h) = faces[0]
            # eğer debug açık sa kamera ekran da görünsün ve yüzler çerçeveye alsın
            # değilse ssadece yüz tespit edip görüntü yakalasın
            # if config.DEBUG:
            # Yüzü çevreleyen dikdörtgen çizin
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Ekrana yüz tespit edildiğine dair mesaj yazdırın
            cv2.putText(frame, 'Yuz Tespit Edildi!', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (152, 64, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame[y:y + h, x:x + w])

            if config.DEBUG:
                face = cv2.resize(frame, (1920 // 6, 1080 // 6))
                cv2.imshow(f'face count {count}', face)
            else:
                base64_image = base64.b64encode(buffer).decode('utf-8')
                detected_faces_list.append(base64_image)
                # veri tabanı yazma işlemi eklenicek
        # for ((x, y, w, h), index) in zip(faces, range(len(faces))):
        #     # eğer debug açık sa kamera ekran da görünsün ve yüzler çerçeveye alsın
        #     # değilse ssadece yüz tespit edip görüntü yakalasın
        #     # if config.DEBUG:
        #     # Yüzü çevreleyen dikdörtgen çizin
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #
        #     # Ekrana yüz tespit edildiğine dair mesaj yazdırın
        #     cv2.putText(frame, 'Yuz Tespit Edildi!', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        #
        #     _, buffer = cv2.imencode('.jpg', frame[y:y + h, x:x + w])
        #
        #     if config.DEBUG:
        #         face = cv2.resize(frame, (1920 // 6, 1080 // 6))
        #         cv2.imshow(f'image {index}', face)
        #     else:
        #         base64_image = base64.b64encode(buffer).decode('utf-8')
        #         detected_faces_list.append(base64_image)
        #         # veri tabanı yazma işlemi eklenicek

        if config.DEBUG:
            cv2.imshow('test-face-detected', frame)

        # 'q' tuşuna basarak uygulamadan çıkın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("cam yok")
    # Kamera bağlantısını ve pencereyi kapatın
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    return detected_faces_list


if __name__ == "__main__":
    detect_face_and_save_image()
