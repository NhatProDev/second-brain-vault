---
type: project
title: ShirtVN Frontend Dev
status: in-progress
created: 2026-11-13
updated: 2026-11-27
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
- **2026-11-14 (buổi 3):** Nâng cấp áo 3D ngay trong code (`src/components/Shirt3D.tsx`), vẫn là áo dựng bằng code:
  - Tay áo buông theo đường cong, khuỷu hơi gập; thân và tay có nếp vải; lá cổ bẻ nằm trên vai/ngực; cúc có lỗ và chỉ.
  - Vải có sợi dệt (normal map) và độ bóng nhẹ; đèn studio tự dựng, có bóng đổ.
  - Vải Floral Blue vẽ lại thành họa tiết paisley, màu nền đổi sang `#5273b3`.
  - Chế độ 3D chừa chỗ cho nút Front / Back / 3D, camera tự lùi khi khung hẹp.
  - Thử dựng áo thật trong Blender (qua Blender MCP) nhưng **chưa làm được**: Blender chưa bật addon MCP nên không kết nối.
- **2026-11-14 (buổi 4):** Làm lại áo 3D để đạt mức ảnh mẫu (chủ vault chê bản dựng bằng code chưa đạt):
  - **Thân và tay áo là lưới mô phỏng vải thật trong Blender** (`public/models/shirt-sim.glb`, ~3,7 MB). Dựng lại bằng script `tools/blender/shirt_sim.py` rồi `shirt_export.py` (chạy trong Blender, ~2 phút). Bản sao file Blender: `tools/blender/shirt-sim.blend` (không đưa lên git).
  - Cổ, nẹp, cúc, túi, măng sét, chữ thêu vẫn dựng bằng code và bám theo bề mặt lưới (`src/components/Shirt3D.tsx`, số đo vòng cổ / cổ tay ở `src/data/shirt-sim.json`).
  - Vải Floral Blue dùng **ảnh vải cắt từ ảnh áo mẫu** (`public/images/fabrics/floral-blue.webp`), ghép thành ô lặp liền mạch. Ảnh gốc nhỏ nên họa tiết còn hơi mềm; cần ảnh scan vải thật để nét hơn. Các vải khác vẫn là họa tiết vẽ.
  - Thêm chế độ xem riêng áo 3D toàn màn hình để kiểm tra: `/?view3d={"collar":"cutaway"}`.
  - Một subagent chấm điểm độc lập so với ảnh mẫu qua 5 vòng: từ 2–5/10 lên **7/10 hầu hết hạng mục, kết luận ĐẠT sát nút**; cổ áo 6/10 là phần yếu nhất (mỏng, chưa thấy rõ chân cổ).
  - Giới hạn: fit Slim / Loose chỉ co giãn ngang cùng một lưới; vạt thẳng là cắt ngang lưới vạt bầu; cổ áo luôn cài kín (ảnh mẫu mở cổ).
  - Code nằm ở nhánh `shirt-3d-cloth` trên GitHub, chưa gộp vào `main`.
- **2026-11-16:** Gộp nhánh `shirt-3d-cloth` vào `main`. Những gì có thêm:
  - Áo 3D đổi sang model áo tải về dựng lại trong Blender (`public/models/shirt-dl.glb`, script `tools/blender/shirt_dl_export.py` + `tools/blender/dl/`), bỏ bản `shirt-sim`.
  - **Server API + database:** Node (`node:http`) + SQLite có sẵn của Node (`node:sqlite`, cần Node ≥ 22.5; máy đã lên Node 24). Code `server/index.js` (API), `server/db.js` (SQL). API: `POST /api/clients` (lưu khách, cùng SĐT thì cập nhật), `POST /api/orders` (tạo đơn, mã `SV-YYYYMMDD-id`), `GET /api/health`. Dữ liệu ở `server/data/shirtvn.sqlite` (không đưa lên git). Chạy: `npm run server`, test: `npm run test:server`.
  - Trang Checkout + thanh bước (Stepper); khách nhận diện bằng SĐT, không đăng nhập; thanh toán giả lập.
  - **Class diagram:** bản Mermaid `docs/class-diagram.md`; bản vẽ trên Visual Paradigm Online (xếp theo luồng trái → phải) — chủ vault tự lưu trên VP.
  - Xem database: cài **DBeaver Community** (có ER Diagram); DB Browser for SQLite cũng đã cài.
