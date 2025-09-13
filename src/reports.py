import os
import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

REPORTS_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def load_private_key(path):
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def load_public_key(path):
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def sign_data(private_key, data: bytes) -> bytes:
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verify_signature(public_key, signature: bytes, data: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
              mgf=padding.MGF1(hashes.SHA256()),
              salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def generate_report(file_path, file_hash, private_key_path, public_key_path):
    # Prepare report metadata
    filename = os.path.basename(file_path)
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    report_data = {
        "file_name": filename,
        "file_hash": file_hash,
        "deleted_at": timestamp,
    }

    # Load private key and sign the file hash JSON string
    private_key = load_private_key(private_key_path)
    report_json_bytes = json.dumps(report_data, indent=4).encode("utf-8")

    signature = sign_data(private_key, report_json_bytes)
    signature_hex = signature.hex()

    # Add signature to report data
    report_data["signature"] = signature_hex

    # Save JSON report
    json_report_path = os.path.join(REPORTS_DIR, f"{filename}_wipe_report.json")
    with open(json_report_path, "w") as f:
        json.dump(report_data, f, indent=4)

    # Generate PDF report
    pdf_report_path = os.path.join(REPORTS_DIR, f"{filename}_wipe_report.pdf")
    c = canvas.Canvas(pdf_report_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Secure Wipe Report")

    c.setFont("Helvetica", 12)
    lines = [
        f"File Name: {report_data['file_name']}",
        f"File SHA256 Hash: {report_data['file_hash']}",
        f"Deleted At (UTC): {report_data['deleted_at']}",
        "",
        "SHA256 Hash Signature (hex):",
        signature_hex,
    ]

    y = height - 100
    for line in lines:
        c.drawString(50, y, line)
        y -= 18

    c.save()

    return json_report_path, pdf_report_path
