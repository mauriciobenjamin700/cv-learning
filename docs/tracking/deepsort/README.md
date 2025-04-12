# 🧠 Guia Completo do Algoritmo Deep SORT em Python

## 📌 O que é o Deep SORT?

**Deep SORT** é uma extensão do algoritmo **SORT** (Simple Online and Realtime Tracking). Ele melhora o desempenho do rastreamento de objetos em vídeo, usando embeddings extraídos por redes neurais profundas para associar detecções ao longo do tempo.

### Comparativo com o SORT

| Característica | SORT | Deep SORT |
|----------------|------|-----------|
| Associações    | Baseado apenas em IOU (Interseção sobre União) | Baseado em IOU + Métricas de Aparência |
| Robustez       | Menor | Maior |
| Reidentificação | Fraca | Forte (usa CNN) |

---

## 🛠️ Pré-requisitos

- Python 3.x
- NumPy
- OpenCV
- TensorFlow ou PyTorch (para rede de extração de features)
- scikit-learn (para cálculo de distância)

---

## 🧱 Estrutura do Deep SORT

1. **Detecção de Objetos**
   - Pode ser YOLO, SSD, Faster R-CNN, etc.

2. **Extração de Features**
   - Um modelo treinado (como ResNet) gera embeddings das detecções.

3. **Rastreamento Kalman Filter**
   - Estima as posições futuras dos objetos com base nas detecções anteriores.

4. **Associação via Hungarian Algorithm**
   - Usa uma combinação de distância IOU e distância de embeddings para associar detecções com rastros.

---

## 📦 Instalação

Você pode clonar uma das implementações populares:

```bash
git clone https://github.com/nwojke/deep_sort.git
cd deep_sort
pip install -r requirements.txt
```

Ou use uma versão mais integrada com detecção:

```bash
git clone https://github.com/ZQPei/deep_sort_pytorch.git
cd deep_sort_pytorch
pip install -r requirements.txt
```

---

## 🔄 Fluxo de Funcionamento

```python
# 1. Detectar objetos no frame
detections = detector.detect(frame)

# 2. Extrair embeddings
features = encoder(frame, detections)

# 3. Criar lista de detecções com bbox + scores + features
detection_list = [
    Detection(bbox, score, feature)
    for bbox, score, feature in zip(detections, scores, features)
]

# 4. Atualizar o rastreador
tracker.predict()
tracker.update(detection_list)

# 5. Obter os rastros ativos
for track in tracker.tracks:
    if track.is_confirmed() and track.time_since_update == 0:
        draw_box(track.to_tlbr(), track.track_id)
```

---

## 🔎 Detalhes Importantes

### Kalman Filter

Usado para prever a próxima posição de um objeto, mesmo que ele não tenha sido detectado por um frame.

### Hungarian Algorithm

Resolve o problema de associação de forma ótima, minimizando a distância combinada entre detecções e rastros.

### Embeddings

Uma rede neural (por exemplo, MobileNet ou ResNet) é usada para criar uma "assinatura" única de cada objeto.

---

## 📚 Recursos Recomendados

- [Deep SORT Original Paper](https://arxiv.org/abs/1703.07402)
- [Implementação em PyTorch](https://github.com/ZQPei/deep_sort_pytorch)
- [YOLO + Deep SORT](https://github.com/theAIGuysCode/yolov4-deepsort)


## 🛠️ Pré-requisitos com YOLOV11

- Python 3.x
- Bibliotecas: `ultralytics`, `opencv-python`, `deep_sort_realtime`
- GPU com CUDA (opcional, mas recomendado para desempenho em tempo real)

Instale as dependências necessárias:

```bash
pip install ultralytics opencv-python deep_sort_realtime
```

---

## 📦 Estrutura do Projeto

```
project/
├── main.py
├── video.mp4
```

---

## 📝 Código de Integração

```python
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
```

---

## 🎯 Resultado Esperado

- Detecção de objetos com **YOLOv11**.
- Rastreamento contínuo dos objetos com IDs únicos utilizando **Deep SORT**.
- Visualização em tempo real com caixas delimitadoras e IDs sobrepostos.

---

## 📚 Recursos Adicionais

- [Documentação oficial do YOLOv11](https://docs.ultralytics.com/models/yolo11/)
- [Repositório do Deep SORT com suporte a YOLO](https://github.com/xuarehere/yolo_series_deepsort_pytorch)

---

Se desejar, posso auxiliar na adaptação desse código para utilizar sua câmera ao vivo ou para processar múltiplos vídeos simultaneamente. Gostaria de prosseguir com alguma dessas opções?
