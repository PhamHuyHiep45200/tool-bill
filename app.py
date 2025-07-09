import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import os
import qrcode
from PIL import Image
import io
from datetime import datetime

# Đường dẫn font Unicode (DejaVuSans)
FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

# Nếu chưa có font, tải về
if not os.path.exists(FONT_PATH):
    import urllib.request
    url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
    urllib.request.urlretrieve(url, FONT_PATH)

# Hàm để trích xuất thông tin từ file PDF đầu vào
# Nếu không có thông tin thì trả về 0
# Giả sử thông tin nằm ở các dòng đầu tiên của trang đầu
# (Có thể tùy chỉnh lại nếu format PDF khác)
def extract_info_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        text = page.get_text()
        lines = text.splitlines()
        name = product = price = "0"
        for line in lines:
            if "Tên khách hàng:" in line:
                name = line.split(":", 1)[-1].strip() or "0"
            if "Sản phẩm:" in line:
                product = line.split(":", 1)[-1].strip() or "0"
            if "Số tiền:" in line:
                price = line.split(":", 1)[-1].strip() or "0"
        return name, product, price
    except Exception:
        return "0", "0", "0"

def create_qr_code(data, size=64):
    """Tạo QR code từ dữ liệu và trả về dưới dạng bytes"""
    try:
        # Tạo QR code đơn giản
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Tạo QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Resize về kích thước mong muốn
        qr_image = qr_image.resize((size, size), Image.Resampling.NEAREST)
        
        # Chuyển thành bytes
        img_byte_arr = io.BytesIO()
        qr_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    except Exception as e:
        print(f"Lỗi tạo QR code: {e}")
        return None

