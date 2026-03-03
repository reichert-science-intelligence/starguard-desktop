"""
Generate base64-encoded QR code for footer embedding.
Use QR_-Landing.png if it exists, otherwise generate one for the demo URL.
"""
import base64
from pathlib import Path

QR_PATH = Path(__file__).parent / "QR_-Landing.png"
DEMO_URL = "https://tinyurl.com/bdevpdz5"

if QR_PATH.exists():
    with open(QR_PATH, "rb") as f:
        qr_base64 = base64.b64encode(f.read()).decode()
    print("Using existing QR_-Landing.png")
else:
    print("QR_-Landing.png not found. Generating QR code for demo URL...")
    import qrcode
    import io
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(DEMO_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_base64 = base64.b64encode(buf.getvalue()).decode()

result = f"data:image/png;base64,{qr_base64}"
print("=" * 80)
print("Base64 string (first 80 chars):")
print(result[:80] + "...")
print("=" * 80)
# Output for programmatic use
print(result)