- **2026-11-16 — Bắt đầu bàn trang quản trị cho nhà may (chưa code):** nhà may đăng nhập để xem khách, đơn của mình, duyệt / từ chối đơn, dashboard, thông báo. Đã chốt hướng (xem Quyết định), đang chờ trả lời câu hỏi về API nhà máy.
- **2026-11-21 → 24 — Đưa trang lên mạng: https://b2c.shirt.vn**
  - **Host:** Google Cloud → Compute Engine → **VM instances**, máy `svr2` (Debian 12), IP `34.81.63.73`. Quản trị qua **SSH-in-browser** trên Google Cloud Console. Web server **Nginx**. VM này chạy chung nhiều trang khác (demo.shirt.vn, factory.shirt.vn, mtm.shirt.vn, varc.net.vn…) → chỉ sửa file của mình.
  - Cấu hình Nginx: `/etc/nginx/sites-enabled/b2c.shirt.vn`; thư mục web: `/u01/yenbien/www/b2c.shirt.vn/html`.
  - Chỉ đưa **bản build** (`dist/`) lên VM, không có source code trên VM.
  - **HTTPS:** bật bằng Certbot (`sudo certbot --nginx -d b2c.shirt.vn`), http tự chuyển sang https, chứng chỉ Let's Encrypt tự gia hạn.
  - Cách deploy thủ công (đang dùng): `npm run build` → đóng gói `html.zip` → UPLOAD FILE trong SSH-in-browser → `unzip` + `sudo rsync -a --delete html/ /u01/yenbien/www/b2c.shirt.vn/html/`.
  - Gộp `shirt-3d-cloth` vào `main` (commit `2c457f9`). GitHub dùng để đồng bộ code giữa các máy: `git pull` trước khi làm, `git push` khi xong; máy mới thì `git clone` + `npm install`.
- **2026-11-24 — Trang chủ + trình tùy biến trang web cho nhà may (đợt 1):** theo 6 ảnh design chủ vault gửi (trang chủ, Shop, Measurements, trang sản phẩm, configurator, dashboard nhà may).
  - Đường dẫn mới: `/` trang chủ, `/design` thiết kế áo (trước ở `/`), `/admin` quản trị Storefront.
  - Trang chủ vẽ từ cấu hình JSON: thương hiệu (tên, khẩu hiệu, 4 màu, font tiêu đề / nội dung) + danh sách section (Hero, Shop by Style, 3D Customizer CTA, Featured Fabrics, The Perfect Fit, Customer Stories, Instagram). Code `src/storefront/` (`schema.ts` dùng chung cho server để kiểm tra dữ liệu).
  - `/admin`: kéo thả đổi thứ tự section, ẩn/hiện, thêm/xóa, sửa chữ + ảnh, đổi màu + font, xem trước máy tính / điện thoại, bấm vào section trong khung xem trước để sửa. Lưu qua `PUT /api/storefront` (bảng `storefronts` trong SQLite).
  - Bảo vệ tạm: một mã quản trị chung `SHIRTVN_ADMIN_TOKEN` (local trong `.env`); chưa có đăng nhập nhà may, chưa tách theo tên miền (tenant cố định `default`).
  - Ảnh mặc định cắt từ ảnh design (`public/images/storefront/`), độ phân giải thấp; chưa có tải ảnh lên (chỉ nhập đường dẫn / chọn ảnh có sẵn).
- **2026-11-24 — Trình kéo thả tự do (kiểu portfolio / Readymag):** theo yêu cầu "trang trống, kéo thả, thiết kế được trên PC / tablet / iPhone".
  - `/` là trang web dựng bằng kéo thả; `/admin` là trình thiết kế. Trang mẫu theo section (đợt trước) chuyển sang `/template` + `/admin/template`.
  - Phần tử: tiêu đề, đoạn văn, ảnh, nút, hình chữ nhật, hình tròn, đường kẻ. Kéo từ cột trái thả vào trang; kéo di chuyển có hút cạnh/giữa (đường hồng); tay nắm đổi cỡ (ảnh giữ tỉ lệ); nhấp đúp sửa chữ; bảng bên phải chỉnh font, cỡ, màu, căn lề, bo góc, liên kết…; hoàn tác/làm lại, nhân bản, lớp trên/dưới, phím tắt.
  - Tải ảnh lên (nút hoặc kéo file từ máy thả vào trang) → `server/data/uploads/`.
  - **Đa thiết bị:** 3 bố cục thiết kế ở 1200 / 768 / 390px. Chưa chỉnh thì tablet thu nhỏ theo máy tính, điện thoại tự xếp một cột theo thứ tự trên → dưới. Chỉnh trên tablet/điện thoại thì bố cục thiết bị đó được chốt riêng (vị trí, cỡ, cỡ chữ, ẩn/hiện); nội dung + màu + font dùng chung. Trang thật chọn bố cục theo bề rộng màn hình (≥1024 máy tính, ≥640 tablet) rồi phóng/thu cho vừa.
  - Code `src/builder/` (`schema.ts` dùng chung cho server kiểm tra dữ liệu: chặn link `javascript:`, màu/font lạ…); API `GET/PUT /api/page`, `POST /api/uploads`.
  - Vẫn chỉ một trang, một nhà may (tenant `default`), khóa bằng mã quản trị chung.
