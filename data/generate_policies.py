"""
Policy PDF Generator for Daily Banking Assistant Knowledge Base
Generates well-formed, readable PDF files for RAG ingestion.
"""
import os
import pypdf

def create_simple_pdf(filepath, title, sections):
    # Using pypdf or minimal standard PDF stream
    lines = [
        "BT",
        "/F1 18 Tf",
        "50 750 Td",
        f"({title}) Tj",
        "ET",
        "BT",
        "/F1 10 Tf",
        "50 710 Td",
        "15 TL"
    ]
    for section_title, content in sections:
        clean_sec = section_title.replace("(", "\(").replace(")", "\)")
        lines.append(f"() '")
        lines.append(f"({clean_sec.upper()}) '")
        lines.append(f"() '")
        for line in content:
            clean_l = line.replace("\\", "\\\\").replace("(", "\(").replace(")", "\)")
            lines.append(f"({clean_l}) '")
    lines.append("ET")
    
    stream_content = "\n".join(lines).encode("latin-1", errors="replace")
    stream_len = len(stream_content)
    
    # We will build valid PDF objects
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 850] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    obj4 = f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode("latin-1") + stream_content + b"\nendstream\nendobj\n"
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    
    header = b"%PDF-1.4\n"
    offset1 = len(header)
    offset2 = offset1 + len(obj1)
    offset3 = offset2 + len(obj2)
    offset4 = offset3 + len(obj3)
    offset5 = offset4 + len(obj4)
    xref_offset = offset5 + len(obj5)
    
    xref = f"xref\n0 6\n0000000000 65535 f \n{offset1:010d} 00000 n \n{offset2:010d} 00000 n \n{offset3:010d} 00000 n \n{offset4:010d} 00000 n \n{offset5:010d} 00000 n \n".encode("latin-1")
    trailer = f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin-1")
    
    with open(filepath, "wb") as f:
        f.write(header + obj1 + obj2 + obj3 + obj4 + obj5 + xref + trailer)

def generate_all():
    policies_dir = "d:/hcl_tech/data/policies"
    os.makedirs(policies_dir, exist_ok=True)
    
    # 1. Card Policy
    card_sections = [
        ("1. Card Blocking and Replacement", [
            "Customers may block debit or credit cards instantly via conversational assistant or mobile banking.",
            "Once blocked, debit cards are rendered permanently inactive for security.",
            "Card replacement takes 3 to 5 business days, delivered to registered KYC address.",
            "A standard replacement fee of INR 150 + GST applies unless waived for fraud or unauthorized incidents."
        ]),
        ("2. Transaction Limits & Contactless", [
            "Default domestic POS and ATM limit is INR 50,000 per day.",
            "Contactless NFC payments up to INR 5,000 do not require PIN authentication.",
            "International card transactions are disabled by default for fraud prevention.",
            "Customers can request temporary limit increases through the assistant pending risk approval."
        ]),
        ("3. Credit Card Payment & Billing Cycle", [
            "Credit card billing cycle generates on the 15th of each month.",
            "Due date is always 20 days after the statement date (typically the 5th of the following month).",
            "Minimum Amount Due (MAD) is 5 percent of the total outstanding statement balance.",
            "Late payment fee of INR 750 applies if MAD is not paid by the due date."
        ])
    ]
    create_simple_pdf(f"{policies_dir}/card_policy.pdf", "Apex Bank - Debit & Credit Card Policy", card_sections)
    
    # 2. Loan Policy
    loan_sections = [
        ("1. Loan Products & Eligibility Criteria", [
            "Apex Bank offers Home Loans, Personal Loans, Auto Loans, and Education Loans.",
            "Pre-approved loan eligibility requires: Minimum credit score of 720, monthly income >= INR 25,000.",
            "Fixed Obligation to Income Ratio (FOIR) must not exceed 50 percent of net monthly income.",
            "Existing account holders with 6+ months active salary credit receive preferential interest rates."
        ]),
        ("2. Interest Rates and Prepayment Terms", [
            "Home Loans: Floating interest rates starting from 8.40 percent p.a. Zero prepayment penalty.",
            "Personal Loans: Fixed interest rates starting from 10.75 percent p.a. Prepayment penalty 2 percent.",
            "Auto Loans: Fixed rates starting at 8.90 percent p.a. Tenures available from 12 to 84 months."
        ]),
        ("3. EMI Payments & Grace Period", [
            "EMIs are debited automatically on designated date (1st to 10th of every month).",
            "A bounce charge of INR 500 applies for failed auto-debit due to insufficient funds.",
            "Customers can view upcoming EMIs, amortization schedules, and principal balances anytime."
        ])
    ]
    create_simple_pdf(f"{policies_dir}/loan_policy.pdf", "Apex Bank - Lending & EMI Policy", loan_sections)
    
    # 3. Payment Policy
    payment_sections = [
        ("1. UPI & Digital Fund Transfers", [
            "Apex Bank UPI limit is INR 1,00,000 per 24-hour cycle across up to 20 transactions.",
            "IMPS transactions are instant and available 24x7 with max per-transaction limit of INR 5,00,000.",
            "NEFT runs in hourly batches 24x7 with no maximum limit.",
            "RTGS is available for high-value transfers exceeding INR 2,00,000."
        ]),
        ("2. Pending & Failed Transactions", [
            "If an account is debited but the merchant does not receive credit, auto-reversal occurs within T+1 days.",
            "For UPI failures where money is debited, RBI guidelines mandate refund within T+3 business days.",
            "Compensation of INR 100 per day is credited to customer if reversal exceeds turnaround time.",
            "Customers can check reference status using UPI UTR or Payment Reference ID."
        ]),
        ("3. Bill Payments and Auto-Pay Reminders", [
            "Smart bill reminders notify customers 5 days before scheduled utility and card due dates.",
            "Auto-pay instructions can be cancelled or paused 24 hours prior to scheduled debit."
        ])
    ]
    create_simple_pdf(f"{policies_dir}/payment_policy.pdf", "Apex Bank - Payment & Settlement Policy", payment_sections)
    
    # 4. Banking FAQ
    faq_sections = [
        ("1. How do I dispute a fraudulent transaction?", [
            "If you see an unfamiliar charge, report it immediately to lock card controls.",
            "The assistant automatically triggers fraud verification and opens a formal dispute ticket.",
            "Disputes filed within 72 hours carry zero customer liability under bank safety rules.",
            "Investigation turnaround time is 7 to 10 working days, with provisional credit granted."
        ]),
        ("2. How does the AI Assistant calculate remaining funds?", [
            "The assistant checks your real-time available balance across active savings accounts.",
            "It computes all obligations due within the upcoming 15 days (EMIs, card dues, utility bills).",
            "Remaining funds = Available Balance minus Total Upcoming Obligations.",
            "This deterministic calculation ensures zero hallucination and complete accuracy."
        ]),
        ("3. Human-in-the-Loop Approval Workflow", [
            "High-risk actions including card blocking, dispute filings, and limit changes require authorization.",
            "Sensitive requests are routed to the Bank Operations Admin Queue for employee review."
        ])
    ]
    create_simple_pdf(f"{policies_dir}/banking_faq.pdf", "Apex Bank - Daily Banking FAQs", faq_sections)
    print("All 4 policy PDFs generated successfully!")

if __name__ == "__main__":
    generate_all()
