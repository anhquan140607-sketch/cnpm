# Hướng dẫn Git và GitHub cho nhóm dự án

Tài liệu này hướng dẫn từng bước làm việc với GitHub cho dự án Film Photography Contest Management Platform (5 thành viên, 8 tuần). Nội dung dựa trên slide Git & GitLab Guides của môn học, chuyển sang thao tác trên GitHub.

Quy ước vai trò (cần nhóm xác nhận): **1 Maintainer** (Scrum Master, giữ quyền merge vào `main`) và **4 Developer**.

---

## Phần 1. Việc của Maintainer (làm một lần)

### 1.1 Tạo repository

1. Đăng nhập GitHub, bấm **+ → New repository**.
2. Repository name: `film-contest-platform`.
3. Chọn **Private**.
4. Tick **Add a README file**.
5. Add .gitignore: chọn template phù hợp (Node, hoặc VisualStudio nếu dùng ASP.NET Core).
6. Bấm **Create repository**.

### 1.2 Mời thành viên

1. Vào repo → **Settings → Collaborators → Add people**.
2. Nhập username hoặc email GitHub của 4 thành viên và giảng viên (nếu cần xem), chọn quyền **Write** cho developer.
3. Mỗi người nhận email mời và phải bấm **Accept invitation**.

### 1.3 Bảo vệ nhánh main

Mục tiêu giống slide: developer được đẩy code lên nhánh riêng, **chỉ Maintainer mới merge vào `main`**.

1. Vào **Settings → Branches → Add branch protection rule** (hoặc **Rules → Rulesets** trên giao diện mới).
2. Branch name pattern: `main`.
3. Tick **Require a pull request before merging**.
4. Tick **Require approvals**, đặt số approval là `1`.
5. Tick **Do not allow bypassing the above settings** nếu muốn áp dụng cho cả Maintainer.
6. Bấm **Create / Save changes**.

Lưu ý: repo Private trên gói miễn phí có thể hạn chế một số tùy chọn bảo vệ nhánh. Nếu không bật được, nhóm thống nhất quy ước bằng lời: không ai push thẳng vào `main`.

### 1.4 Tạo cấu trúc thư mục ban đầu

Theo sơ đồ trên bảng của giảng viên:

```
film-contest-platform/
├── Docs/          các file .md của dự án
├── BE/            backend
├── FE/            frontend
├── README.md
├── Check_list.md
└── Skills/
```

Cách nhanh nhất: giải nén thư mục `film-contest-platform` tôi gửi kèm, rồi làm theo mục 2 và 3 bên dưới để đẩy lên repo.

---

## Phần 2. Việc của mỗi thành viên (làm một lần)

### 2.1 Cài Git và cấu hình

Tải Git tại https://git-scm.com rồi chạy:

```bash
git config --global user.name "Ho Ten Cua Ban"
git config --global user.email "email-dang-ky-github@example.com"
git config --global init.defaultBranch main
```

Kiểm tra:

```bash
git config --list
```

### 2.2 Clone repository

```bash
git clone https://github.com/<owner>/film-contest-platform.git
cd film-contest-platform
```

Khi push lần đầu, GitHub yêu cầu đăng nhập. Dùng **Personal Access Token** (Settings → Developer settings → Personal access tokens) thay cho mật khẩu, hoặc cài **GitHub Desktop** / **Git Credential Manager** để đăng nhập bằng trình duyệt.

---

## Phần 3. Quy trình làm việc hằng ngày

Mỗi công việc trong Jira (ví dụ `FILM-12`) tương ứng một nhánh và một pull request.

### Bước 1. Cập nhật code mới nhất

```bash
git checkout main
git pull
```

### Bước 2. Tạo nhánh cho công việc

Tên nhánh = mã Jira + mô tả ngắn.

```bash
git checkout -b FILM-12-film-roll-form
```

### Bước 3. Làm việc và kiểm tra thay đổi

```bash
git status
git diff
```

### Bước 4. Đưa file vào staging và commit

```bash
git add Docs/01-project-scope.md
git commit -m "FILM-12: add film roll form"
```

- Muốn thêm toàn bộ thay đổi: `git add -A` (kiểm tra `git status` trước để không đưa file rác).
- Commit message luôn bắt đầu bằng mã Jira, viết ngắn, nói rõ việc đã làm.
- Sửa commit cuối nếu chưa push: `git commit --amend -m "FILM-12: ..."`.

### Bước 5. Đẩy nhánh lên GitHub

Lần đầu của nhánh:

```bash
git push -u origin FILM-12-film-roll-form
```

Các lần sau chỉ cần:

```bash
git push
```

### Bước 6. Tạo Pull Request

1. Vào repo trên GitHub, bấm **Compare & pull request** (hoặc **Pull requests → New pull request**).
2. Base: `main`, compare: nhánh của bạn.
3. Title: `FILM-12: add film roll form`. Phần mô tả ghi những gì đã làm và cách kiểm tra.
4. Ở **Reviewers**, chọn ít nhất 1 bạn trong nhóm (module xác thực và chấm điểm chọn 2 người).
5. Bấm **Create pull request**.

