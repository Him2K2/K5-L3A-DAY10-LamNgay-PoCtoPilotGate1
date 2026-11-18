"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    # Ghim phiên bản chính sách đang hiệu lực theo ngày hệ thống
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy:
        return Verdict.allow(policy_id=policy.get("policy_id"))
    return Verdict.escalate("Không tìm thấy chính sách hiệu lực theo ngày vận hành")


def write_gate(ctx, action):
    tool = action.get("tool")

    # CỔNG 1: Bảo vệ ngân sách hoàn tiền - đối soát theo tracking thực tế (chống tin lời khách tự khai khống)
    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            real_delay = H.db_delay_days(parcel, ctx.as_of)
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            entitled = H.entitlement_vnd(policy, order, real_delay, parcel.get("delay_cause"))

            # Chặn hoàn tiền sai khi khách không đủ điều kiện theo tracking DB
            if action.get("amount_vnd", 0) > entitled:
                if entitled == 0:
                    ctx.log("guard_refund_denied_tracking_mismatch", claimed=action.get("amount_vnd"), entitled=0)
                    return Verdict.deny(f"Đơn hàng chỉ trễ {real_delay} ngày theo tracking DB, chưa đủ điều kiện hoàn phí theo chính sách")
                ctx.log("guard_refund_modified_to_entitled", claimed=action.get("amount_vnd"), entitled=entitled)
                return Verdict.modify(f"Điều chỉnh số tiền hoàn về đúng mức quyền lợi theo tracking DB: {entitled}đ", amount_vnd=entitled)

        # Kiểm tra trần hoàn tiền tự động trong ngày từ cổng kinh doanh
        cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
        spent = ctx.tools.auto_refund_today_vnd()
        if cap is not None and spent + action.get("amount_vnd", 0) > cap:
            ctx.log("guard_refund_cap_exceeded", cap=cap, spent=spent, requested=action.get("amount_vnd"))
            return Verdict.escalate("Vượt trần ngân sách hoàn tiền tự động trong ngày, chuyển người duyệt")

    # CỔNG 2: Bảo vệ đối tác hãng vận chuyển - không ghi lỗi oan
    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            real_delay = H.db_delay_days(parcel, ctx.as_of)
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)

            # Chặn ghi lỗi khi tracking không ghi nhận lỗi của hãng hoặc chưa đủ ngày trễ
            if not H.carrier_at_fault(policy, parcel, real_delay):
                ctx.log("guard_carrier_fault_denied", real_delay=real_delay, cause=parcel.get("delay_cause"))
                return Verdict.deny("Tracking không ghi nhận nguyên nhân chậm trễ do lỗi hãng vận chuyển")

            # Cổng pháp lý: Bắt buộc phải có nguyên nhân ghi nhận
            carrier_requires_cause = (ctx.gates or {}).get("legal", {}).get("carrier_fault_requires_recorded_cause", False)
            if carrier_requires_cause and not parcel.get("delay_cause"):
                return Verdict.deny("Cổng pháp lý: thiếu nguyên nhân chậm trễ được ghi nhận")

            carrier_id = parcel["carrier_id"]
            if action.get("parcel_id") != parcel["parcel_id"] or action.get("carrier_id") != carrier_id:
                return Verdict.deny("Kiện hoặc hãng trong yêu cầu ghi lỗi không khớp tracking")
            cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
            if cap is not None and len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= cap:
                ctx.log("carrier_strike_cap_hit", carrier_id=carrier_id, cap=cap)
                return Verdict.deny("Đã đạt trần ghi lỗi tự động của hãng trong ngày; vận hành kiểm tra riêng")
        else:
            return Verdict.deny("Không tìm thấy đơn để xác minh lỗi hãng")

    # CỔNG 3: Bảo vệ dữ liệu cá nhân (PII) khi gửi cho bên thứ ba
    if tool == "notify_carrier":
        blocked_fields = (ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party", [])
        payload = action.get("payload", {})
        if blocked_fields and any(k in payload for k in blocked_fields):
            cleaned = {k: v for k, v in payload.items() if k not in blocked_fields}
            ctx.log("guard_pii_filtered", blocked=blocked_fields)
            return Verdict.modify("Loại bỏ các trường dữ liệu cá nhân theo quy định pháp lý", payload=cleaned)

    return Verdict.allow()
