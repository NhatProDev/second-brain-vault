---
type: project
title: ERP SHIRTBYHAND
status: in-progress
created: 2026-11-20
updated: 2026-11-20
tags:
  - project
  - erp
  - inventory
  - purchasing
  - barcode
  - web
---

# ERP SHIRTBYHAND

## Mô tả
Làm website ERP cho xưởng may **SHIRTBYHAND**, phạm vi đầu tiên: **Kho (Inventory)**, **Mua hàng (Purchasing)** và **Đơn hàng MTM/BULK**, kèm hệ thống **barcode** cho kho. Liên quan tới [[shirtvn-frontend]] (đơn từ nền tảng shirt.vn rốt cuộc chảy về xưởng).

## Mục tiêu
Thay quy trình thủ công (Excel, ghi nhớ, nhắn tin) bằng dữ liệu kho real-time, để đơn hàng, NVL và đặt mua được kiểm soát chặt.

## Bối cảnh: quy trình sản xuất hiện tại
- **MTM:** Input → Tiếp nhận đơn (Thắm) → Xuất kho ảo → Thiết kế pattern → Lấy NVL ở kho → Sản xuất → Kho xuất hàng → OUT.
- **BULK:** Input → Tiếp nhận đơn (Thắm) → Xuất kho ảo → Thiết kế pattern (tùy) → Chuẩn bị NVL (đơn lớn, phức tạp, hay sai) → Nhập kho bulk → Sản xuất → Kho xuất hàng → OUT.
- Mọi đơn **dùng chung một kho NVL**.

### Thuật ngữ
- **Kho ảo / kho văn phòng:** kho trên phần mềm; người đặt hàng xem tồn để quyết định có đủ NVL nhận đơn không.
- **Kho vật lý:** thủ kho chỉ lo việc kho thật, không quan tâm kho ảo.
- **Xuất kho:** cái gì rời kho thì bị trừ.
- **Số lượng báo động kho:** NVL xuống dưới mức tối thiểu.

## Vấn đề (từ tài liệu của chủ vault)
**Kho**
1. **Tranh chấp NVL:** đơn B lấy trước, không cập nhật real-time → đơn A tới ngày thì thiếu (vd. 5 bút, A cần 4 ngày 3.1, B cần 2 ngày 2.1).
2. **Lệch kho:** số người đặt hàng biết (cập nhật cũ) khác số thực tế.
3. **Báo động tồn tối thiểu:** thủ kho cuối tháng mới làm báo cáo tồn tay rồi tự order → cần cảnh báo real-time.

**Mua hàng**
4. **Giá thay đổi, không ai nhập:** NCC báo giá qua Zalo, Gmail, PDF, tin nhắn "35k em nhé"; giám đốc duyệt rồi mới nhập → rườm rà, dễ sai.
5. **Hóa đơn lệch đơn đặt hàng:** đặt 9 bút giá 10k, hóa đơn về giá 11k (số lượng không sai, sai ở giá).
6. **Nhập tay Item ID/Name** (vd. `CUC14L_BLOM_NV`) → sai. Đề xuất: chọn danh mục dạng dropdown trước, hệ thống tự sinh mã (vd. Nước uống → Lavie → 1.5L ⇒ `NU_LV_1.5L`).

**Barcode (MTM)**
7. Khách MTM **đổi vải giữa chừng** qua vài tin nhắn (A → B); kho vật lý xuất đúng B nhưng hệ thống vẫn ghi A.
8. Người đặt hàng nhập Excel (mã đơn, mã vải, số lượng), sáng hôm sau merge thành file tổng + chồng tờ đặt hàng gửi thiết kế → kho; kho lấy vải và nhập tay. Đề xuất: **thủ kho quét barcode trên tờ đặt hàng, hệ thống tự cập nhật tồn**.

**Tính năng mong muốn:** profile cho từng item (biểu đồ giá, lịch giá, tần suất, metadata, ảnh – tùy); so sánh hóa đơn với PO; cây (node tree) theo dõi đơn hàng – order – NVL tích hợp với kho.

## Trạng thái hiện tại
- **2026-11-20:** Giai đoạn phân tích & thiết kế. Đã có (local, thư mục ERP):
  - `INVENTORY-PURCHASING-summary.html` — tóm tắt 6 vấn đề Kho/Mua hàng.
  - `ERP-FLOWS.html` — 8 luồng "Hiện tại vs Đề xuất" (MTM, BULK, đổi vải, tranh chấp NVL, tồn tối thiểu, đổi giá NCC, đối chiếu hóa đơn, tạo item).
  - `ERP-TECH-STACK-CLASS-DIAGRAM.html` — so sánh 3 hướng, stack đề xuất, kiến trúc, class diagram (Danh mục & Kho, Đơn hàng & Sản xuất, Mua hàng & Giá), quy tắc nghiệp vụ, lộ trình.
