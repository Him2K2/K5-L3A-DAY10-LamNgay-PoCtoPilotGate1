# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `LamNgay`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-LamNgay-PoCtoPilotGate1`
- Thẻ sự cố của nhóm: [S3 · Hãng miền Tây bị phạt vì bão](incidents/S3/card.md).

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |     Hồ Xuân Vũ      |  2A202603406    |   kỹ sư cổng  |             |
|   2 |     Phan Hải Đăng      |  2A202603409    |  kỹ sư cổng    |             |
|   3 |       Nguyễn Quang Trung    |  2A202603389    |  Vận hành và pháp lý   |             |
|   4 |    Trần Thanh Tùng       |  2A202603418    |   Sản phẩm và kinh doanh  |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoXuanVu-2A202603406

### Phần việc phụ trách

Kỹ sư cổng; phụ trách phần cổng trong `lab10/guards.py` và đối chiếu các điều kiện cổng ở Phiếu B. Xác nhận phạm vi thực tế trước khi ghi đóng góp đã hoàn thành.

### Đóng góp cụ thể

Chưa có bằng chứng gắn đóng góp cá nhân với log hoặc commit trong tài liệu hiện có; bổ sung công việc thực tế đã làm.

### Bằng chứng

Chưa xác nhận; bổ sung mã commit, mã lần chạy (`runs/<mã>`) hoặc mục phiếu liên quan.

### Exit ticket

Một điều học được: ... · Một điều còn chưa chắc: ...

## PhanHaiDang-2A202603409

### Phần việc phụ trách

Em phụ trách cổng hệ thống và kiểm tra hồi quy ở vòng 2 cho thẻ S3.

### Đóng góp cụ thể

Em tiếp nhận gói S3, bổ sung kiểm tra đúng kiện và hãng trước khi ghi lỗi, rồi giới hạn ghi tự động ở hai lỗi mỗi hãng mỗi ngày. Khi chạm trần, cổng chặn ghi thêm lỗi và vẫn giữ kết quả hoàn phí của khách. Em bổ sung chỉ số `carrier_strike_cap_hit_rate` để vận hành biết khi nào cần đối soát, đồng thời ghi kết quả kiểm thử vào Phiếu C.

### Bằng chứng

Commit `3a365e6` tiếp nhận gói S3, commit `91bad6d` ghi nhận phần hoàn thiện Khối 3. Phiếu C mục C0 ghi S3 đạt 60/60 lượt và bộ nền đạt 110/110 lượt sau sửa. Số lỗi hãng oan trên S3 giảm từ 10 ở mốc `prepared` xuống 0 ở mốc `after`.

### Exit ticket

Một điều em học được là kiểm tra đúng từng ticket vẫn có thể bỏ sót rủi ro tích lũy theo hãng trong ngày. Điều em còn chưa chắc là sổ lỗi trên pilot thật có cập nhật đủ nhanh để giữ đúng trần khi nhiều ticket được xử lý đồng thời.

## NguyenQuangTrung-2A202603389

### Phần việc phụ trách

Vận hành và pháp lý; phụ trách rà soát các điều kiện vận hành, giám sát, dừng và tác động pháp lý trong Phiếu B/C. Xác nhận phạm vi thực tế trước khi ghi đóng góp đã hoàn thành.

### Đóng góp cụ thể

Chưa có bằng chứng gắn đóng góp cá nhân với log hoặc commit trong tài liệu hiện có; bổ sung công việc thực tế đã làm.

### Bằng chứng

Chưa xác nhận; bổ sung mã commit, mã lần chạy (`runs/<mã>`) hoặc mục phiếu liên quan.

### Exit ticket

Một điều học được: ... · Một điều còn chưa chắc: ...

## TranThanhTung-2A202603418

### Phần việc phụ trách

Sản phẩm và kinh doanh; phụ trách rà soát phạm vi pilot, ngưỡng kinh doanh và quyết định Gate 1 trong Phiếu B/C. Xác nhận phạm vi thực tế trước khi ghi đóng góp đã hoàn thành.

### Đóng góp cụ thể

Chưa có bằng chứng gắn đóng góp cá nhân với log hoặc commit trong tài liệu hiện có; bổ sung công việc thực tế đã làm.

### Bằng chứng

Chưa xác nhận; bổ sung mã commit, mã lần chạy (`runs/<mã>`) hoặc mục phiếu liên quan.

### Exit ticket

Một điều học được: ... · Một điều còn chưa chắc: ...