- **2026-11-24 — Đăng nhập nhà may + tách dữ liệu theo tiệm:**
  - Nhà may tự đăng ký cửa hàng ở `/register` (tên tiệm, địa chỉ `slug` tự sinh từ tên, email, mật khẩu), đăng nhập ở `/login`, đăng xuất trong trình thiết kế. `/admin` chưa đăng nhập thì chuyển sang `/login`.
  - Trang công khai của từng tiệm: `/s/<slug>` (chạy được ngay trên b2c.shirt.vn) hoặc tên miền con `<slug>.localhost` khi chạy local / `<slug>.<tên miền gốc>` trên server (biến `SHIRTVN_BASE_DOMAIN`). `/s/<slug>/design` đặt may, khách + đơn gắn vào tiệm đó. `/` (không có tiệm) là trang giới thiệu nền tảng.
  - Mỗi tiệm có trang kéo thả, trang mẫu, ảnh tải lên, khách, đơn riêng; tiệm này không sửa được dữ liệu tiệm kia. Khách nhận diện theo SĐT trong từng tiệm.
  - Bỏ mã quản trị chung `SHIRTVN_ADMIN_TOKEN`. Mật khẩu băm scrypt; phiên 30 ngày qua cookie HttpOnly; chống CSRF (kiểm nguồn request); khóa 15 phút khi sai mật khẩu nhiều lần.
  - DB cũ tự chuyển đổi khi chạy: khách/đơn cũ thuộc "tài khoản chung" (tenant 0); trang kéo thả + trang mẫu cũ (tenant `default`) để lại ở bảng `pages_legacy` / `storefronts_legacy`, không tự gán cho tiệm nào.
  - Code: `server/auth.js` (mật khẩu, phiên, cookie, CSRF, giới hạn thử), `server/db.js`, `server/index.js`; frontend `src/auth/Auth.tsx`, `src/shop.ts`, `src/api.ts`. Test `server/auth.test.js`.
  - Đã chạy thử local với 2 tiệm: đăng ký, lưu trang, đăng xuất, xem trang từng tiệm qua `/s/...` và tên miền con.
  - Review tự động nhiều góc nhìn (bảo mật đăng nhập, cô lập dữ liệu, chuyển đổi DB, frontend) có kiểm chứng chéo: sửa 9 lỗi đã xác nhận — gửi đăng nhập song song lách được giới hạn số lần thử; link chuyển hướng sau đăng nhập dẫn ra trang ngoài được; IPv6 đổi địa chỉ để né giới hạn (nay gộp theo dải /64, thêm giới hạn theo email); `www.` bị coi là tiệm; tải trang lỗi mà vẫn mở trang trống để sửa (lưu sẽ đè trang thật); trang mẫu mất bản nháp khi hết phiên; slug sai ở `/template` hiện trang mặc định; cấu hình Nginx cần `$http_host`.
  - Còn để lại (không sửa đợt này): khách nặc danh gửi cùng SĐT sẽ ghi đè thông tin khách cũ của tiệm (có từ trước); đăng ký lộ email nào đã có tài khoản; chưa giới hạn dung lượng ảnh mỗi tiệm; `/s/<slug-sai>/design` chỉ báo lỗi lúc gửi đơn.