- Chưa viết code.

## Thiết kế đề xuất (tóm tắt)
- **Hướng A (đề xuất): tự build TypeScript full-stack.** Thay thế: B. Django; C. dùng thử Odoo 1 tuần với dữ liệu thật nếu cần dùng sớm.
- Stack: React + Vite + Ant Design, TanStack Query, RHF + Zod; NestJS; Prisma; PostgreSQL 16; Redis + BullMQ; Socket.IO; MinIO/R2; LLM đọc báo giá (AI chỉ điền nháp, giám đốc duyệt); barcode Code128 (máy quét USB HID + `@zxing/browser` camera, `bwip-js` sinh mã); Docker Compose trên 1 VPS.
- Kiến trúc: **modular monolith** — module catalog, inventory, orders, purchasing.
- Nguyên tắc cốt lõi:
  - Một **sổ kho (StockMovement)** duy nhất, không UPDATE số tồn trực tiếp; kho ảo = `khả dụng = tồn thực − đã giữ chỗ`.
  - **Giữ chỗ (Reservation)** trong transaction, khóa dòng `SELECT … FOR UPDATE`.
  - **Phiếu đơn có phiên bản**; đổi vải → barcode cũ bị `voided`, quét sẽ báo "đơn đã thay đổi".
  - Số lượng `numeric(18,3)`, tiền `numeric(18,2)`/VND nguyên — không dùng float.
  - Chỉ Giám đốc tạo `SupplierPrice`; PO chụp lại giá lúc đặt; đối chiếu 3 bên PO / phiếu nhập / hóa đơn với ngưỡng (vd. ≤ 0.5%).
  - Kiểm kê tạo `ADJUSTMENT` có lý do, người duyệt; mọi thao tác có nhật ký.
- Vai trò: Đặt hàng, Thủ kho, Thiết kế, Giám đốc, Kế toán, Admin.

## Việc tiếp theo
- [ ] Chủ vault chốt hướng đi: tự build (A) hay thử Odoo trước.
- [ ] Lộ trình nếu đi hướng A:
  1. Nền móng: Auth/RBAC, Category, Item (mã tự sinh), Warehouse, Supplier, nhập tồn đầu kỳ từ Excel.
  2. Sổ kho: nhập/xuất/chuyển, barcode, kiểm kê.
  3. Đơn hàng: MTM/BULK, BOM, giữ chỗ, phiếu barcode có phiên bản, đổi vải.
  4. Mua hàng: cảnh báo tồn, PurchaseRequest, PO, nhận hàng.
  5. Giá & hóa đơn: hộp báo giá + AI, duyệt giá, profile item, đối chiếu hóa đơn.
- [ ] Giai đoạn 2–3 quan trọng nhất; chạy song song với Excel 2–4 tuần để so số trước khi bỏ Excel.
- [ ] Xin dữ liệu mẫu: file Excel đơn hàng, danh sách mã item hiện có, mẫu tờ đặt hàng, vài báo giá NCC thật.

## Quyết định
- **2026-11-20 — Đề xuất kiến trúc modular monolith, chưa microservices.** Lý do: team nhỏ, dữ liệu kho và đơn hàng gắn chặt trong cùng transaction.
- **2026-11-20 — Đề xuất dùng sổ kho + giữ chỗ thay vì sửa số tồn.** Lý do: giải quyết tận gốc lệch kho và tranh chấp NVL.
- (Hướng A/B/C: **chưa chốt**.)

## Câu hỏi còn mở
- Tự build hay Odoo? Ai sẽ làm backend?
- Quy mô người dùng, số kho vật lý, có cần app điện thoại cho kho không?
- Báo giá Zalo đến từ Zalo cá nhân hay Zalo OA (chỉ OA có API)?
- Mức tối thiểu và lượng đặt lại cho từng NVL do ai đặt?
- Deadline: chưa có.

## Tài nguyên
- Tài liệu gốc (local, máy Windows): `C:\Users\ACER\Desktop\ERP\` — `INVENTORY-PURCHASING.docx`, `BARCODE.docx`, cùng 3 trang HTML phân tích ở trên.
- Code: chưa có repo.