def create_simple_qr_code(text, size=80):
    """Tạo QR code đơn giản (đã test thành công)"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((size, size), Image.Resampling.NEAREST)
        
        img_byte_arr = io.BytesIO()
        qr_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    except Exception as e:
        print(f"Lỗi tạo QR code: {e}")
        return None

def process_pdf(input_path, output_path):
    # Dữ liệu mẫu hóa đơn (có thể lấy từ extract_info_from_pdf nếu muốn động)
    company = "CÔNG TY TNHH THƯƠNG MẠI - DỊCH VỤ KENJO VIỆT NAM"
    address = "183/12/17 Bùi Minh Trực, Phường 5, Quận 8, Thành Phố Hồ Chí Minh, Việt Nam"
    mst = "0316353178"
    account = ""
    invoice_code = "1C22TKJ"
    invoice_symbol = ""
    invoice_number = "4"
    customer = "CÔNG TY TNHH THIẾT KẾ VÀ XÂY DỰNG NHÀ CỘNG SINH"
    customer_mst = "0311556897"
    customer_address = "22 Đào Duy Anh, Phường 09, Quận Phú Nhuận, Thành phố Hồ Chí Minh, Việt Nam"
    payment_method = "TM/CK"
    bank_account = ""
    product = "Ghế massage JS680"
    unit = "Chiếc"
    quantity = "1"
    unit_price = "30.000.000"
    amount = "30.000.000"
    vat_rate = "8%"
    vat_amount = "2.400.000"
    total_payment = "32.400.000"
    total_text = "Ba mươi hai triệu, bốn trăm nghìn đồng chẵn"
    signer = "Nguyễn Tiến Khoa"
    # Tạo file PDF mới
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size
    # Viền ngoài hóa đơn
    page.draw_rect([20, 20, 575, 822], color=(0,0,1), width=1.2)
    # Header logo và mã số hóa đơn
    # Logo (nếu có)
    logo_path = os.path.join(os.path.dirname(__file__), "tax.jpg")
    if os.path.exists(logo_path):
        page.insert_image([30, 30, 120, 80], filename=logo_path)
    # Tiêu đề hóa đơn
    page.insert_font(fontname="F0", fontfile=FONT_PATH)
    page.insert_textbox([120, 30, 420, 55], "HÓA ĐƠN GIÁ TRỊ GIA TĂNG", fontsize=15, fontname="F0", color=(0,0,0.7), render_mode=2, align=1)
    page.insert_textbox([120, 55, 420, 75], "(VAT INVOICE)", fontsize=10, fontname="F0", color=(0,0,0.7), align=1)
    # Mã số, ký hiệu, số hóa đơn
    page.insert_textbox([430, 30, 570, 45], f"Ký hiệu (Serial No): {invoice_code}", fontsize=9, fontname="F0", color=(1,0,0), align=2)
    page.insert_textbox([430, 45, 570, 60], f"Số: {invoice_number}", fontsize=12, fontname="F0", color=(1,0,0), align=2)

    y = 90
        
    # Divider trước thông tin công ty
    y += 10
    page.draw_line((30, y), (565, y), color=(0.7,0.7,0.7), width=0.5)
    y += 15

    page.insert_text((30, y), company, fontsize=11, fontname="F0", color=(0,0,0), render_mode=2)
    y += 18
    page.insert_text((30, y), f"Mã số thuế (Tax code): {mst}", fontsize=10, fontname="F0")
    y += 15
    page.insert_text((30, y), f"Địa chỉ (Address): {address}", fontsize=9, fontname="F0")
    y += 15
    # page.insert_text((30, y), f"Số tài khoản: {account}", fontsize=9, fontname="F0")
        
    # Divider trước thông tin khách hàng
    y += 10
    page.draw_line((30, y), (565, y), color=(0.7,0.7,0.7), width=0.5)
    y += 15

    # QR code - tạo từ thông tin hóa đơn (sử dụng cấu hình đã test thành công)
    qr_data = f"HOADON-{invoice_number}-{total_payment}"
    qr_bytes = create_simple_qr_code(qr_data, size=80)
    if qr_bytes:
        page.insert_image([480, 180, 560, 260], stream=qr_bytes, overlay=True, keep_proportion=True)
    # Thông tin công ty bán


    # Thông tin người mua
    page.insert_text((30, y), f"Tên đơn vị (Buyer): {customer}", fontsize=10, fontname="F0")
    y += 15
    page.insert_text((30, y), f"Mã số thuế (Tax code): {customer_mst}", fontsize=9, fontname="F0")
    y += 15
    page.insert_text((30, y), f"Địa chỉ (Address): {customer_address}", fontsize=9, fontname="F0")
    y += 15
    page.insert_text((30, y), f"Hình thức thanh toán (Payment): {payment_method}", fontsize=9, fontname="F0")

    # Bảng hàng hóa
    y_table = y + 25
    col_widths = [30, 220, 60, 60, 80, 100]
    row_height = 28
    header_height = 32
    subheader_height = 16
    font_size_header = 10
    font_size_text = 8
    vertical_align_big = (row_height - font_size_header) / 2
    vertical_align_small = (row_height - font_size_text) / 2
    table_headers = [
        ("STT", "(No)"),
        ("Tên hàng hóa, dịch vụ", "(Description)"),
        ("Đơn vị tính", "(Unit)"),
        ("Số lượng", "(Quantity)"),
        ("Đơn giá", "(Unit Price)"),
        ("Thành tiền", "(Amount)")
    ]
    table_data = [
        ["1", product, unit, quantity, unit_price, amount],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""]
    ]
    # Header bảng: 2 dòng
    x0, y0 = 30, y_table
    # Vẽ nền header
    page.draw_rect([x0, y0, x0+sum(col_widths), y0+header_height+subheader_height], color=(0,0,0.7), fill=(0.93,0.93,0.99), width=1.2)
    # Vẽ tiêu đề lớn (căn giữa dọc)
    x = x0
    for i, (header, subheader) in enumerate(table_headers):
        page.insert_textbox([x, y0 + vertical_align_big, x+col_widths[i], y0+header_height], header, fontsize=10, fontname="F0", color=(0,0,0.7), render_mode=2, align=1)
        x += col_widths[i]
    # Vẽ dòng subheader (chú thích tiếng Anh, in nghiêng, căn giữa dọc)
    x = x0
    for i, (header, subheader) in enumerate(table_headers):
        page.insert_textbox([x, y0+header_height, x+col_widths[i], y0+header_height+subheader_height], subheader, fontsize=8, fontname="F0", color=(0,0,0.7), render_mode=2, align=1)
        x += col_widths[i]
    # Vẽ border header
    page.draw_rect([x0, y0, x0+sum(col_widths), y0+header_height+subheader_height], color=(0,0,0.7), width=1.2)
    # Dữ liệu hàng hóa (căn giữa dọc)
    for row_idx, row in enumerate(table_data):
        y = y0 + header_height + subheader_height + row_height * row_idx
        x = x0
        for col_idx, cell in enumerate(row):
            page.insert_textbox([x, y + vertical_align_small, x+col_widths[col_idx], y+row_height], cell, fontsize=10, fontname="F0", color=(0,0,0), align=1)
            x += col_widths[col_idx]
        page.draw_rect([x0, y, x0+sum(col_widths), y+row_height], color=(0.5,0.5,0.5), width=0.7)
    # Các dòng tổng hợp trong bảng (không kẻ dọc bên trong, chỉ giữ kẻ dọc ngoài cùng)
    y_sum = y0 + header_height + subheader_height + row_height*len(table_data)
    # Cộng tiền hàng
    page.draw_line((x0, y_sum), (x0+sum(col_widths), y_sum), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum+row_height), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    # Kẻ dọc ngoài cùng
    page.draw_line((x0, y_sum), (x0, y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0+sum(col_widths), y_sum), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.insert_textbox([x0, y_sum + vertical_align_small, x0+sum(col_widths)-100, y_sum+row_height], "Cộng tiền hàng (Total before VAT):", fontsize=10, fontname="F0", align=2)
    page.insert_textbox([x0+sum(col_widths)-100, y_sum + vertical_align_small, x0+sum(col_widths), y_sum+row_height], amount, fontsize=10, fontname="F0", align=2)
    # Thuế suất GTGT và Tiền thuế GTGT
    y_sum += row_height
    page.draw_line((x0, y_sum), (x0+sum(col_widths), y_sum), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum+row_height), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum), (x0, y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0+sum(col_widths), y_sum), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.insert_textbox([x0, y_sum + vertical_align_small, x0+sum(col_widths)//2, y_sum+row_height], f"Thuế suất GTGT (VAT rate): {vat_rate}", fontsize=10, fontname="F0", align=2)
    page.insert_textbox([x0+sum(col_widths)//2, y_sum + vertical_align_small, x0+sum(col_widths)-100, y_sum+row_height], "Tiền thuế GTGT (VAT amount):", fontsize=10, fontname="F0", align=2)
    page.insert_textbox([x0+sum(col_widths)-100, y_sum + vertical_align_small, x0+sum(col_widths), y_sum+row_height], vat_amount, fontsize=10, fontname="F0", align=2)
    # Tổng tiền thanh toán
    y_sum += row_height
    page.draw_line((x0, y_sum), (x0+sum(col_widths), y_sum), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum+row_height), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum), (x0, y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0+sum(col_widths), y_sum), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.insert_textbox([x0, y_sum + vertical_align_small, x0+sum(col_widths)-100, y_sum+row_height], "Tổng tiền thanh toán (Total amount):", fontsize=10, fontname="F0", render_mode=2, align=2)
    page.insert_textbox([x0+sum(col_widths)-100, y_sum + vertical_align_small, x0+sum(col_widths), y_sum+row_height], total_payment, fontsize=10, fontname="F0", render_mode=2, align=2)
    # Số tiền bằng chữ
    y_sum += row_height
    page.draw_line((x0, y_sum), (x0+sum(col_widths), y_sum), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum+row_height), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0, y_sum), (x0, y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.draw_line((x0+sum(col_widths), y_sum), (x0+sum(col_widths), y_sum+row_height), color=(0.5,0.5,0.5), width=0.7)
    page.insert_textbox([x0, y_sum + vertical_align_small, x0+sum(col_widths), y_sum+row_height], f"Số tiền viết bằng chữ (Total amount in words): {total_text}", fontsize=10, fontname="F0", color=(1,0,0), align=0)
    # Đường dọc bảng chỉ vẽ cho phần dữ liệu hàng hóa
    x = x0
    y1 = y0
    y2 = y0 + header_height + subheader_height + row_height * len(table_data)
    for w in col_widths:
        page.draw_line((x, y1), (x, y2), color=(0.5,0.5,0.5), width=0.7)
        x += w
    page.draw_line((x, y1), (x, y2), color=(0.5,0.5,0.5), width=0.7)
    # Watermark dưới bảng
    tax_img_path = os.path.join(os.path.dirname(__file__), "tax.jpg")
    if os.path.exists(tax_img_path):
        page.insert_image([x0+30, y0+header_height+subheader_height+30, x0+sum(col_widths)-30, y0+header_height+subheader_height+row_height*7], filename=tax_img_path, overlay=False, keep_proportion=True)
    # Chữ ký (style lại giống mẫu)
    y_sign = y_sum + 50
    sign_col_width = 250
    # Người mua hàng
    page.insert_textbox([x0, y_sign, x0+sign_col_width, y_sign+20], "Người mua hàng(Buyer)", fontsize=12, fontname="F0", color=(0,0,0), render_mode=2, align=1)
    page.insert_textbox([x0, y_sign+20, x0+sign_col_width, y_sign+36], "(Ký, ghi rõ họ, tên)", fontsize=10, fontname="F0", color=(0,0,0), render_mode=2, align=1)
    page.insert_textbox([x0, y_sign+36, x0+sign_col_width, y_sign+50], "(Signature & full name)", fontsize=9, fontname="F0", color=(0,0,0), render_mode=2, align=1)
    # Người bán hàng
    x_seller = x0+sign_col_width+70
    page.insert_textbox([x_seller, y_sign, x_seller+sign_col_width, y_sign+20], "Người bán hàng(Seller)", fontsize=12, fontname="F0", color=(0,0,0), render_mode=2, align=1)
    page.insert_textbox([x_seller, y_sign+20, x_seller+sign_col_width, y_sign+36], "(Ký, ghi rõ họ, tên)", fontsize=10, fontname="F0", color=(0,0,0), render_mode=2, align=1)
    page.insert_textbox([x_seller, y_sign+36, x_seller+sign_col_width, y_sign+50], "(Signature & full name)", fontsize=9, fontname="F0", color=(0,0,0), render_mode=2, align=1)
    # Dòng ký tên người bán màu đỏ, in nghiêng, căn giữa
    page.insert_textbox([x_seller, y_sign+52, x_seller+sign_col_width, y_sign+68], "Ký tên, đóng dấu", fontsize=11, fontname="F0", color=(1,0,0), render_mode=2, align=1)
    # Box Signature Valid (di chuyển xuống dưới phần ký tên seller, sát lề phải)
    box_x0 = x0+sum(col_widths)-210
    box_y0 = y_sign+90
    box_x1 = box_x0+200
    box_y1 = box_y0+60
    page.draw_rect([box_x0, box_y0, box_x1, box_y1], color=(0.2,0.6,0.2), fill=(0.95,1,0.95), width=1)
    page.insert_textbox([box_x0+5, box_y0+5, box_x1-5, box_y0+22], "Signature Valid", fontsize=11, fontname="F0", color=(0,0.5,0), render_mode=2, align=0)
    page.insert_textbox([box_x0+5, box_y0+22, box_x1-5, box_y0+38], "Ký bởi: CÔNG TY TNHH THƯƠNG MẠI - DỊCH VỤ KENJO VIỆT NAM", fontsize=10, fontname="F0", color=(1,0,0), render_mode=2, align=0)
    page.insert_textbox([box_x0+5, box_y0+38, box_x1-5, box_y0+54], "Ký ngày: 07/02/2022    09:35:53", fontsize=10, fontname="F0", color=(1,0,0), render_mode=2, align=0)
    # Dòng tra cứu hóa đơn và chú thích nhỏ cuối trang
    y_footer = 800
    page.insert_textbox([x0, y_footer, x0+sum(col_widths), y_footer+15], "Tra cứu Hóa đơn điện tử tại: http://tracuu.hoadon.vn  Mã tra cứu: A596F098C9", fontsize=9, fontname="F0", color=(0,0,0.7), align=1)
    page.insert_textbox([x0, y_footer+15, x0+sum(col_widths), y_footer+30], "(Tổ chức truyền nhận và cung cấp giải pháp HĐĐT: Công ty CP công nghệ tin học EFY Việt Nam, MST: 0102519041, www.efy.com.vn, ĐT: 19006142)", fontsize=8, fontname="F0", color=(0,0,0), align=1)
    # Đóng file
    doc.save(output_path)
    doc.close()

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Invoice Tool")
        self.pdf_path = None
        self.result_path = None

        self.upload_btn = tk.Button(root, text="Upload PDF", command=self.upload_pdf)
        self.upload_btn.pack(pady=10)

        self.create_btn = tk.Button(root, text="Tạo hóa đơn", command=self.create_invoice, state=tk.DISABLED)
        self.create_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="No file uploaded.")
        self.status_label.pack(pady=10)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_path = file_path
            self.status_label.config(text=f"Đã chọn: {os.path.basename(file_path)}")
            self.create_btn.config(state=tk.NORMAL)

    def create_invoice(self):
        if not self.pdf_path:
            messagebox.showerror("Lỗi", "Chưa chọn file PDF!")
            return
        
        # Tạo tên file tự động theo định dạng ngày giờ
        current_time = datetime.now()
        filename = f"hoa_don_{current_time.strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Lấy thư mục hiện tại để lưu file
        # current_dir = os.getcwd()
        # save_path = os.path.join(current_dir, filename)
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=filename, title="Lưu hóa đơn PDF")
        
        try:
            process_pdf(self.pdf_path, save_path)
            self.status_label.config(text=f"Đã tạo hóa đơn: {filename}")
            messagebox.showinfo("Thành công", f"Đã lưu file: {save_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # Set window size to 400x400
    app = PDFApp(root)
    root.mainloop() 