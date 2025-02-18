import face_recognition
import cv2
import numpy as np
import os
import threading
import queue
import time
import pickle
import signal
import sys

# Set environment variables for Qt compatibility
os.environ["QT_QPA_PLATFORM"] = "xcb"  # Force X11 backend
cv2.ocl.setUseOpenCL(False)

# Handle SIGINT for graceful shutdown
def signal_handler(sig, frame):
    print("Finalizando captura de vídeo...")
    video_capture.stop()
    video_capture.join()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Load known faces with caching

def load_known_faces(directory):
    known_encodings, known_names = [], []
    print("📂 Carregando e gerando face encodings...")

    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            name = os.path.splitext(filename)[0]
            image_path = os.path.join(directory, filename)
            pkl_path = os.path.join(directory, f"{name}.pkl")

            try:
                if os.path.exists(pkl_path):
                    with open(pkl_path, 'rb') as pkl_file:
                        encoding = pickle.load(pkl_file)
                    known_encodings.append(encoding)
                    known_names.append(name)
                    print(f"✅ Carregado: {pkl_path}")
                else:
                    # 🖼️ Carrega e Redimensiona
                    image = face_recognition.load_image_file(image_path)
                    small_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

                    # 🟢 Primeiro tenta localizar rosto
                    face_locations = face_recognition.face_locations(
                        small_image, model="hog"
                    )

                    if face_locations:
                        # Gera encoding com face detectada
                        face_encs = face_recognition.face_encodings(
                            small_image, known_face_locations=face_locations, num_jitters=5
                        )

                        if face_encs:
                            encoding = face_encs[0]
                            known_encodings.append(encoding)
                            known_names.append(name)

                            # 💾 Salva .pkl
                            with open(pkl_path, 'wb') as pkl_file:
                                pickle.dump(encoding, pkl_file)
                            print(f"💾 Gerado e salvo: {pkl_path}")
                        else:
                            print(f"⚠️ Sem encoding gerado: {image_path}")
                    else:
                        print(f"⚠️ Nenhum rosto detectado: {image_path}")

            except Exception as e:
                print(f"❌ Erro ao processar {image_path}: {e}")

    print(f"\n✅ Total de faces carregadas: {len(known_encodings)}")
    return np.array(known_encodings), known_names

class VideoCaptureThread(threading.Thread):
    def __init__(self, src=0, width=720, height=720, queue_size=2):
        super().__init__()
        self.capture = cv2.VideoCapture(src, cv2.CAP_V4L2)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.queue = queue.Queue(maxsize=queue_size)
        self.stopped = False

    def run(self):
        while not self.stopped:
            ret, frame = self.capture.read()
            if ret and not self.queue.full():
                self.queue.put(frame)
            time.sleep(0.001)

    def read(self):
        return self.queue.get() if not self.queue.empty() else None

    def stop(self):
        self.stopped = True
        self.capture.release()

if __name__ == "__main__":
    known_encodings, known_names = load_known_faces("faces")
    video_capture = VideoCaptureThread()
    video_capture.start()

    while True:
        frame = video_capture.read()
        if frame is None:
            continue
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb_small_frame)
        encodings = face_recognition.face_encodings(rgb_small_frame, locations)

        for (top, right, bottom, left), encoding in zip(locations, encodings):
            distances = np.linalg.norm(known_encodings - encoding, axis=1)
            name = "Unknown"
            if distances.size > 0 and np.min(distances) <= 0.6:
                name = known_names[np.argmin(distances)]

            top, right, bottom, left = [x * 2 for x in (top, right, bottom, left)]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.stop()
    video_capture.join()
    cv2.destroyAllWindows()