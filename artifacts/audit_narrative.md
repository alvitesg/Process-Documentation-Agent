# Audit Narrative: Procure-to-Pay

## Scope Summary
Assessment of requisition, approval, purchase order, receipt, and invoice payment.

## Process Walkthrough
- **S1** (Requester) Creates requisition [System: ERP]
- **S2** (Manager) Approves requisition [System: ERP]
- **S3** (Procurement) Issues purchase order [System: ERP]
- **S4** (AP) Performs three-way match and posts invoice [System: ERP]
- **S5** (Treasury) Executes payment run [System: Bank Portal]

## Control Points
- **C1**: Manager approval required before PO creation (Owner: Department Manager, Frequency: Per transaction)
- **C3**: Three-way match between PO, receipt, and invoice (Owner: Accounts Payable, Frequency: Per transaction)

## Noted Gaps / Follow-ups
- Validate whether all critical approvals are evidenced and retained.
- Confirm segregation of duties across initiation, approval, and posting.
- Obtain samples for control operating effectiveness testing.
