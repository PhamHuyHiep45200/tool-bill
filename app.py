import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import os

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

def process_pdf(input_path, output_path):
    # Dữ liệu mẫu hóa đơn
    company = "CÔNG TY CỔ PHẦN VẬT TƯ THIẾT BỊ HOÀNG KIM"
    address = "Số nhà 18, ngõ 114, đường Thanh Bình, Phường Mộ Lao, Quận Hà Đông, Thành phố Hà Nội, Việt Nam"
    mst = "0108397618"
    account = "191338091017 - Ngân hàng Techcombank - CN Hà Tây"
    invoice_code = "01GTKT0/001"
    invoice_symbol = "HK/18E"
    invoice_number = "0000000"
    customer = "Tên khách hàng: ..........................................."
    buyer = "Người mua hàng: ..........................................."
    date = "......../......../2023"
    table_headers = ["STT", "Tên hàng hóa, dịch vụ", "Đơn vị tính", "Số lượng", "Đơn giá", "Thành tiền (đồng)"]
    table_data = [
        ["1", "", "", "", "", ""],
        ["2", "", "", "", "", ""],
        ["3", "", "", "", "", ""],
        ["4", "", "", "", "", ""],
        ["5", "", "", "", "", ""],
        ["6", "", "", "", "", ""],
        ["7", "", "", "", "", ""],
        ["8", "", "", "", "", ""],
        ["9", "", "", "", "", ""],
        ["10", "", "", "", "", ""]
    ]
    total = ""
    vat = ""
    total_payment = ""

    # Tạo file PDF mới
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size
    # Logo lớn góc trái (nếu có)
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        page.insert_image([40, 25, 140, 75], filename=logo_path)

    # Viền ngoài hóa đơn
    page.draw_rect([30, 20, 565, 800], color=(0.2,0.2,0.2), width=1)

    # Đăng ký font Unicode với tên F0
    page.insert_font(fontname="F0", fontfile=FONT_PATH)
    # Tiêu đề căn giữa, màu nổi bật
    page.insert_textbox([180, 35, 540, 60], "HÓA ĐƠN", fontsize=18, fontname="F0", color=(1,0,0), render_mode=3, align=1)
    page.insert_textbox([180, 55, 540, 75], "GIÁ TRỊ GIA TĂNG", fontsize=13, fontname="F0", color=(1,0,0), align=1)
    # Mẫu số, ký hiệu, số hóa đơn
    page.insert_textbox([430, 30, 590, 45], f"Mẫu số : {invoice_code}", fontsize=9, fontname="F0", color=(0,0,0), align=2)
    page.insert_textbox([430, 45, 590, 60], f"Ký hiệu : {invoice_symbol}", fontsize=9, fontname="F0", color=(0,0,0), align=2)
    page.insert_textbox([430, 60, 590, 75], f"Số : {invoice_number}", fontsize=9, fontname="F0", color=(1,0,0), align=2)

    # Thông tin công ty căn trái
    page.insert_text((50, 90), company, fontsize=11, fontname="F0", color=(0,0,0), render_mode=3)
    page.insert_text((50, 110), f"Mã số thuế : {mst}", fontsize=10, fontname="F0")
    page.insert_text((50, 125), address, fontsize=9, fontname="F0")
    page.insert_text((50, 140), f"Số tài khoản : {account}", fontsize=9, fontname="F0")
    # QR code placeholder (vẽ khung, bạn có thể thay bằng ảnh QR thật)
    page.draw_rect([420, 90, 470, 140], color=(0.7,0.7,0.7), width=0.7)
    page.insert_text((475, 100), "QR", fontsize=10, fontname="F0", color=(0.5,0.5,0.5))
    # Ngày tháng
    page.insert_text((430, 110), f"Ngày ... tháng ... năm ...", fontsize=9, fontname="F0")

    # Vẽ bảng
    x0, y0 = 40, 180
    col_widths = [30, 180, 60, 60, 80, 100]
    row_height = 26
    # Header bảng: nền xám nhạt, border đậm
    page.draw_rect([x0, y0, x0+sum(col_widths), y0+row_height], color=(0.2,0.2,0.2), fill=(0.93,0.93,0.93), width=1)
    x = x0
    for i, header in enumerate(table_headers):
        page.insert_text((x+2, y0+7), header, fontsize=10, fontname="F0", color=(0,0,0), render_mode=3)
        x += col_widths[i]
    # Vẽ dòng header
    page.draw_rect([x0, y0, x0+sum(col_widths), y0+row_height], color=(0.2,0.2,0.2), width=1)
    # Vẽ các dòng dữ liệu
    for row_idx, row in enumerate(table_data):
        y = y0 + row_height * (row_idx+1)
        x = x0
        for col_idx, cell in enumerate(row):
            page.insert_text((x+2, y+7), cell, fontsize=10, fontname="F0", color=(0,0,0))
            x += col_widths[col_idx]
        page.draw_rect([x0, y, x0+sum(col_widths), y+row_height], color=(0.7,0.7,0.7), width=0.5)
    # Vẽ các đường dọc
    x = x0
    y1 = y0
    y2 = y0 + row_height * (len(table_data) + 1)
    for w in col_widths:
        page.draw_line((x, y1), (x, y2), color=(0.7,0.7,0.7), width=0.5)
        x += w
    page.draw_line((x, y1), (x, y2), color=(0.7,0.7,0.7), width=0.5)

    # Sau khi vẽ bảng, chèn ảnh watermark tax.jpg vào giữa trang
    tax_img_path = os.path.join(os.path.dirname(__file__), "tax.jpg")
    if os.path.exists(tax_img_path):
        # Vị trí và kích thước watermark (giữa trang, lớn)
        # (x0, y0, x1, y1) = (100, 260, 500, 600) có thể điều chỉnh cho phù hợp
        page.insert_image([100, 260, 500, 600], filename=tax_img_path, overlay=False, keep_proportion=True)

    # Thông tin tổng tiền, VAT, tổng thanh toán
    y_sum = y0 + row_height*(len(table_data)+1) + 15
    page.insert_text((x0, y_sum), "Cộng tiền hàng: ........................................", fontsize=10, fontname="F0")
    page.insert_text((x0, y_sum+18), "Thuế suất GTGT: ............. Tiền thuế GTGT: .............", fontsize=10, fontname="F0")
    page.insert_text((x0, y_sum+36), "Tổng cộng tiền thanh toán: ........................................", fontsize=10, fontname="F0")
    # Chữ ký style đẹp, chú thích đỏ
    y_sign = y_sum + 70
    page.insert_text((x0, y_sign), "Người mua hàng", fontsize=10, fontname="F0", render_mode=3)
    page.insert_text((x0+200, y_sign), "Người bán hàng", fontsize=10, fontname="F0", render_mode=3)
    page.insert_text((x0+400, y_sign), "Thủ trưởng đơn vị", fontsize=10, fontname="F0", render_mode=3)
    page.insert_text((x0, y_sign+18), "(Ký, ghi rõ họ tên)", fontsize=9, fontname="F0", color=(1,0,0))
    page.insert_text((x0+200, y_sign+18), "(Ký, ghi rõ họ tên)", fontsize=9, fontname="F0", color=(1,0,0))
    page.insert_text((x0+400, y_sign+18), "(Ký, ghi rõ họ tên)", fontsize=9, fontname="F0", color=(1,0,0))
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
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_path:
            try:
                process_pdf(self.pdf_path, save_path)
                self.status_label.config(text=f"Đã tạo hóa đơn: {os.path.basename(save_path)}")
                messagebox.showinfo("Thành công", f"Đã lưu file: {save_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # Set window size to 400x400
    app = PDFApp(root)
    root.mainloop() 