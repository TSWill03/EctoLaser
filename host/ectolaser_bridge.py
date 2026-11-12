"""
EctoLaser | POC fotografia -> deteccao YOLO -> LED de status no Arduino UNO.
O LED indica um candidato; NENHUM mecanismo de eliminacao e controlado.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

TARGET_CLASS = "cluster_larvas_pasto"
DEFAULT_THRESHOLD = 0.65


def focus_found(predictions, threshold=DEFAULT_THRESHOLD):
    """predictions: iteravel de (nome_da_classe, confianca)."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Confidence threshold must be between 0 and 1")
    return any(
        name == TARGET_CLASS and float(conf) >= threshold
        for name, conf in predictions
    )


def command_for_predictions(predictions, threshold=DEFAULT_THRESHOLD):
    """Comando para indicador LED, jamais para ferramenta de controle fisico."""
    return "INDICATE" if focus_found(predictions, threshold) else "CLEAR"


def send_to_arduino(port: str, command: str) -> str:
    if command not in {"INDICATE", "CLEAR", "PING"}:
        raise ValueError("Unsupported serial command")
    try:
        import serial
    except ImportError as exc:
        raise RuntimeError("Install pyserial: python -m pip install pyserial") from exc

    # Ao abrir a serial, o UNO R3 normalmente reinicia. Esperamos o boot.
    with serial.Serial(port, 115200, timeout=2, write_timeout=2) as conn:
        time.sleep(2.0)
        conn.reset_input_buffer()
        conn.write((command + "\n").encode("ascii"))
        conn.flush()
        reply = conn.readline().decode("ascii", errors="replace").strip()
        expected = "PONG" if command == "PING" else "OK"
        if reply != expected:
            raise RuntimeError(f"Arduino response not expected: {reply!r}")
        return reply


def run_photo(image_path: str, weights_path: str, threshold: float, output: str):
    try:
        import cv2
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError(
            "Install dependencies from requirements-host.txt"
        ) from exc

    if not Path(weights_path).is_file():
        raise FileNotFoundError(weights_path)
    photo = cv2.imread(image_path)
    if photo is None:
        raise FileNotFoundError(image_path)

    detector = YOLO(weights_path)
    names = detector.names
    available_classes = {
        str(label) for label in
        (names.values() if isinstance(names, dict) else names)
    }
    if TARGET_CLASS not in available_classes:
        raise ValueError(
            f"Model does not provide required class: {TARGET_CLASS}. "
            "Do not use default COCO or weed-detection weights."
        )

    result = detector.predict(source=photo, conf=threshold, verbose=False)[0]
    detections = []

    if result.boxes is not None:
        for box in result.boxes:
            label = str(result.names[int(box.cls[0].item())])
            conf = float(box.conf[0].item())
            if label != TARGET_CLASS:
                continue
            xyxy = [int(value) for value in box.xyxy[0].tolist()]
            detections.append((label, conf))
            x1, y1, x2, y2 = xyxy
            cv2.rectangle(photo, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(
                photo, f"CANDIDATO {conf:.2f}",
                (x1, max(18, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2,
            )

    if not cv2.imwrite(output, photo):
        raise OSError(f"Could not write annotated image: {output}")
    return detections


def main() -> None:
    parser = argparse.ArgumentParser(description="EctoLaser - demonstrador sem laser")
    parser.add_argument("--image", help="Imagem de entrada")
    parser.add_argument("--weights", help="Pesos .pt treinados no Roboflow/dados do EctoLaser")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--output", default="ectolaser_result.jpg")
    parser.add_argument("--port", help="Porta USB serial Arduino (ex.: COM5)")
    parser.add_argument("--manual-demo", action="store_true",
                        help="Simula um foco no LED, sem inferencia de IA")
    args = parser.parse_args()

    if args.manual_demo:
        if args.image or args.weights:
            parser.error("--manual-demo cannot be combined with image/weights")
        print("[SIMULACAO] Comando INDICATE: nao detecta carrapatos.")
        cmd = "INDICATE"
    else:
        if not args.image or not args.weights:
            parser.error("Use --image and --weights, or --manual-demo")
        detections = run_photo(
            args.image, args.weights, args.threshold, args.output
        )
        print(f"Candidatos detectados: {len(detections)} | anotacao: {args.output}")
        cmd = command_for_predictions(detections, args.threshold)

    if args.port:
        reply = send_to_arduino(args.port, cmd)
        print(f"Arduino {args.port} -> {cmd}, resposta: {reply}")
    else:
        print(f"Sem Arduino conectado. Comando que seria enviado: {cmd}")


if __name__ == "__main__":
    main()
