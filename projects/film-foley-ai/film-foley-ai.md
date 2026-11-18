---
type: project
title: Film Foley AI (sound design bằng AI)
status: in-progress
created: 2026-11-19
updated: 2026-11-19
tags:
  - project
  - film
  - sound-design
  - foley
  - ai
---

# Film Foley AI

## Mô tả
Thử nghiệm dùng Claude làm **sound designer / sound editor** cho phim: Claude tự spotting (lập cue sheet từ hình), tạo Foley, dựng theo timecode, mix và xuất theo chuẩn phát hành. Budget **0$**.

Demo đang dùng: 60 giây đầu MV **"Day & Night" – Jung Seung-hwan (OST Start-Up)**, YouTube `2dEeiY_w3xE`. Chỉ dùng để test riêng tư, không đăng lại (bản quyền thuộc hãng phát hành).

## Phạm vi (người dùng đã chốt)
- **Chỉ Foley "primary":** bước chân, giấy, vải, đồ vật (corndog, chai sốt, túi nhựa, máy nghe nhạc), ambience nền, mưa.
- **Không làm:** whoosh và các hiệu ứng điện ảnh, thoại, nhạc. Audio gốc của MV bị thay hoàn toàn.

## Mục tiêu
Đạt chất lượng gần chuẩn industry với chi phí 0$. Bàn giao gồm:
- Cue sheet
- Stem tách riêng (FEET / PROPS / CLOTH / BG)
- 48 kHz / 24-bit, **-24 LKFS**, true peak **≤ -2 dBTP**
- Video đã ghép âm thanh

## Cách làm (quy trình)
1. **Lấy video:** dùng `yt-dlp --download-sections "*0-60"`, bản 720p. ffmpeg lấy từ gói `imageio-ffmpeg`, vì máy không cài sẵn ffmpeg.
2. **Spotting:**
   - Dùng ffmpeg `select='gt(scene,0.3)'` để tìm các điểm cắt cảnh.
   - Ghép frame thành contact sheet ở 2 fps để xem toàn bộ, và ở 8 fps cho các điểm cần sync chính xác.
   - Kết quả: `code/cue_sheet.csv` (35 cue) và `code/shots.csv` (24 shot kèm prompt).
3. **v1, tổng hợp thuật toán** (`code/foley_build.py`):
   - Đọc cue sheet và tổng hợp từng âm thanh bằng numpy/scipy.
   - Xuất 4 stem và mix đạt -24 LUFS.
   - Chất lượng mới ở mức temp track, nghe còn "điện tử".
4. **v2, AI video-to-audio bằng MMAudio** (`code/batch_gen.py`):
   - Dùng model `small_44k`, tạo 2 seed cho mỗi shot.
   - Prompt phủ định: music, speech, whoosh, impact.
5. **Chấm điểm mà không cần nghe** (`code/analyze_gen.py`):
   - Đo loudness.
   - Đo độ harmonic bằng HPSS, để phát hiện nhạc hoặc giọng lọt vào.
   - Dùng pyin để phát hiện tiếng nói.
   - So onset với các hit point trong cue sheet.
   - Kết quả ghi ra `gen_scores.csv` và tự chọn seed tốt nhất cho mỗi shot.
6. **Dựng v2** (`code/assemble_v2.py`):
   - Lớp chính là audio MMAudio, cân loudness theo loại cảnh: ngoài trời ban ngày -27, trong nhà -33, mưa -25 LUFS.
   - Thêm hit âm thanh tổng hợp của v1 ở những chỗ AI không khớp sync (align < 0.6).
   - Nếu shot của AI có nhạc hoặc giọng lọt vào thì thay cả shot bằng v1.
   - Chuẩn hóa -24 LUFS, giới hạn true peak.
   - Có thể ép chọn seed bằng tham số, ví dụ `python assemble_v2.py S01=1`.

## Trạng thái hiện tại (2026-11-19)
- ✅ **v1** xong cho cả 60 giây.
- ⏸️ **v2 đã tạm dừng theo yêu cầu.** MMAudio mới tạo xong **S01, S02, S03 và S11** (mỗi shot 2 seed).
- ✅ Đã có preview 0–10 giây cho cả v1 và v2 để so sánh A/B. Người dùng **chưa phản hồi** sau khi nghe.
- Chọn seed hiện tại:
  - S01 = seed 1, vì seed 2 có dấu hiệu tiếng người (voiced 0.14).
  - S02 = seed 2. Lưu ý: số tiếng "rộp" nhiều hơn số lần cắn trên hình.
  - S03 = seed 2.
  - S11 = seed 2.
