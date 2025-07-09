import qrcode
from PIL import Image
import io

def test_qr_code():
    """Test tạo QR code đơn giản"""
    try:
        # Tạo QR code đơn giản
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )
        
        # Dữ liệu đơn giản
        test_data = "HOADON-4-32400000"
        qr.add_data(test_data)
        qr.make(fit=True)
        
        # Tạo image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((100, 100), Image.Resampling.NEAREST)
        
        # Lưu file test
        qr_image.save("test_qr.png")
        print(f"Đã tạo QR code test với dữ liệu: {test_data}")
        print("File: test_qr.png")
        print("Hãy quét QR code này để kiểm tra!")
        
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        return False

if __name__ == "__main__":
    test_qr_code() 