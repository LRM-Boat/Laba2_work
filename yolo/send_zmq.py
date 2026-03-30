#подключаем библиотеки
import zmq
import cv2
import numpy as np
from ultralytics import YOLO


def main():
    zmq_ip = "........"
    zmq_port = "...."


    model = YOLO("yolo11n.pt")

    context = zmq.Context()
    # создайте сокет типа sub
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    # Поставьте опцию, запрещающую копить старые кадры
    socket.setsockopt(...)
    socket.setsockopt(zmq.RCVTIMEO, 2000)
    socket.connect(f"tcp://{zmq_ip}:{zmq_port}")

    print(f"Connected to tcp://{zmq_ip}:{zmq_port}")

    try:
        while True:
            try:
                data = socket.recv()
            except zmq.Again:
                print("No frames received")
                continue

            print(f"Received {len(data)} bytes")

            # Декодировка сообщения
            # Допишите эту секцию, чтобы преобразовать полученные байты в numpy массив типа utf8
            nparr = np.frombuffer(...)
            # Далее деодируйте сообщение в jpeg
            frame = ...

            if frame is None:
                print("Failed to decode image")
                continue

            # YOLO inference
            results = model.predict(
                source=frame,
                conf=0.35,
                verbose=False
            )

            result = results[0]
            annotated = frame.copy()

            # Рисуем боксы вручную
            if result.boxes is not None and len(result.boxes) > 0:
                for box in result.boxes:
                    cls_id = int(box.cls.item())
                    conf = float(box.conf.item())
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    label = model.names.get(cls_id, str(cls_id))
                    text = f"{label} {conf:.2f}"

                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        annotated,
                        text,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA
                    )

            print("Frame shape:", annotated.shape)
            cv2.imshow("ZMQ Image + YOLO", annotated)

            if cv2.waitKey(1) == 27:
                break

    finally:
        cv2.destroyAllWindows()
        socket.close()
        context.term()


if __name__ == "__main__":
    main()