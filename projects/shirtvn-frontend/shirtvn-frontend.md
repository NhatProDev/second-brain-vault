---
type: project
title: ShirtVN Frontend Dev
status: in-progress
created: 2026-11-13
updated: 2026-11-14
tags:
  - project
  - frontend
  - web
  - b2c
  - saas
---

# ShirtVN Frontend Dev

## Mô tả
Phát triển frontend cho nền tảng **B2C của shirt.vn**. Đây là **dịch vụ SaaS cho các nhà may đo trên toàn thế giới**. Mỗi nhà may có thể:
- tùy biến trang web và tên miền riêng,
- quản lý danh mục vải và kiểu áo,
- lưu cơ sở dữ liệu khách hàng (kèm số đo), v.v.

Khi khách đặt hàng, nhà may duyệt đơn. Đơn được duyệt sẽ gửi về **nền tảng B2B** (backend) qua API để chuyển tới xưởng may.

## Mục tiêu
Hoàn thành frontend B2C bằng ReactJS, kết nối được với backend B2B API hiện có.

## Luồng dữ liệu
Khách hàng → Trang web của nhà may (frontend B2C) → Nhà may duyệt đơn → Backend API B2B → Xưởng may

## Người tham gia
- **Tôi**: làm frontend B2C.
- **Chú tôi** (công ty Yên Biên): cầm trịch nền tảng B2B và backend API.

## Dữ liệu số đo trong đơn hàng
Theo form hiện có của hệ thống B2B (ảnh chụp màn hình do chủ vault cung cấp):
- Thông tin khách: Client ID, Họ tên, Email.
- Loại số đo (Measurement type): ví dụ "Body Measurement" (dropdown, có thể có loại khác).
- Số đo bắt buộc (cm, kèm khoảng hợp lệ):
  - Neck 30–60
  - Chest 80–190
  - Waist 70–190
  - Hips 70–190
  - Shoulders 30–65
  - Arm Length 40–90
  - Upper Arm 20–50
  - Wrist 12–35
  - Back Length 50–100
- Thông tin tùy chọn: Body Height 120–250 cm, Body Weight 40–250 kg, Shoe size 32–46.

## Trạng thái hiện tại
- Đã chốt công nghệ (ReactJS) và nắm phạm vi sản phẩm (SaaS đa nhà may).
- **2026-11-14:** Đã dựng xong bản đầu của **trang thiết kế áo (shirt configurator)** theo design của chủ vault, chạy được local (`npm run dev`, cổng 5173):
  - Thanh bên 12 mục: Product, Fabric, Fit type, Collar, Sleeve, Cuffs, Front placket, Pocket, Button, Embroidery, Others, Measurements.
  - Hình áo xem trước vẽ bằng SVG, đổi theo lựa chọn, có mặt trước và mặt sau; có nút reset và nút Expand bảng tùy chọn.
  - Giá cộng dồn theo lựa chọn (mặc định 899,000 đ); form số đo kiểm tra khoảng hợp lệ; Check out hiện tóm tắt đơn.
  - Dữ liệu còn là **dữ liệu mẫu** (`src/data/catalog.ts`), chưa nối API; ảnh minh họa tùy chọn đang là hình nét tạm.
- **2026-11-14 (buổi 2):** Làm lại trang theo design điện thoại, thêm bản desktop và bản 3D:
  - **Điện thoại / tablet (< 1024px):** khớp design gốc (ảnh `1.webp` chủ vault gửi). Ảnh áo hoa thật cắt từ design (`public/images/preview/shirt-floral-blue-front.webp`) chỉ hiện khi cấu hình đúng như áo trong ảnh; đổi chi tiết thì quay về hình SVG.
  - **Desktop (≥ 1024px):** bố cục mới do Claude tự thiết kế dựa trên font Montserrat + tông đen/trắng/xám của design: cột bước bên trái, áo lớn ở giữa, bảng tùy chọn bên phải có "Step x of 12", nút ← →, "Next: …", tổng tiền và Check out. Chủ vault đã duyệt, thích design này.
  - **Chế độ 3D:** nút "3D" cạnh Front/Back. Áo dựng bằng three.js (React Three Fiber), ghép từ bộ phận theo option (fit, vạt, tay, măng sét, 6 kiểu cổ, nẹp, cúc, túi, ly sau, chữ thêu); vải là texture từ họa tiết mẫu. Xoay / dời / zoom được. Code: `src/components/Shirt3D.tsx`, tải riêng (~920 KB) chỉ khi bấm 3D.
  - Hạn chế: áo 3D là hình khối cơ bản, trông "cứng", chưa có nếp vải.
