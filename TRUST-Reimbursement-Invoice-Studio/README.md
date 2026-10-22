# Reimbursement Invoice Studio | SharePoint Finance Workflow

**Organization:** T.R.U.S.T. South LA  
**Role:** Solution architect, developer, finance workflow designer  
**Year:** 2026  
**Project status:** Completed and closed at the selected v1.2 download-first scope. A prior pilot ran in SharePoint; final v1.2 rollout remains a separate verification step.

## Business problem

Finance needed to prepare reimbursement documentation from an existing credit-card tracker without manually transcribing transaction details, re-uploading supporting documents, or replacing the Microsoft 365 intake workflow.

## Solution

Built a branded SharePoint Framework (SPFx) web part that reads the existing Excel table in **read-only** mode, normalizes source transactions, and lets staff search and select expense lines. Users can edit invoice information, preview an invoice, verify original linked receipts, and download a combined PDF with the invoice first and receipt appendix afterward.

An integrated financial dashboard summarizes net monthly card activity and gross purchases by vendor, grant category, department, employee, and approver, while surfacing source-data quality issues. Version 1.2 refines chart axes and titles and makes verified PDF download the final product workflow.

## Engineering contributions

- **Microsoft 365 integration:** Authenticated SharePoint REST workbook access; robust named-table parsing and transaction normalization.
- **Document automation:** Invoice editing and rendering, original receipt resolution, missing-file checks, receipt index and PDF merging with pdf-lib.
- **Finance analytics:** Source-based KPI calculations, credits/refunds, grouped spending charts, and exception diagnostics.
- **Reliability and release engineering:** Integer-cent calculations, validated positive claim adjustments, source-to-receipt mapping, automated contract tests, TypeScript compilation and PowerShell/Heft standalone project packaging.
- **Scope design:** Retained the established source workbook and minimized extra infrastructure by omitting a redundant invoice register/approval backend.

## Validation and outcome

In an authorized SharePoint pilot, the application loaded **440 live transaction records**, reported source classification notices, resolved supporting files and produced a **four-page invoice-plus-receipts example** (one invoice, three original documents). The financial dashboard also ran with live workbook data.

The adopted v1.2 source introduces a clean, non-watermarked download and labeled spending charts. The exact v1.2 full Windows/tenant deployment is **not** independently confirmed by the supplied logs. No hours-saved, cost-savings, reimbursement approval or other financial-impact metric is claimed.

## Technology

SPFx, TypeScript, JavaScript, HTML/CSS, SharePoint REST, Microsoft 365 Excel, delegated Graph only where authorized, pdf-lib, fflate, Node.js, Yeoman, Heft, Windows PowerShell, automated contract checks.

## Operational and privacy boundaries

The export does **not** submit, approve, archive, lock, pay or deduplicate reimbursement claims. Finance continues its standard ledger, retention, security and approval procedures. This is a **portfolio case study only**: internal SharePoint links, workbook identifiers, proprietary application source, actual transactions, receipts and employee information are intentionally withheld.
