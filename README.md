# AI-Powered Daily Banking Assistant

> **HCLTech | Future Ready AI Engineer Hackathon**  
> A secure, personalized, explainable, and auditable conversational AI assistant for everyday account servicing, payments, cards, loans, expense insights, reminders, and fraud support.

---

## 🏛️ System Architecture & Workflow

The architecture follows a strict **Deterministic Tool-First** design principle:  
*Use deterministic banking tools for balances, calculations, eligibility, and actions. Use language models for natural conversation, explanation, and orchestration, backed by policy controls and human-in-the-loop (HITL) approvals for high-risk decisions.*

```
[ User (Web / Mobile) ]
           │
           ▼
[ API Gateway & Security ] ──(JWT, Auth, Rate Limit, Audit Trace)
           │
           ▼
[ AI Orchestrator (LangGraph) ]
  ├── 1. Intent Understanding (Classify 10 use cases)
  ├── 2. Query Planning (Select deterministic tools / RAG)
  ├── 3. Tool Execution & Deterministic Math
  ├── 4. Human-in-the-Loop Approval (High-risk card/dispute actions)
  └── 5. Explainable Response Generation (with Trace ID & structured widgets)
           │
   ┌───────┴─────────────────────────────┬──────────────────────────┐
   ▼                                     ▼                          ▼
[ Knowledge / RAG Layer ]       [ Banking Tool Layer ]      [ Human-in-the-Loop ]
- card_policy.pdf               - get_balance()             - Bank Officer Queue
- loan_policy.pdf               - analyze_expenses()        - Dispute Authorization
- payment_policy.pdf            - calculate_remaining_funds - Card Lock Review
- banking_faq.pdf               - get_payment_status()
- Vector Index & Retriever      - block_card() / fraud_check()
                                         │
                                         ▼
                             [ Core Banking Systems ]
                             - Accounts & Ledger
                             - UPI / Payment Switch
                             - Credit Card CMS
                             - Loan Management (LMS)
                             - Fraud Monitoring Engine
```

---

## 🎯 10 Daily Banking Use Cases Supported

| # | Use Case | Example Customer Query | Deterministic Action & Behavior |
|---|---|---|---|
| **1** | **Account & Balance Inquiry** | *"What is my current account balance?"* | Retrieves live available & ledger balance and recent credit/debit summary. |
| **2** | **Daily Expense Tracking** | *"How much have I spent this month?"* | Aggregates debit transactions, calculates category breakdowns (Food ₹8,500, Transport ₹3,200, Shopping ₹12,000, Bills ₹4,500) and trends. |
| **3** | **Credit Card Assistance** | *"When is my credit card payment due?"* | Retrieves statement details, payment due date (2026-11-05), minimum due (₹1,000) and total due (₹10,000). |
| **4** | **UPI & Payment Assistance** | *"Did my UPI payment to Amazon go through?"* | Verifies transaction status (`COMPLETED`), bank reference number (`UPI993821034`), and failure explanations when applicable. |
| **5** | **EMI & Loan Tracking** | *"What is my next EMI amount?"* | Retrieves loan details, amortization schedule, next EMI due date, and outstanding balance. |
| **6** | **Personal Finance Guidance** | *"Can I save more this month?"* | Analyzes income against discretionary spending and provides non-binding savings observations and auto-sweep suggestions. |
| **7** | **Smart Bill Reminder** | *"What payments are due this week?"* | Identifies upcoming credit card dues, EMIs, utility bills (BESCOM, Airtel), and subscription renewals. |
| **8** | **Card Services** | *"I lost my debit card."* | Authenticates customer, locks card controls immediately, and initiates replacement dispatch under bank controls. |
| **9** | **Fraud Support** | *"I do not recognize this transaction."* | Evaluates transaction risk score (`TXN123456`), locks international channel, and opens an auditable dispute workflow routed to Bank Officer review. |
| **10** | **Personalized Offers** | *"Am I eligible for a pre-approved loan?"* | Evaluates customer credit score (780) and income against bank lending rules; presents pre-approved loan offers up to ₹5,00,000 @ 9.99%. |
| **—** | **Deterministic Remaining Funds** | *"How much money do I have available after paying all upcoming bills?"* | Computes `Available Balance (₹1,70,000) - Total Obligations (₹34,648) = ₹135,352` with full explainability. |

