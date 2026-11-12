"""
EctoLaser - prototipo de visao computacional por webcam.

Mostra:
  * Presenca de rostos (nao identifica individuos).
  * Leitura de cracha QR de demonstracao com texto "Wicolly" (nao prova identidade).
  * Opcional: LED embutido do Arduino UNO via USB serial (sem laser).

Nao guarda imagens da webcam, nao faz reconhecimento facial e nao acessa Instagram.
"""
from __future__ import annotations

import argparse
import platform
import time

import cv2
import numpy as np

BADGE_PAYLOAD = "ECTOLASER:WICOLLY:BADGE-DEMO"
WINDOW_NAME = "EctoLaser | Prototipo Webcam"
FACE_XML = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def is_demo_badge(value: str) -> bool:
    return value.strip() == BADGE_PAYLOAD


def describe_scene(face_count: int, badge_found: bool) -> tuple[str, str]:
    """Return non-biometric status messages, not a person's identity."""
    face_status = "ROSTO PRESENTE" if face_count > 0 else "SEM ROSTO"
    badge_status = (
        "CRACHA WICOLLY LIDO (DEMO)" if badge_found else "CRACHA NAO DETECTADO"
    )
    return face_status, badge_status


def make_badge(path: str) -> None:
    encoder = cv2.QRCodeEncoder_create()
    raw_qr = encoder.encode(BADGE_PAYLOAD)
    module = 13
    border = 8
    qr_with_border = cv2.copyMakeBorder(
        raw_qr, border, border, border, border,
        cv2.BORDER_CONSTANT, value=255,
    )
    large = cv2.resize(
        qr_with_border,
        (qr_with_border.shape[1] * module, qr_with_border.shape[0] * module),
        interpolation=cv2.INTER_NEAREST,
    )
    card = np.full(
        (large.shape[0] + 175, large.shape[1] + 100, 3),
        255, dtype=np.uint8,
    )
    x = (card.shape[1] - large.shape[1]) // 2
    card[115:115 + large.shape[0], x:x + large.shape[1]] = cv2.cvtColor(
        large, cv2.COLOR_GRAY2BGR
    )
    cv2.putText(
        card, "ECTOLASER", (40, 48), cv2.FONT_HERSHEY_SIMPLEX,
        1.2, (20, 68, 60), 3, cv2.LINE_AA,
    )
    cv2.putText(
        card, "WICOLLY - CRACHA DEMO", (40, 88),
        cv2.FONT_HERSHEY_SIMPLEX, .65, (65, 65, 65), 2, cv2.LINE_AA,
    )
    cv2.putText(
        card, "Nao comprova identidade", (40, card.shape[0] - 24),
        cv2.FONT_HERSHEY_SIMPLEX, .55, (55, 55, 55), 1, cv2.LINE_AA,
    )
    if not cv2.imwrite(path, card):
        raise OSError(f"Falha ao salvar QR: {path}")


def capture_from(index: int):
    if platform.system() == "Windows":
        return cv2.VideoCapture(index, cv2.CAP_DSHOW)
    return cv2.VideoCapture(index)


class UnoIndicator:
    """Conexao persistente com firmware do PR #1: somente LED embutido."""

    def __init__(self, port: str):
        try:
            import serial
        except ImportError as exc:
            raise RuntimeError(
                "Para usar Arduino: python -m pip install pyserial"
            ) from exc
        self.connection = serial.Serial(
            port, 115200, timeout=0.7, write_timeout=0.7,
        )
        time.sleep(2.0)
        self.connection.reset_input_buffer()
        self._last_sent = 0.0

    def update(self, active: bool):
        now = time.monotonic()
        if now - self._last_sent < 0.4:
            return
        self._last_sent = now
        command = "INDICATE" if active else "CLEAR"
        self.connection.write((command + "\n").encode("ascii"))
        self.connection.flush()
        response = self.connection.readline().decode(
            "ascii", errors="replace"
        ).strip()
        if response != "OK":
            raise RuntimeError(
                f"Resposta inesperada do Arduino: {response!r}"
            )

    def close(self):
        try:
            self.connection.write(b"CLEAR\n")
        finally:
            self.connection.close()