- Đo được: bản mix v2 đạt -24.3 LUFS, true peak khoảng -2.5 dBTP.

## Việc tiếp theo
- [ ] Hỏi phản hồi của người dùng về preview 0–10s (v1 và v2).
- [ ] Nếu tiếp tục v2: chạy batch cho S04–S10 và S12–S24. Script tự bỏ qua shot đã có file. Trên CPU mất khoảng 45–50 phút.
- [ ] Chạy lại `analyze_gen.py`, rồi `assemble_v2.py`, rồi render toàn bộ 60 giây.
- [ ] Cân nhắc nâng cấp:
  - Dùng thư viện Foley thu thật miễn phí: Sonniss GDC (dùng thương mại được), Freesound CC0 (cần người dùng tự tạo API key).
  - Làm project REAPER kèm `reaper-mcp` để người dùng chỉnh tay.

## Cài đặt lại trên máy mới
1. Python 3.11. Cài các gói:
   `pip install yt-dlp imageio-ffmpeg numpy scipy soundfile pyloudnorm librosa`
2. **MMAudio** phải nằm ở **đường dẫn ngắn**, ví dụ `C:\Users\<user>\sfx-tools\`. Thư mục phiên của Claude có đường dẫn quá dài, làm git clone trên Windows bị lỗi "Filename too long".
   - `git clone https://github.com/hkchengrex/MMAudio`
   - Tạo venv, rồi `pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1`
   - Sau đó `pip install -e MMAudio`. Lệnh này tự nâng torch lên 2.15, phải cài lại 2.5.1.
   - Đặt `batch_gen.py` và `shots.csv` vào `sfx-tools\`.
   - Cắt video thành từng clip theo `shots.csv`, lưu vào `sfx-tools\shots\<id>.mp4`.
   - Chạy từ trong thư mục `MMAudio\`: `..\venv\Scripts\python ..\batch_gen.py small_44k ..\shots.csv [S04,S05...]`
   - Weights tự tải khi chạy lần đầu (khoảng 4 GB, từ Hugging Face và GitHub releases).
3. Các đường dẫn `C:\Users\ACER\sfx-tools\gen\small_44k` đang **viết cứng** trong `analyze_gen.py` và `assemble_v2.py`. Sửa lại nếu máy khác dùng đường dẫn khác.

## Quyết định
- **Tổng hợp thuật toán cho v1:** Higgsfield `generate_audio` bị chặn bởi auto-mode, và tài khoản có 0 credit.
- **MMAudio chạy trên CPU:** máy là RTX 3050 Ti 4 GB, nhưng `download.pytorch.org` bị chặn SSL từ mạng nhà, nên không cài được bản PyTorch CUDA. PyTorch trên PyPI cho Windows chỉ có bản CPU.
- **Chọn `small_44k`:** VRAM không đủ cho bản large (cần khoảng 6 GB). Bản 44k có dải tần rộng hơn bản 16k, tốt hơn cho tiếng giấy và tiếng mưa. Giới hạn: âm thanh chỉ tới khoảng 16 kHz.
- **Không dùng HunyuanVideo-Foley:** cần quá nhiều VRAM.
- **Code để trong vault là ngoại lệ:** người dùng đồng ý ngày 2026-11-19, để máy khác chạy tiếp được. Không đưa video hay audio lên repo vì lý do bản quyền và dung lượng.
- **Không dùng thư viện BBC SFX:** giấy phép chỉ cho dùng phi thương mại.

## Câu hỏi còn mở
- Chất lượng v2 so với v1 nghe thế nào? Có tiếng người hay nhạc lọt vào không? Tiếng cắn ở S02 có bị thừa không?
- Sẽ làm hết 4 phút của MV, hay chuyển sang phim thật của người dùng?

## Tài nguyên
- Code và dữ liệu: `projects/film-foley-ai/code/` (trong vault).
- Máy ACER, không nằm trong repo:
  - MMAudio và venv: `C:\Users\ACER\sfx-tools\`
  - Audio đã tạo: `C:\Users\ACER\sfx-tools\gen\small_44k\`
  - Video nguồn, stem v1/v2, bản mix và preview: `C:\Users\ACER\sfx-tools\project-media\`
- Giấy phép: code MMAudio theo MIT, **weights theo CC-BY-NC 4.0 (chỉ dùng phi thương mại)**.
- Nghiên cứu công cụ AI sound design (11/2026): ElevenLabs SFX/MCP, Mirelo SFX 2.0, Sony Woosh, Foley-Omni, Adobe MultiFoley, reaper-mcp, protools-mcp (chỉ chạy trên macOS).
