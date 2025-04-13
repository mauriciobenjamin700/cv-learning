# 🎯 Requisitos

Antes de executar o script, certifique-se de instalar as bibliotecas necessárias:

```bash
pip install ultralytics opencv-python
```

---

## 📄 Script: Rastreamento com YOLOv11 + ByteTrack

```python
import cv2
from ultralytics import YOLO

# Carregar o modelo YOLOv11
model = YOLO("yolo11n.pt")  # Substitua pelo caminho do seu modelo, se necessário

# Abrir o vídeo
video_path = "seu_video.mp4"  # Substitua pelo caminho do seu vídeo
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
```

---

## 🔧 Explicação dos Parâmetros

- `persist=True`: Mantém os IDs de rastreamento entre os frames.
- `conf=0.3`: Define o limiar de confiança para as detecções.
- `iou=0.5`: Define o limiar de IoU (Intersection over Union) para associação de detecções.
- `tracker="bytetrack.yaml"`: Especifica o uso do ByteTrack como algoritmo de rastreamento.

---

## 📁 Observações

- Certifique-se de que o arquivo `bytetrack.yaml` esteja disponível no diretório de configuração da biblioteca Ultralytics. Caso contrário, você pode encontrá-lo no repositório oficial da Ultralytics ou criar um personalizado conforme suas necessidades.
- O modelo `yolo11n.pt` é utilizado como exemplo. Você pode substituí-lo por outro modelo YOLOv11 treinado conforme sua aplicação específica.
