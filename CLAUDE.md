# SecondBrain — hướng dẫn cho Claude

Đây là second brain của chủ vault (người Việt, nói tiếng Việt). Mục đích: gom project, việc cần làm và kiến thức vào một chỗ để không phải giải thích lại mỗi khi đổi thiết bị.

## Khi bắt đầu một phiên làm việc
1. Đọc `projects/index.md` để biết có những project nào và trạng thái.
2. Với project người dùng nhắc tới, đọc ghi chú chính của project đó trong `projects/<tên-project>/`.
3. Dựa trên đó tiếp tục công việc; đừng hỏi lại những điều đã ghi trong vault.

## Cấu trúc
- `projects/` — mỗi project một thư mục. Ghi chú chính cùng tên thư mục là "trang bàn giao": mô tả, mục tiêu, tiến độ, việc tiếp theo, quyết định, tài nguyên.
- `inbox/` — nguồn thô chờ xử lý (do plugin claude-obsidian quản lý).
- `wiki/` — kiến thức đã xử lý (do plugin claude-obsidian quản lý). Không sửa tay các file `wiki/` hoặc `.vault-meta/`, `.raw/`.

## Quy ước
- Viết tiếng Việt. Giữ ghi chú ngắn, cụ thể.
- Sau mỗi buổi làm việc có tiến triển, cập nhật mục "Trạng thái hiện tại", "Việc tiếp theo" và ngày `updated` trong trang bàn giao của project.
- Ghi quyết định kèm lý do vào mục "Quyết định".
- Không lưu mật khẩu, khóa API hay thông tin nhạy cảm trong vault.
- Không chép code vào vault; chỉ ghi nơi code nằm (đường dẫn hoặc link repo).

## Lưu ý kỹ thuật
Plugin claude-obsidian chỉ ghi được vault khi Claude Code chạy trong WSL/Linux/macOS. Trên Windows thuần, chỉ đọc và sửa file Markdown trong `projects/` trực tiếp.
