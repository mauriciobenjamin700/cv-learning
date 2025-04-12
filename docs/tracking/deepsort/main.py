from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

# Inicializa o modelo YOLOv11
model = YOLO('yolo11n.pt')  # Substitua pelo modelo desejado

# Inicializa o Deep SORT
tracker = DeepSort(max_age=30)

# Captura de vídeo
cap = cv2.VideoCapture('video.mp4')  # Substitua pelo caminho do seu vídeo

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecção com YOLOv11
    results = model(frame)
    detections = results[0].boxes.data.cpu().numpy()

    # Lista para armazenar detecções formatadas
    dets = []
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        dets.append(([int(x1), int(y1), int(x2 - x1), int(y2 - y1)], conf, int(cls)))

    # Rastreamento com Deep SORT
    tracks = tracker.update_tracks(dets, frame=frame)

    # Desenha as caixas delimitadoras e IDs
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        x1, y1, x2, y2 = map(int, ltrb)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('YOLOv11 + Deep SORT', frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()