- **2026-11-25 — Lấy giao diện, font và tông màu từ portfolio cũ của chủ vault** (repo `NhatProDev/portfolio-v3`, clone ở `portfolio-v3/` cạnh `shirtvn-b2c-web/`, chỉ để tham khảo):
  - Sửa lỗi font: font mặc định cũ (Jost, Bodoni Moda) **không có dấu tiếng Việt** nên chữ như "đề" bị vỡ dấu. Mặc định nay là Inter + Cormorant Garamond. Thêm 10 font có tiếng Việt (Manrope, Fraunces, Archivo, League Gothic, Libre Franklin, Big Shoulders, Hanken Grotesk, IBM Plex Mono, Old Standard TT, Spectral). 5 font cũ không dấu vẫn giữ để trang đã lưu không lỗi, nhưng có nhãn "(không dấu tiếng Việt)".
  - Thẻ **Kiểu** trong trình thiết kế: 16 **bộ chữ** phối sẵn (lấy từ portfolio, chỉ giữ bộ có tiếng Việt hoặc đã thay font) và 7 **tông màu** (6 bảng của portfolio + tông ShirtVN kem/đen/đỏ đô), bấm một lần áp cho cả trang. Code `src/builder/theme.ts`.
  - Trình thiết kế đổi sang khung tối trung tính ấm như editor portfolio (font giao diện Inter, viền chọn xanh #7c9cff, đường gióng hồng), có thanh công cụ nổi trên phần tử (cỡ chữ, căn lề, màu, lớp, nhân bản, xoá/ẩn), thẻ Thêm / Lớp / Kiểu, nhãn tên + kích thước khi kéo, đường gióng ⅓ và ⅔.
  - Thêm "Dòng nhỏ" (chữ hoa nhỏ giãn rộng), 3 kiểu nút (nền đặc / viền / chữ gạch chân), hiệu ứng hiện khi cuộn (hiện dần, trượt lên, phóng, trượt ngang, làm mờ).
  - Sửa thao tác: sửa liên tục một ô chỉ tính một bước hoàn tác; trên Tablet/Điện thoại, thêm phần tử chỉ hiện ở thiết bị đó và Delete chỉ ẩn ở thiết bị đó; đưa lớp lên/xuống bằng phím tắt.
  - Làm bằng workflow nhiều agent (đọc portfolio → làm theme → làm editor → review đối kháng); review xác nhận 7 lỗi, đã sửa hết (nặng nhất: phần tử có hiệu ứng ở cuối trang/sát mép có thể không bao giờ hiện). Đã thử trên trình duyệt.
- **2026-11-25 — Trang mẫu + nghiên cứu typography:**
  - Trang mẫu cho tiệm thử "Nhà May Đức Anh" (`/s/nha-may-duc-anh`), dựng theo prototype trang chủ chủ vault gửi: Newsreader + Inter, nền kem, ảnh Unsplash (giấy phép dùng miễn phí, kể cả thương mại; nhúng thẳng link, chưa tải về server). Có bố cục riêng cho điện thoại. Script tạo trang đang ở thư mục tạm của phiên, chưa đưa vào repo.
  - Workflow 9 agent (xem chữ trên web tiệm may / thời trang cao cấp như Drake's, Suitsupply, Anderson & Sheppard, Hermès, Kinfolk; gom nguyên tắc chữ tiếng Việt; rà font Google; 3 người thiết kế bộ chữ; tổng hợp; kiểm chứng). Thêm 26 font có dấu tiếng Việt (vd Brygada 1918, Commissioner, Be Vietnam Pro, Literata, Noto Serif Display, Inter Tight, Plus Jakarta Sans) và 15 bộ chữ mới đặt trước 16 bộ cũ trong thẻ Kiểu.
  - Nguyên tắc rút ra (dùng khi thiết kế tiếp): tiêu đề giãn dòng ≥ 1.15 vì dấu chồng (Ấ, Ữ); tiêu đề serif đậm 400–500; chữ hoa nhỏ (dòng nhỏ, nút) đậm 500–600, giãn 0.08–0.2em; đoạn văn ≥ 16px, giãn dòng 1.65; tối đa 2 họ font; font tương phản cao (Didone, Cormorant) chỉ dùng ≥ 28px.
  - Bản 3 của trang mẫu: đổi sang Brygada 1918 + Commissioner, thêm phần lời khách (chữ nghiêng), nhịp dọc đều (máy tính 112px giữa các phần, điện thoại 64px), ảnh bộ sưu tập dọc 3:4, số liệu xếp hàng trên điện thoại. Có agent review độc lập theo chuẩn typography (10 điểm, đã áp).
  - Sửa 3 lỗi builder: tablet tự thu nhỏ ép cỡ chữ tối thiểu 12px làm chữ tràn khung (nay thu nhỏ đều); padding nút bị cộng hai lần làm cắt chữ; tên bộ chữ trong thẻ xem trước bị bẻ giữa từ.
- **2026-11-25 — Nhiều trang cho mỗi tiệm + bộ trang mẫu mới:**
  - Builder có nhiều trang: API `GET/PUT/DELETE /api/page?page=<slug>` (bỏ trống = trang chủ), `GET /api/pages`; trang công khai `/s/<tiệm>/<slug>`; trình thiết kế có ô chọn trang, "+ Trang mới…", nút xoá trang (`/admin?page=<slug>`). Code ở `server/index.js`, `server/db.js`, `src/api.ts`, `src/shop.ts`, `src/builder/Site.tsx`, `src/builder/Editor.tsx`; test ở `server/auth.test.js`.
  - Thiết kế lại "Nhà May Đức Anh" lấy shirtbyhand.com làm tham khảo (chỉ lấy phong cách, không chép chữ/ảnh/logo): Inter mảnh (300) cho tiêu đề, nền trắng, xanh đá `#445566`, ô liu `#808369`, cát `#cec3af`, xám lục `#e3e3dc`, nút bo tròn, hero ảnh tràn lề phủ tối. 6 trang: trang chủ, `ao-so-mi`, `vai`, `quy-trinh`, `ve-chung-toi`, `dat-lich`; đầu/chân trang chung, menu điện thoại thành một hàng chữ. Script dựng trang vẫn ở thư mục tạm của phiên (chưa đưa vào repo).
  - Sau đó, theo yêu cầu chủ vault, mọi chữ và nút của 6 trang mẫu đều đậm (tối thiểu 600).
- **2026-11-26 — Trang giới thiệu nền tảng (`/`) làm lại:**
  - Nghiên cứu bằng agent model rẻ (sonnet): website builder (Squarespace, Wix, Framer, Webflow), bán hàng thời trang (Shopify, Big Cartel, Square), portfolio (Format, Pixpa, Cargo, Carrd), nền tảng Việt (Haravan, Sapo, LadiPage), SaaS theo ngành (Fresha, Owner.com), web tiệm may đo (Proper Cloth, Hockerty). Có agent đóng vai chủ tiệm may 52 tuổi ở Hà Nội để phản biện.
  - Trang mới là HTML tĩnh `shirtvn-b2c-web/public/landing/index.html`, kit ở `public/assets/`, 11 ảnh chụp sản phẩm thật ở `public/landing/`. Quy tắc trả trang cho `/` ở `vite.config.ts`.
  - Các phần: hero (ảnh trình sửa trang), tiệm mẫu Nhà May Đức Anh, 3 bước, thiết kế áo 3D, so với Zalo, 4 tính năng sửa trang, hỏi đáp (nói rõ cái chưa có: thanh toán online, trang xem đơn, giá, đặt lại mật khẩu), chân trang.
  - Màu và chữ đổi theo trang thiết kế áo (`/s/<tiệm>/design`): nền trắng, chữ `#111`, xám `#ececec`, nút đen góc vuông, chữ Montserrat, chân trang nền đen.
  - Gate của skill: PASS, 5 lỗi được miễn kèm lý do (bộ kiểm tra chỉ hiểu tiếng Anh, FAQ không cần hình…), ghi ở `shirtvn-b2c-web/.taste-skill/waivers.json`. Build và 15 test server qua.
  - Sau đó làm tinh hơn theo phong cách cleonstudio.com (chỉ lấy kiểu, giữ trắng-đen + Montserrat): tiêu đề mảnh hơn (500), nhãn nhỏ viết hoa giãn chữ trên hero ("Cho tiệm may đo · Bản thử nghiệm"), nút và menu chữ hoa nhỏ, số bước dạng "01", thẻ 3 bước bỏ khung, phần thiết kế áo thành dải nền đen. Gate PASS lại.
  - Theo yêu cầu chủ vault, thanh menu bỏ hết mục (Sản phẩm, Cách làm, So với Zalo, Hỏi đáp): chỉ còn logo, "Đăng nhập", "Tạo cửa hàng". Điện thoại vẫn có nút ☰ để tới "Đăng nhập". Gate PASS.
  - Hero đổi từ ảnh trình sửa sang video Remotion của chủ vault (dự án `shirtvn-video`, 60 giây, không tiếng). Nén thành `public/landing/promo-1920.mp4` (6,2 MB) và `promo-1280.mp4` (3,4 MB) cho điện thoại; có nút Tạm dừng/Phát, tự dừng khi cuộn qua, không tự chạy khi bật giảm chuyển động.
  - Thêm 3 tiệm mẫu mới, mỗi tiệm một kiểu bố cục (làm bằng workflow agent sonnet, đã xem lại ảnh chụp): Tiệm May Phố Cổ (cổ điển, căn giữa, chữ có chân, nền kem + đỏ rượu, 3 trang), Xưởng Áo Trắng (đen trắng kiểu Thuỵ Sĩ, tiêu đề lớn, có bảng giá và đặt lịch, 3 trang), Sơ Mi Gió Nam (một trang dài, khối màu xanh than / cát / đất nung, thẻ vải bo góc). Script ở `shirtvn-b2c-web/tools/templates/<tiệm>/`; tài khoản các tiệm mẫu ở `server/data/template-accounts.json` (local, không commit).
  - Phần tiệm mẫu Đức Anh trên trang giới thiệu đổi thành phần "Trang mẫu" (`#trang-mau`): 4 thẻ, mỗi thẻ ảnh đầu trang chủ của mẫu (máy tính) hoặc bản điện thoại (trên điện thoại), rê chuột thì ảnh trượt như cuộn trang, link "Xem mẫu". Gate PASS (miễn thêm 1 lỗi: 4 thẻ cùng cấu trúc là có chủ đích). Build và 15 test server qua.
- **2026-11-26 — Trình thiết kế `/admin` đổi giao diện theo cleonstudio.com:** nền gần đen `#0d0c0b`, đường kẻ mảnh `#2a2724`, chữ/nút chính màu kem `#ece6dc`, góc vuông, nhãn viết hoa giãn chữ, tên "ShirtVN" bằng Cormorant Garamond; phím tắt và phần giải thích bố cục thiết bị gập vào mục "Phím tắt" / "Chi tiết". Khung chọn phần tử vẫn màu xanh để dễ thấy. Code ở `src/builder/editor.css`, `Editor.tsx`, `panels.tsx`, font thêm ở `index.html`. Làm bằng agent sonnet. Ba ảnh chụp trình sửa trên trang giới thiệu đã chụp lại theo giao diện mới.
- **2026-11-27 — Trang giới thiệu đổi sang nền tối, phong cách Shopify; tên hiển thị là "Shirt.VN":**
  - Đầu trang: video nhà máy làm nền, phủ tối, cao khoảng 74% màn hình (`public/landing/factory-1600.mp4`, `factory-960.mp4`, không tiếng). Video giới thiệu Remotion chuyển xuống phần `#gioi-thieu` ngay bên dưới.
  - Chữ Inter (Shopify dùng Inter), tiêu đề mảnh 330, thân 420, nút 550. Nền `#0b0b0b`, nút trắng. Khoảng cách giữa các phần thu lại.
  - Dải "Tổ chức tin tưởng chúng tôi" chạy ngang dưới video đầu trang: Todd Snyder, Tommy Hilfiger, Shirtbyhand, BSCI, Oeko-Tex, amfori (`public/landing/logos/`). Phần so với Zalo đã bỏ.
  - Video giới thiệu (`shirtvn-video`) nay dài 73 giây, có cảnh bản đồ xưởng Hà Nội; nhạc nền thử bằng ACE-Step (`shirtvn-video/music/`, bản A–D).
  - Code đã đẩy lên GitHub, repo `shirtvn-b2c-web`, nhánh `main`. `shirtvn-video` chưa có repo.
- Chạy local: `npm install`, `npm run dev` + `npm run server` (Node ≥ 22.5).

## Việc tiếp theo
- [ ] Tạo repo cho `shirtvn-video`.
- [ ] Trang giới thiệu: xin phép dùng logo trên dải "Tổ chức tin tưởng" (Todd Snyder, Tommy Hilfiger…) trước khi quảng bá; thay `logos/bsci.png` bằng file gốc nét hơn; kiểm cỡ điện thoại. Trang app và video còn Montserrat, nền sáng.
- [ ] Chọn bản nhạc (A/B/C/D) cho video giới thiệu.
- [x] Đăng nhập nhà may + tách dữ liệu theo nhà may (2026-11-24).
- [ ] Builder đợt sau (lấy tiếp từ portfolio): chọn nhiều phần tử (kéo khung, căn đều, nhóm), slider/carousel ảnh, mẫu section dựng sẵn (Hero, bảng giá, quy trình may đo), tự lưu nháp.
- [x] Nhiều trang cho mỗi tiệm (2026-11-25).
- [ ] Trang giới thiệu: chủ vault chốt (1) có ghi "miễn phí trong giai đoạn thử nghiệm" không (hiện ghi "chưa có bảng giá"), (2) email/Zalo liên hệ cho chân trang, (3) có cần trang xem đơn cho chủ tiệm trước khi quảng bá không (hiện chủ tiệm chưa xem được đơn). Khi deploy thêm quy tắc Nginx cho `/` (README).
- [ ] Video giới thiệu ghi "Đăng ký miễn phí" / "Tạo cửa hàng miễn phí", còn trang giới thiệu ghi "chưa có bảng giá": chủ vault chốt một cách nói rồi sửa video (`shirtvn-video`) hoặc trang cho khớp.
- [ ] Cho chủ tiệm chọn một trang mẫu khi đăng ký ("Dùng mẫu này"): chép các trang của tiệm mẫu sang tiệm mới. Chưa làm.
- [ ] Đưa script dựng Nhà May Đức Anh từ thư mục tạm vào `tools/templates/nha-may-duc-anh/` như ba mẫu kia.
- [ ] Sơ Mi Gió Nam: nút "Nhắn Zalo" đang dẫn về trang chủ (chưa có Zalo thật); builder chưa có link neo tới một phần trong trang.
- [ ] Builder: đầu/chân trang dùng chung giữa các trang (hiện mỗi trang chép riêng, sửa một chỗ phải sửa cả 6), menu dạng nút ba gạch cho điện thoại.
- [ ] Sau đăng nhập: quên mật khẩu / đổi mật khẩu (cần gửi email), xác minh email, mẫu khởi đầu, tên miền riêng của tiệm (không phải tên miền con).
- [ ] Deploy bản có đăng nhập: chạy `server/index.js` trên VM, Nginx chuyển `/api` sang Node kèm header `Host`, `X-Forwarded-*`, đặt `SHIRTVN_TRUST_PROXY=1` (chi tiết trong README của repo). Muốn tên miền con: DNS `*.b2c.shirt.vn` + chứng chỉ wildcard.
- [ ] Storefront đợt sau: trang Shop (lọc vải/họa tiết/màu/giá), trang sản phẩm, trang Measurements theo design; tải ảnh lên; đăng nhập nhà may; tách nhà may theo tên miền; dashboard (đơn, doanh thu).
- [ ] Deploy bản mới: Nginx `b2c.shirt.vn` cần `try_files $uri /index.html;` để mở được `/design`, `/admin`.
- [ ] API trên server: `location /api` của b2c.shirt.vn đang trỏ `localhost:8001` — là app khác, không phải API của repo (mặc định cổng 8787) → nút đặt hàng trên trang thật chưa chạy. Cần chạy `server/index.js` trên VM (Node ≥ 22.18, pm2) và cho khớp cổng.
- [ ] `www.b2c.shirt.vn` chưa có bản ghi DNS (nếu cần thì thêm rồi chạy lại certbot cho www).
- [ ] Trang quản trị nhà may: trả lời câu hỏi "API backend nhà máy" là server trong repo này hay hệ thống B2B riêng (nút Approve có gửi đơn sang B2B không, có tài liệu API không), rồi viết design và làm.
- [ ] Xin tài liệu backend API B2B từ chú (endpoint, xác thực, định dạng đơn hàng, các loại measurement type khác).
- [ ] Áo 3D: thân/tay đã có lưới mô phỏng vải (buổi 4). Còn lại: dựng cổ áo dày và đẹp hơn (có thể nhờ người làm CLO3D), lưới riêng cho từng fit, xem xét gộp nhánh `shirt-3d-cloth` vào `main`.
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
- **2026-11-16 — Backend tạm: Node + SQLite trong cùng repo, không thêm thư viện.** Lý do: cần lưu khách/đơn ngay để demo; đổi sang DB khác chỉ phải sửa `server/db.js`.
- **2026-11-16 — Mỗi nhà may tách theo tên miền riêng, độc lập hoàn toàn; mã khách có tiền tố theo tiệm (vd ShirtbyHand → `SBH-0001`).** Lý do: chủ vault chốt; các tiệm không quen biết nhau, tất cả nối chung API backend nhà máy. Sau này tiệm tự tùy biến trang (ảnh, logo) — chưa làm đợt này.
- **2026-11-21 — Host trên Google Cloud VM (svr2) + Nginx, dùng chung VM với các trang shirt.vn khác.** Lý do: hạ tầng có sẵn của công ty.
- **2026-11-24 — GitHub chỉ để đồng bộ code giữa nhiều máy; deploy vẫn làm tay (build → `html.zip` → SSH-in-browser), không dùng deploy tự động.** Lý do: chủ vault quản trị VM bằng giao diện Google (SSH-in-browser) và muốn tự kiểm soát lúc đưa lên trang thật.
- **2026-11-24 — Trang nhà may làm bằng trình kéo thả tự do (định vị tuyệt đối), mỗi thiết bị một bố cục, trang thật phóng/thu theo bề rộng thiết kế.** Lý do: chủ vault muốn trang trống kéo thả như portfolio, thiết kế được cho PC / tablet / điện thoại. Bản section trước giữ ở `/template`.
- **2026-11-24 — Tách nhà may bằng đăng nhập.** Lý do: chủ vault chốt.
- **2026-11-24 — Trang nhà may dựng từ cấu hình section (JSON) thay vì trang cố định; trình sửa tự viết, kéo thả bằng HTML5 có sẵn, không thêm thư viện.** Lý do: nhà may cần tự kéo thả/tùy biến; cùng một cấu hình vừa render trang thật vừa xem trước trong admin.
- **2026-11-14 — Ảnh chụp thật chỉ hiện khi cấu hình khớp ảnh, còn lại dùng SVG.** Lý do: ảnh chụp không đổi theo cổ/tay/túi, hiện sai sẽ gây hiểu nhầm.
- **2026-11-24 — Tách nhà may bằng tài khoản đăng nhập (email + mật khẩu), mỗi tài khoản một cửa hàng.** Lý do: chủ vault chốt; đơn giản nhất để mỗi tiệm tự thiết kế trang riêng.
- **2026-11-24 — Địa chỉ tiệm: `/s/<slug>` và tên miền con `<slug>.<tên miền>`; ghi dữ liệu luôn theo phiên đăng nhập, không theo tên miền.** Lý do: `/s/<slug>` chạy ngay trên b2c.shirt.vn không cần DNS; tên miền con cho tiệm có địa chỉ đẹp; ghi theo phiên thì không ai sửa được trang tiệm khác bằng cách đổi tên miền.
- **2026-11-24 — Phiên đăng nhập bằng cookie HttpOnly lưu ở server (SQLite), không dùng JWT, không thêm thư viện.** Lý do: đăng xuất là hủy phiên ngay; JavaScript trên trang không đọc được cookie; giữ nguyên hướng "không thêm thư viện".
- **2026-11-24 — Dữ liệu trang cũ (tenant `default`) không tự gán cho tiệm nào, giữ ở bảng `*_legacy`.** Lý do: không biết tiệm nào là chủ; tránh để tiệm đăng ký đầu tiên nhận trang của người khác.
- **2026-11-25 — Lấy từ portfolio cũ: font, bộ chữ, tông màu, giao diện editor, thanh công cụ nổi; không lấy bố cục section/flow, trình soạn chữ Tiptap, thư viện kéo thả dnd-kit.** Lý do: chủ vault muốn dùng lại font + tông của portfolio; phần không lấy trái với mô hình định vị tự do của builder hoặc phải thêm thư viện.
- **2026-11-25 — Chỉ dùng font có dấu tiếng Việt cho mặc định và bộ chữ phối sẵn.** Lý do: tiệm may ở Việt Nam, font thiếu dấu làm vỡ chữ.
- **2026-11-25 — Font mới chỉ thêm khi đã thử URL Google Fonts trả 200 và có bộ ký tự tiếng Việt.** Lý do: một tham số font sai làm hỏng cả URL tải font gộp; nhiều font Google đẹp (Libre Caslon, Bodoni Moda, Jost) không có dấu tiếng Việt.
- **2026-11-25 — Trang mẫu dùng Brygada 1918 (tiêu đề, đậm 400, một dòng nghiêng làm điểm nhấn) + Commissioner (chữ thường).** Lý do: chủ vault cho đổi font tự do miễn đẹp; nghiên cứu chấm cặp này hợp tiệm may lâu năm nhất (dáng Caslon như Drake's), dấu tiếng Việt chắc nét trên nền kem. Newsreader nay tải kèm trục opsz.
- **2026-11-25 — Trang mẫu đổi sang Inter (300 tiêu đề) + bảng màu xanh đá / ô liu / cát theo tham khảo shirtbyhand.com, thay bản Brygada.** Lý do: chủ vault yêu cầu lấy trang đó làm chuẩn font và màu.
- **2026-11-26 — Trang giới thiệu là HTML tĩnh riêng, không phải component React.** Lý do: CSS toàn cục của app (`.card`, `.grid`, `.panel`, `.sheet`) đụng bộ kit; trang tĩnh nhẹ hơn và máy tìm kiếm đọc được nội dung (SPA trả HTML rỗng).
- **2026-11-26 — Trang giới thiệu dùng màu và chữ của trang thiết kế áo (trắng, đen, xám, Montserrat), thay bản kem + đỏ đất + Geist.** Lý do: chủ vault yêu cầu; nền tảng và trang thiết kế áo trông cùng một sản phẩm. Skill thiết kế mặc định tránh Montserrat, nhưng yêu cầu của chủ vault được ưu tiên.
- **2026-11-26 — Trang giới thiệu giữ trắng-đen, chỉ lấy chi tiết của cleonstudio (nhãn viết hoa giãn chữ, nút vuông chữ nhỏ, một dải tối); `/admin` lấy cả bảng màu tối + kem của cleonstudio.** Lý do: chủ vault chọn giữ trắng-đen cho trang tổng để khớp trang thiết kế áo; trình sửa vốn là khung tối nên hợp bảng màu cleonstudio. Chỉ lấy phong cách, không chép chữ, ảnh hay logo của họ.
- **2026-11-26 — Trang giới thiệu không ghi số khách, logo, lời khen hay giá; nói thẳng những gì chưa làm.** Lý do: chưa có khách thật, giá chưa chốt; chủ tiệm may lớn tuổi tin trang nói thật hơn.
- **2026-11-26 — Ảnh trên trang giới thiệu là ảnh chụp màn hình thật của sản phẩm (trình sửa, tiệm mẫu, trang thiết kế áo).** Lý do: cho chủ tiệm thấy đúng thứ họ sẽ dùng; không dùng ảnh minh hoạ chung chung.
- **2026-11-26 — Video hero đặt trong dải nền đen, hiện trọn khung (`object-fit: contain`), không cắt.** Lý do: video có chữ ở sát mép; cắt cho vừa khung sẽ mất chữ.
- **2026-11-26 — Trang mẫu là các tiệm hư cấu dựng bằng chính trình kéo thả, không ghi đánh giá, số khách hay lời khen giả.** Lý do: cho chủ tiệm thấy trình kéo thả làm được những bố cục nào; giữ nguyên tắc trang chỉ nói thật.
- **2026-11-26 — Không sửa video của chủ vault, dù có chữ "miễn phí" lệch với trang giới thiệu.** Lý do: giá là việc chủ vault chốt; video là sản phẩm của chủ vault.
- **2026-11-25 — Nhiều trang lưu theo slug trong bảng `pages` có sẵn, chọn trang bằng `?page=`, tối đa 20 trang/tiệm, cấm slug trùng đường dẫn hệ thống (design, admin, api…).** Lý do: bảng đã có khoá (tiệm, slug) nên không phải đổi DB; đổi trang trong trình sửa bằng tải lại trang để dùng lại cảnh báo "chưa lưu" có sẵn.

## Câu hỏi còn mở
- Tài liệu API B2B nằm ở đâu, xác thực thế nào?
- Phần quản lý của nhà may (tùy biến trang, tên miền, vải, khách hàng) do backend nào lưu: dùng chung backend B2B hay cần backend B2C riêng?
- Tên miền riêng cho từng nhà may sẽ triển khai thế nào (subdomain, custom domain)? — Đã chốt: mỗi tiệm một tên miền; chi tiết kỹ thuật chưa làm.
- "API backend nhà máy có sẵn" là server trong repo này hay hệ thống B2B (mtm.shirt.vn)? Duyệt đơn có tự gửi sang B2B không?
- Ngoài "Body Measurement" còn những loại số đo nào?
- Deadline: chưa có.

## Tài nguyên
- Code: GitHub `NhatProDev/shirtvn-b2c-web` (private); local trên máy Windows: `C:\KhanhNhat\shirtvn b2c web` (bản cũ ở `D:\file cua choe 2\2. Projects\13\shirtvn-b2c-web`). Trang thật: https://b2c.shirt.vn. Trang thiết kế áo: `src/App.tsx`, `src/components/`, dữ liệu mẫu ở `src/data/`.
- Tài liệu API: chưa có.