- Chạy local: `npm install` rồi `npm run dev` (Node 20.13 chạy được).

## Việc tiếp theo
- [ ] Xin tài liệu backend API B2B từ chú (endpoint, xác thực, định dạng đơn hàng, các loại measurement type khác).
- [ ] Tìm người làm 3D dựng áo bằng CLO3D / Marvelous Designer, xuất **.glb** chia phần theo option (`collar_classic`, `sleeve_long`, `cuff_french`, `pocket_left`…, có UV) để thay áo 3D hình khối.
- [ ] Ảnh thật: thẻ Product (Shirt / Polo / Overshirt), ảnh scan vải, ảnh áo cho từng vải (thêm vào `PREVIEW_PHOTOS` trong `src/data/catalog.ts`).
- [ ] Danh sách tùy chọn thật và giá thật.
- [ ] Chốt có chuyển sang Next.js không (khi làm trang công khai cho nhà may cần SEO / tên miền riêng).
- [ ] Liệt kê các màn hình còn lại: phía khách (trang chủ, theo dõi đơn) và phía nhà may (tùy biến trang, quản lý vải/áo, khách hàng, duyệt đơn).
- [ ] Các trang còn thiếu của website: trang chủ, Inspiration (nút đang chưa dẫn đi đâu), giỏ hàng.

## Quyết định
- **2026-11-13 — Frontend dùng ReactJS.** Lý do: chủ vault chọn.
- **2026-11-13 — Sản phẩm là SaaS đa nhà may (multi-tenant), không phải một shop đơn lẻ.** Lý do: mục tiêu kinh doanh là bán dịch vụ cho nhà may đo toàn cầu; đơn chỉ gửi sang B2B sau khi nhà may duyệt.
- **2026-11-14 — Trang đầu tiên làm là trang thiết kế áo (configurator).** Lý do: chủ vault đã có design cho trang này.
- **2026-11-14 — Bản đầu dùng Vite 6 + React 18 + TypeScript, CSS thuần.** Lý do: dựng nhanh một trang tương tác; máy đang có Node 20.13 (Vite 7 cần ≥ 20.19). Code component chuyển sang Next.js được nếu sau này cần.
- **2026-11-14 — Giao diện khách dùng tiếng Anh, theo design.** Lý do: SaaS phục vụ nhà may toàn cầu.
- **2026-11-14 — Design điện thoại giữ nguyên cho < 1024px; desktop dùng bố cục riêng.** Lý do: design gốc chỉ có bản điện thoại; chủ vault cho phép Claude tự thiết kế desktop dựa trên font, màu và tính năng sẵn có.
- **2026-11-14 — Xem trước 3D bằng three.js, áo ghép từ bộ phận theo option; bản hiện tại là mẫu hình khối.** Lý do: cần áo xoay/di chuyển được và đổi theo lựa chọn; chưa có model thật nên dựng tạm, cấu trúc giữ được khi thay bằng file .glb.
- **2026-11-14 — Ảnh chụp thật chỉ hiện khi cấu hình khớp ảnh, còn lại dùng SVG.** Lý do: ảnh chụp không đổi theo cổ/tay/túi, hiện sai sẽ gây hiểu nhầm.

## Câu hỏi còn mở
- Tài liệu API B2B nằm ở đâu, xác thực thế nào?
- Phần quản lý của nhà may (tùy biến trang, tên miền, vải, khách hàng) do backend nào lưu: dùng chung backend B2B hay cần backend B2C riêng?
- Tên miền riêng cho từng nhà may sẽ triển khai thế nào (subdomain, custom domain)?
- Ngoài "Body Measurement" còn những loại số đo nào?
- Deadline: chưa có.

## Tài nguyên
- Code: GitHub `NhatProDev/shirtvn-b2c-web` (private); local trên máy Windows: `C:\KhanhNhat\shirtvn b2c web`. Trang thiết kế áo: `src/App.tsx`, `src/components/`, dữ liệu mẫu ở `src/data/`.
- Tài liệu API: chưa có.