def render_frame(frame, faces, points, face_label, badge_label, fps):
    height, width = frame.shape[:2]
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame, (x, y), (x + w, y + h),
            (113, 230, 80), 3,
        )
    if points is not None and len(points) > 0:
        polygon = points.reshape(-1, 2).astype(np.int32)
        cv2.polylines(frame, [polygon], True, (255, 191, 80), 3)

    # Painel fixo no lado direito, independente do tamanho da camera.
    frame = cv2.resize(frame, (960, 540), interpolation=cv2.INTER_LINEAR)
    panel = np.full((540, 420, 3), (35, 30, 25), dtype=np.uint8)
    cv2.putText(
        panel, "ECTOLASER", (25, 65), cv2.FONT_HERSHEY_SIMPLEX,
        1.15, (120, 231, 134), 3, cv2.LINE_AA,
    )
    cv2.putText(
        panel, "Webcam / laboratorio", (25, 100),
        cv2.FONT_HERSHEY_SIMPLEX, .58, (212, 210, 205), 1, cv2.LINE_AA,
    )
    cv2.line(panel, (25, 125), (390, 125), (95, 95, 95), 1)
    cv2.putText(
        panel, "DETECCAO VISUAL", (25, 160),
        cv2.FONT_HERSHEY_SIMPLEX, .53, (190, 190, 190), 1, cv2.LINE_AA,
    )
    cv2.putText(
        panel, face_label, (25, 195),
        cv2.FONT_HERSHEY_SIMPLEX, .67, (112, 226, 123), 2, cv2.LINE_AA,
    )
    cv2.putText(
        panel, "LEITURA DE QR", (25, 250),
        cv2.FONT_HERSHEY_SIMPLEX, .53, (190, 190, 190), 1, cv2.LINE_AA,
    )
    cv2.putText(
        panel, badge_label, (25, 285),
        cv2.FONT_HERSHEY_SIMPLEX, .56, (125, 205, 251), 2, cv2.LINE_AA,
    )
    cv2.line(panel, (25, 325), (390, 325), (95, 95, 95), 1)
    notes = (
        "A webcam detecta rostos.",
        "O QR le um cracha de demo.",
        "Nao reconhece quem e a pessoa.",
        "Nenhuma imagem e salva.",
        "Q / ESC = encerrar.",
    )
    for i, note in enumerate(notes):
        cv2.putText(
            panel, note, (25, 355 + i * 29),
            cv2.FONT_HERSHEY_SIMPLEX, .49, (205, 205, 205),
            1, cv2.LINE_AA,
        )
    cv2.putText(
        panel, f"FPS: {fps:.1f}", (25, 525),
        cv2.FONT_HERSHEY_SIMPLEX, .5, (176, 176, 176), 1,
    )
    return np.hstack((frame, panel))


def check_camera(index: int) -> None:
    cap = capture_from(index)
    try:
        ok, frame = cap.read() if cap.isOpened() else (False, None)
        if not ok:
            raise RuntimeError(
                f"Webcam {index} indisponivel; tente --camera 0, 1 ou 2."
            )
        print(
            f"CAMERA_OK index={index} resolution="
            f"{frame.shape[1]}x{frame.shape[0]}"
        )
    finally:
        cap.release()


def live(camera: int, port: str | None, max_frames: int, headless: bool):
    cascade = cv2.CascadeClassifier(FACE_XML)
    if cascade.empty():
        raise RuntimeError(f"Cascade face data unavailable: {FACE_XML}")
    detector = cv2.QRCodeDetector()
    cap = capture_from(camera)
    if not cap.isOpened():
        raise RuntimeError(
            f"Nao foi possivel abrir a webcam {camera}. Tente 0, 1 ou 2."
        )

    uno = None
    if port:
        try:
            uno = UnoIndicator(port)
        except Exception:
            cap.release()
            raise

    processed = 0
    detected_qr = False
    face_seen = False
    last_tick = time.monotonic()
    last_qr_time = 0.0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            processed += 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = cascade.detectMultiScale(
                gray, scaleFactor=1.12, minNeighbors=5,
                minSize=(55, 55),
            )
            face_seen = len(faces) > 0

            payload, qr_points, _ = detector.detectAndDecode(frame)
            if is_demo_badge(payload):
                last_qr_time = time.monotonic()
            detected_qr = time.monotonic() - last_qr_time < 1.5
            face_label, badge_label = describe_scene(
                len(faces), detected_qr,
            )

            if uno is not None:
                uno.update(face_seen and detected_qr)

            now = time.monotonic()
            fps = 1.0 / max(now - last_tick, 0.00001)
            last_tick = now
            if not headless:
                panel_frame = render_frame(
                    frame, faces, qr_points, face_label, badge_label, fps,
                )
                cv2.imshow(WINDOW_NAME, panel_frame)
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q"), ord("Q")):
                    break
            if max_frames > 0 and processed >= max_frames:
                break
        print(
            f"TESTE_OK frames={processed}, rosto_ultimo_frame="
            f"{face_seen}, qr_demo_ultimo_frame={detected_qr}"
        )
    finally:
        if uno is not None:
            uno.close()
        cap.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="EctoLaser: detector de rosto + QR, sem identificacao facial"
    )
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--make-badge", metavar="PNG")
    parser.add_argument("--check-camera", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--max-frames", type=int, default=0)
    parser.add_argument("--port", help="Opcional: porta USB Arduino UNO, ex.: COM5")
    args = parser.parse_args()

    if args.make_badge:
        make_badge(args.make_badge)
        print(f"CRACHA_DEMO_CRIADO: {args.make_badge}")
    elif args.check_camera:
        check_camera(args.camera)
    else:
        live(args.camera, args.port, args.max_frames, args.headless)


if __name__ == "__main__":
    main()
