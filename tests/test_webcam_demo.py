"""Unit tests; webcam and actual faces are not required."""
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from demo.webcam_demo import (
    BADGE_PAYLOAD,
    FACE_XML,
    describe_scene,
    is_demo_badge,
    make_badge,
    render_frame,
)


class WebcamDemoTests(unittest.TestCase):
    def test_badge_exact_match_only(self):
        self.assertTrue(is_demo_badge(BADGE_PAYLOAD))
        self.assertFalse(is_demo_badge("WICOLLY"))
        self.assertFalse(is_demo_badge("ECTOLASER:VISITANTE"))

    def test_face_without_qr_is_not_identified(self):
        self.assertEqual(
            describe_scene(1, False),
            ("ROSTO PRESENTE", "CRACHA NAO DETECTADO"),
        )

    def test_badge_is_not_face_identity(self):
        self.assertEqual(
            describe_scene(0, True),
            ("SEM ROSTO", "CRACHA WICOLLY LIDO (DEMO)"),
        )

    def test_no_face_no_badge(self):
        self.assertEqual(
            describe_scene(0, False),
            ("SEM ROSTO", "CRACHA NAO DETECTADO"),
        )

    def test_haar_cascade_exists(self):
        cascade = cv2.CascadeClassifier(FACE_XML)
        self.assertFalse(cascade.empty())

    def test_qr_badge_decodes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "badge.png"
            make_badge(str(path))
            image = cv2.imread(str(path))
            self.assertIsNotNone(image)
            payload, points, _ = cv2.QRCodeDetector().detectAndDecode(image)
            self.assertEqual(payload, BADGE_PAYLOAD)
            self.assertIsNotNone(points)

    def test_render_does_not_require_identity(self):
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        display = render_frame(
            blank, [], None, "SEM ROSTO", "CRACHA NAO DETECTADO", 19.4
        )
        self.assertEqual(display.shape, (540, 1380, 3))


if __name__ == "__main__":
    unittest.main()
