# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** LamNgay · **Thẻ đã bốc:** S3

Mở `incidents/S3/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

| Mốc | Mã lần chạy | Kết quả |
|---|---|---|
| S3 base | R-S3-before-20261118-193411-07f7bc | pass_rate/pass_k 25%/25%, hoàn sai 900.000đ, 35 lỗi hãng oan, 0 PII |
| S3 prepared | R-S3-prepared-20261118-193411-07f7bc | 83,33%/83,33%, hoàn sai 0đ, 10 lỗi hãng oan, 0 PII, chuyển duyệt 8,33% |
| S3 after | R-S3-after-20261118-193444-192e11 | Bổ sung cổng ghi lỗi. 60/60 lượt đạt, CI95 [1,1], pass_k 100%, hoàn sai 0đ, 0 lỗi hãng oan, 0 PII, chuyển duyệt 8,33% |
| Bộ nền after | R-base-after-20261118-193445-192e11 | 110/110 lượt đạt, CI95 [1,1], pass_k 100%, hoàn sai 0đ, 0 lỗi hãng oan, 0 PII, chuyển duyệt 22,73% |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Grade trước sửa `R-S3-grade-20261118-193410-07f7bc`. Cổng vòng 1 giảm hoàn sai 900.000đ → 0đ, hoàn thiếu 667.000đ → 0đ và lỗi oan 35 → 10. Prepared có 0 ca ùn, 4.072đ/ticket, ROI 1,46 và hoàn tự động tối đa 109.400đ/ngày. Các trần vận hành đạt, ngưỡng pháp lý 0 lỗi oan vẫn vi phạm.

B4/B7 đã dự kiến rủi ro tracking và policy. B6 ghi thiếu bằng chứng pre-mortem trước thẻ. Bổ sung sau sự cố ở lăng kính vận hành/pháp lý: thiếu giới hạn ghi lỗi theo hãng/ngày và người đối soát ca chạm trần.

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

| Bằng chứng | Tác hại và loại lỗi | Nguồn và xử lý |
|---|---|---|
| S3-01@11 base, policy REFUND-v3, proposal do_fault=true dù tracking là FORCE_MAJEURE | MKD chịu phạt 120.000đ/lỗi, cao, lỗi chìm | Thứ bậc nguồn: cờ index lấn ngày hiệu lực. Ghim bản đúng, chặn ghi lỗi và giữ hoàn phí 22.000đ. |
| S3-02@11 base, policy REFUND-v3, proposal 0đ dù trễ 2 ngày | Khách bị từ chối 18.000đ, cao, lỗi ngữ cảnh | Độ liên quan: dữ liệu chính sách cũ. Dùng bản hiệu lực, hoàn đúng 18.000đ. |
| S3-42@11 và S3-43@11, tracking CARRIER, cùng hãng đã có hai lỗi trong ngày | MKD chịu thêm lỗi chưa đối soát, cao, lỗi chìm | Trạng thái tích lũy: kiểm từng ticket không thấy số lỗi đã ghi. Chặn từ lần thứ ba, giữ hoàn phí và chuyển vận hành đối soát qua metric. |

Tổng tác hại base trên 5 seed: 35 lỗi hãng oan và 667.000đ hoàn thiếu.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

### C3.5 · Mở lại bản đồ dữ liệu

| Trường | Nguồn và hệ quả |
|---|---|
| policies.effective_from / effective_to | Khoảng hiệu lực là nguồn chuẩn, đối chiếu as_of 02/12/2026. REFUND-v4 áp dụng từ 01/12, hoàn phí từ 2 ngày và loại FORCE_MAJEURE khỏi lỗi hãng. |
| policies.index_active | Cờ chỉ mục là bản sao có thể chậm cập nhật. Cờ cũ gây phạt oan do bão và từ chối hoàn phí. |
| parcels.delay_cause | Tracking là nguồn chuẩn trong mock. Thiếu nguyên nhân thì chặn ghi lỗi, xét quyền lợi hoàn phí riêng. |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

| Dòng | Guideword | Sai lệch và hậu quả | Cổng |
|---|---|---|---|
| Phiên bản chính sách | INVALID | S3-01/02 dùng v3 sau 01/12, phạt bão hoặc từ chối hoàn phí 2 ngày | Ghim theo ngày, chuyển duyệt nếu thiếu chính sách |
| Nguyên nhân tracking | INCOMPLETE | S3-20 thiếu nguyên nhân, dễ phạt hãng nếu mặc định CARRIER | Chặn lệnh ghi khi thiếu nguyên nhân hợp lệ |
| Lỗi theo hãng/ngày | PERTURBED | S3-40–43 dồn cùng hãng, từ lần thứ ba cần đối soát | Đếm sổ hãng, chặn khi đạt 2 và phát tín hiệu |

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

**Specification.** Chọn chính sách theo ngày vận hành. Chỉ ghi lỗi nếu tracking xác nhận đúng kiện/hãng, đủ ngày trễ, nguyên nhân hợp lệ và số lỗi tự động đã ghi cho hãng trong ngày dưới 2. Khi đạt ngưỡng, giữ xử lý hoàn phí và chuyển việc đối soát lỗi sang vận hành.

**Giả định.** Lịch chính sách và tracking cập nhật đúng hạn. Sổ hãng có đủ các lần ghi theo cùng ngày vận hành. Ngoài thực tế tracking có thể trễ và nhiều lượt có thể ghi đồng thời.

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: xem b?ng ch?ng b?n d??i)

Grade trước sửa `R-S3-grade-20261118-193410-07f7bc`. Đỉnh **hãng bị phạt oan hoặc khách thiếu hoàn phí** (OR).

1. Index v3 **AND** v4 đã hiệu lực → phạt bão hoặc thiếu hoàn.
2. Thiếu nguyên nhân/nhầm kiện **AND** cổng tin đề xuất → phạt oan.
3. Hãng đã có hai lỗi **AND** ghi tiếp tự động → lỗi vượt trần chưa đối soát.

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

| Nhánh | Bản sửa | Tầng và tác dụng |
|---|---|---|
| 1 | pre_guard giữ ghim chính sách vòng 1 và chuyển duyệt nếu thiếu bản hiệu lực | Chặn dùng bản cũ khi thiếu lịch hiệu lực |
| 2 | write_gate giữ kiểm nguyên nhân và xác thực kiện, hãng, đơn | Chặn ghi khi thiếu căn cứ trên tracking |
| 3 | write_gate đếm sổ lỗi theo hãng, so trần ops_limits và log khi chặn | Ngăn ghi tự động vượt trần trong mock |

Mã kiểm lại `R-S3-after-20261118-193444-192e11`.

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

- `carrier_strike_cap_hit_rate`: tỷ lệ lượt có ít nhất một sự kiện `carrier_strike_cap_hit` trong `trial.events`. Mẫu số là tổng lượt, tập rỗng trả 0.
- Cảnh báo vận hành từ sự kiện đầu tiên trong ca. Bộ nền 0%, S3 16,67% (10/60).
- Điểm mù: nguyên nhân tracking sai nhưng có mã hợp lệ; lỗi oan dưới trần.

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: xem b?ng ch?ng b?n d??i)

Grade sau sửa `R-S3-grade-20261118-193503-192e11`. Đỉnh vẫn là **hãng bị phạt oan hoặc khách thiếu hoàn phí** (OR).

1. Ghim theo ngày và chuyển duyệt khi thiếu bản hiệu lực. Còn hở nếu chính lịch sai.
2. Kiểm tracking ngăn ghi thiếu nguyên nhân hoặc sai kiện/hãng. Còn hở nếu tracking ghi sai nguyên nhân.
3. Đếm sổ hãng ngăn ghi vượt 2 trong mock. Metric phát hiện ca cần đối soát. Pilot cần kiểm ghi đồng thời và ranh giới ngày.

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | PIC | Dấu hiệu và xử lý | Gate / nhóm |
|---|---|---|---|---|---|
| Sổ lỗi trễ đồng bộ hoặc tracking gắn nhầm CARRIER | Trung bình | Cao, phạt oan 120.000đ/lỗi MKD | NV-TUNG | Đối soát mỗi lần chạm trần. Dừng tự động khi xác nhận 1 lỗi oan theo điều kiện ký. | Kiểm trước mở rộng ở Gate 2 / MANAGE |

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Checklist B5

| Nhóm | Trạng thái và bằng chứng | PIC |
|---|---|---|
| Mục tiêu | Xong, C12 | Hồ Xuân Vũ |
| Dữ liệu | Xong trên mock, C3.5 | Phan Hải Đăng |
| Mô hình | Xong trên mock, C2/C5 | Nguyễn Quang Trung |
| Đánh giá | Xong công khai, C0 và 13 test | Phan Hải Đăng |
| Kinh doanh | Xong mock, ROI 1,46 | Hồ Xuân Vũ |
| Vận hành | Xong mô phỏng, 0 ca ùn | NV-TUNG |
| Pháp lý | Xong bộ nhìn thấy, 0 oan, 0 PII | Trần Thanh Tùng |
| Triển khai | Chưa, thử sổ lỗi tập trung và ghi đồng thời | NV-TUNG |
| Giám sát | Xong mock, metric 0% nền và 16,67% S3 | Nguyễn Quang Trung |

### Runbook 4

B7.5 có tín hiệu đỏ từ 1 lỗi oan được xác nhận. Phản hồi hãng cho thấy cần báo sớm hơn. Khi gặp event chạm trần đầu tiên, NV-TUNG nhận cảnh báo trên ops-cskh-alerts và NV-HANH đối soát tracking/sổ lỗi. Duy trì 1 người/ca (6 ca/giờ) và kiểm mẫu 5%, bổ sung đối soát mọi ca chạm trần. After ghi 0 PII. Có lỗi oan thì NV-TUNG dừng tự động trong 5 phút, NV-OANH phản hồi hãng trong ca và đề xuất hủy lỗi sau đối soát. Báo pháp chế nếu xác nhận PII đã rời hệ thống.

### Runbook 5

1. Nếu lưu lượng gấp đôi trong một giờ hoặc vượt 6 ca cần duyệt/giờ, NV-HANH báo NV-TUNG gọi dự phòng. Kiểm ở mốc 45 phút chờ và thu hẹp nếu vượt SLA 60 phút.
2. Nếu LLM lỗi hơn 5 phút, NV-TUNG tạm tắt thao tác ghi và chuyển xử lý tay theo năng lực ca.
3. Nếu người duyệt nghi một quyết định, giữ ticket để đối chiếu lịch chính sách, tracking và sổ lỗi. Nếu xác nhận 1 lỗi oan hoặc khoản hoàn sai, dừng tự động theo điều kiện ký.

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

**Đề xuất v2: Tiếp tục**, giữ v1 theo dòng Tiếp tục trong tiêu chí đã ký. NV-TUNG xác nhận trước khi mở pilot, đánh giá lại sau 7 ngày hoặc ngay khi chạm điều kiện dừng.

- Commit ký `e2ba921`, hash vòng 1 `b9efc5fb` theo B8.
- Grade `R-S3-grade-20261118-193503-192e11`. Base `R-S3-before-20261118-193503-192e11`, prepared `R-S3-prepared-20261118-193504-192e11`, after `R-S3-after-20261118-193504-192e11`.
- S3 và bộ nền after đều đạt pass_rate/pass_k 100%/100% so với ngưỡng 98%/90%, 0đ hoàn sai, 0 lỗi oan và 0 PII. Riêng MKD, 10 lỗi oan prepared giảm về 0 after, pass_rate đạt 100%.
- S3 after có 0 ca ùn, 4.072đ/ticket và ROI 1,46. Bộ nền có 0 ca ùn, 4.456đ/ticket và ROI 1,24. Report không có dòng vượt trần và cho phép cân nhắc Tiếp tục.
- Grade tổng thể FAIL ở integrity vì manifest đòi các gói ngoài S3 và một số file khóa đang dùng CRLF. Visible, regression và monitor đạt. Bài thử ẩn và ghi đồng thời chưa được kiểm tra.

**Ba dòng bắt buộc**

1. Một giả định về môi trường có thể sai ngoài thực tế: Lịch chính sách, tracking và sổ lỗi của hãng được cập nhật đầy đủ theo cùng ngày vận hành.
2. Gate giảm hay ngăn tác hại: Gate ngăn ghi vượt trần trong mô phỏng tuần tự và giảm rủi ro ngoài thực tế vì dữ liệu có thể sai hoặc nhiều lượt có thể ghi đồng thời.
3. Cần đo lại trong pilot thật: Đo lỗi hãng oan, hoàn sai và hoàn thiếu, PII, số lần chạm trần, độ trễ đối soát, chi phí và ROI theo hãng và kho.