---

## 💻 Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.13+, FastAPI, Pydantic, HTTPX, PyJWT
- **AI Orchestration**: LangGraph StateGraph pipeline, deterministic tool binding, RAG policy groundings
- **RAG & Vector Store**: PyPDF, dense vector indexing, cosine similarity, banking policy PDFs
- **Data & Storage**: Unified Data Layer supporting MongoDB with transparent high-performance JSON & SQLite persistence fallback
- **Observability**: MongoDB Audit Logs, Python Structured Logger, Trace IDs (`BANK-XXXXX`), p50/p95 response metrics
- **Infrastructure**: Nginx reverse proxy configuration

---

## 📂 Repository Structure

```
daily-banking-assistant/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/         (Navbar, Sidebar, Loader, ErrorMessage)
│   │   │   ├── chat/           (ChatWindow, ChatMessage, ChatInput, ToolExecution)
│   │   │   ├── dashboard/      (BalanceCard, ExpenseChart, UpcomingPayments, RecentTransactions)
│   │   │   └── admin/          (ApprovalQueue, ApprovalCard, AuditLogs)
│   │   ├── pages/              (Login, Dashboard, Chat, Transactions, Admin)
│   │   ├── services/           (api.js, authApi.js, chatApi.js, bankingApi.js)
│   │   ├── store/              (authStore.js, chatStore.js)
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/             (settings.py, database.py)
│   │   ├── api/                (router.py, routes: auth, chat, banking, transactions, cards, loans, payments, fraud, admin)
│   │   ├── middleware/         (auth.py, rate_limit.py, request_id.py)
│   │   ├── models/             (user, account, transaction, card, loan, payment, bill, dispute, offer, audit_log)
│   │   ├── schemas/            (auth, chat, banking, transaction, response)
│   │   ├── services/           (auth, banking, transaction, payment, card, loan, fraud, audit services)
│   │   ├── agents/             (graph.py, state.py, nodes: intent, planner, tool_executor, approval, response)
│   │   ├── tools/              (account, transaction, expense, payment, card, loan, fraud, offer tools)
│   │   ├── rag/                (loader, splitter, embeddings, vector_store, retriever)
│   │   ├── banking_systems/    (core_banking, payment_system, card_system, loan_system, fraud_system)
│   │   ├── calculations/       (balance, expenses, emi, obligations)
│   │   └── utils/              (logger, security, trace)
│   ├── tests/                  (test_auth, test_tools, test_calculations, test_banking, test_agent)
│   ├── requirements.txt
│   └── .env
│
├── data/
│   ├── policies/               (card_policy.pdf, loan_policy.pdf, payment_policy.pdf, banking_faq.pdf)
│   └── seed/                   (users.json, accounts.json, transactions.json, loans.json)
│
├── infrastructure/
│   └── nginx/                  (nginx.conf)
│
├── .gitignore
├── README.md
└── .env.example
```

---

## 🚀 Quick Start Guide

### 1. Run Backend Server
```bash
cd backend
python app/main.py
```
*Backend API starts at: `http://127.0.0.1:8000`*  
*Health Check: `http://127.0.0.1:8000/health`*

### 2. Run Frontend Web App
```bash
cd frontend
npm run dev
```
*Frontend opens at: `http://localhost:3000`*

### 3. Run Automated Tests
```bash
cd backend
python tests/test_agent.py
python tests/test_tools.py
python tests/test_calculations.py
python tests/test_banking.py
python tests/test_auth.py
```

---

## 🔐 Demo Credentials

| Role | Username / ID | Password | Access |
|---|---|---|---|
| **Customer** | `C1001` (Aarav Sharma) | `password123` | Dashboard, AI Assistant, Transactions & Dues |
| **Customer** | `C1002` (Priya Patel) | `password123` | Dashboard, AI Assistant, Personal Loans |
| **Bank Officer** | `A9001` (Vikram Malhotra) | `admin123` | Human-in-the-Loop Approval Queue, Audit Observability Logs |
