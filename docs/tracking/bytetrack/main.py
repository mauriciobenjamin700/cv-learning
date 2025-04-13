import cv2
from ultralytics import YOLO

# Carregar o modelo YOLOv11
model = YOLO("yolo11n.pt")  # Substitua pelo caminho do seu modelo, se necessário

# Abrir o vídeo
video_path = "video.mp4"  # Substitua pelo caminho do seu vídeo
cap = cv2.VideoCapture(video_path)

# Verificar se o vídeo foi aberto corretamente
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Loop para processar cada frame do vídeo
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar rastreamento com ByteTrack
    results = model.track(
        source=frame,
        persist=True,
        conf=0.3,
        iou=0.5,
        tracker="bytetrack.yaml",
        show=False
    )

    # Anotar o frame com as detecções e IDs de rastreamento
    annotated_frame = results[0].plot()

    # Exibir o frame anotado
    cv2.imshow("YOLOv11 + ByteTrack", annotated_frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
cap.release()
cv2.destroyAllWindows()
