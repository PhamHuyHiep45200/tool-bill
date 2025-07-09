import fitz  # PyMuPDF
import os

def read_pdf_content(pdf_path):
    """Đọc và hiển thị nội dung PDF"""
    try:
        doc = fitz.open(pdf_path)
        print(f"=== NỘI DUNG FILE PDF: {os.path.basename(pdf_path)} ===")
        print(f"Số trang: {len(doc)}")
        print("=" * 50)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            print(f"\n--- TRANG {page_num + 1} ---")
            print(text)
            print("-" * 30)
        
        doc.close()
        return True
    except Exception as e:
        print(f"Lỗi đọc PDF: {e}")
        return False

def extract_specific_info(pdf_path):
    """Trích xuất thông tin cụ thể từ PDF"""
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]  # Lấy trang đầu tiên
        text = page.get_text()
        lines = text.splitlines()
        
        print(f"\n=== THÔNG TIN TRÍCH XUẤT TỪ: {os.path.basename(pdf_path)} ===")
        print("Các dòng có chứa ':' (có thể chứa thông tin quan trọng):")
        
        for i, line in enumerate(lines):
            if ':' in line:
                print(f"Dòng {i+1}: {line.strip()}")
        
        doc.close()
        return True
    except Exception as e:
        print(f"Lỗi trích xuất thông tin: {e}")
        return False

if __name__ == "__main__":
    # Đọc file test.pdf nếu có
    test_pdf = "test.pdf"
    if os.path.exists(test_pdf):
        print("Đang đọc file test.pdf...")
        read_pdf_content(test_pdf)
        extract_specific_info(test_pdf)
    else:
        print("Không tìm thấy file test.pdf")
        print("Hãy đặt file PDF vào thư mục này và chạy lại script") 