### Bước 7. Review và merge

- Người review đọc code, để comment, rồi bấm **Review changes → Approve** (hoặc **Request changes**).
- Sau khi đủ approval, **Maintainer** bấm **Merge pull request**, sau đó **Delete branch**.
- Các bạn còn lại chạy `git checkout main && git pull` để lấy code mới.

---

## Phần 4. Xử lý tình huống thường gặp

### Push bị từ chối vì người khác đã push trước

```bash
git pull
```

Nếu có conflict, Git đánh dấu trong file như sau:

```
<<<<<<< HEAD
nội dung của bạn
=======
nội dung của người khác
>>>>>>> origin/main
```

Cách xử lý: mở file, sửa thành nội dung đúng và xóa các dòng `<<<<<<<`, `=======`, `>>>>>>>`, rồi:

```bash
git add <file-da-sua>
git commit -m "FILM-12: resolve merge conflict"
git push
```

### Cập nhật nhánh của bạn với main mới nhất

```bash
git checkout main
git pull
git checkout FILM-12-film-roll-form
git merge main
```

### Hủy commit cuối chưa push

```bash
git reset --soft HEAD~1    # giữ thay đổi trong staging
git reset HEAD~1           # giữ thay đổi trong thư mục làm việc
git reset --hard HEAD~1    # xóa luôn thay đổi (cẩn thận)
```

### Khôi phục file về bản commit cuối

```bash
git checkout -- ten_file
```

(Hoặc `git restore ten_file` trên Git mới.)

### Cảnh báo

- Không dùng `git push --force` lên `main` hoặc nhánh người khác đang dùng.
- Không commit file bí mật: API key (OpenAI), chuỗi kết nối database, file `.env`. Thêm chúng vào `.gitignore` và dùng biến môi trường.

---

## Phần 5. Xem lịch sử và so sánh

```bash
git log --oneline            # lịch sử commit
git branch -a                # danh sách nhánh
git diff --staged            # thay đổi đã staged
git diff main FILM-12-film-roll-form   # so sánh hai nhánh
```

---

## Phần 6. Tag và milestone

Mỗi sprint kết thúc, Maintainer gắn tag cho bản phát hành:

```bash
git checkout main
git pull
git tag -a v0.1 -m "Sprint 1: auth, RBAC, master data"
git push origin v0.1
```

Gợi ý tag theo sprint: `v0.1` (Sprint 1), `v0.2` (Sprint 2), `v0.3` (Sprint 3), `v1.0` (Sprint 4, bản nộp).

Trên GitHub: vào **Releases → Draft a new release** để chọn tag và ghi chú phát hành. **Issues → Milestones** dùng để tạo mốc theo sprint nếu nhóm muốn theo dõi cả trên GitHub (công việc chính vẫn quản lý ở Jira).

---

## Phần 7. Làm việc với thư mục Docs

Theo sơ đồ của giảng viên, thành viên **đẩy các file .md vào thư mục Docs bằng Git**.

1. Tạo nhánh: `git checkout -b FILM-30-update-scope-doc`.
2. Sửa hoặc thêm file `.md` trong `Docs/`.
3. `git add Docs/` rồi commit, push, tạo pull request như Phần 3.
4. Đặt tên file có số thứ tự, chữ thường, nối bằng dấu gạch ngang, ví dụ `05-test-plan.md`.
5. Khi sửa tài liệu, cập nhật tick trong `Check_list.md` nếu liên quan.

Mỗi tài liệu hiện có trong `Docs/`:

| File | Nội dung |
| --- | --- |
| `01-project-scope.md` | Major Features, Limitations & Exclusions |
| `02-scope-estimation.md` | WBS, độ phức tạp, ưu tiên, effort (man-hours) |
| `03-management-approach.md` | Mục tiêu, rủi ro, quy trình Scrum, Jira, chất lượng |
| `04-git-workflow-guide.md` | Tài liệu này |
| `05-srs.md` | Đặc tả yêu cầu phần mềm (SRS) |

---

## Phần 8. Liên kết GitHub với Jira

1. Luôn ghi mã Jira (`FILM-12`) trong tên nhánh, commit và tiêu đề pull request.
2. Trong Jira, cài app **GitHub for Jira** (Apps → Explore more apps) và kết nối với repo, khi đó các nhánh, commit và PR hiện ngay trong issue.
3. Khi PR được merge, chuyển issue sang **Done** (hoặc cấu hình tự động trong Jira Automation).

Mã dự án `FILM` ở trên là ví dụ. Hãy thay bằng project key thật trong Jira của nhóm.

---

## Checklist nhanh trước khi tạo Pull Request

- [ ] Nhánh tạo từ `main` mới nhất
- [ ] Tên nhánh và commit có mã Jira
- [ ] `git status` sạch, không có file rác hoặc file bí mật
- [ ] Đã chạy thử và test phần mình làm
- [ ] Đã chọn reviewer
