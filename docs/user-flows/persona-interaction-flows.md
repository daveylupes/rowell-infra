# Persona Interaction Flows

> **Detailed User Flows for All Rowell Infrastructure Personas**

## 📋 Overview

This document provides comprehensive interaction flows for all four user personas on the Rowell Infrastructure platform. Each persona has unique needs, goals, and workflows optimized for their specific use cases.

### The Four Personas

| Persona | Primary Use Case | Key Features | Complexity |
|---------|------------------|--------------|------------|
| 👤 **Individual User** | Personal remittances & payments | Send/receive money, manage wallet | Low |
| 🏪 **Merchant** | Accept business payments | Payment processing, POS integration | Medium |
| 🏦 **Anchor** | Fiat on/off ramps | Liquidity provision, compliance | High |
| 🎗️ **NGO** | Aid distribution & fundraising | Transparent tracking, donor reports | Medium-High |

---

## 👤 PERSONA 1: Individual User

### Profile

**Name:** Sarah, 28  
**Location:** Lagos, Nigeria  
**Occupation:** Software Developer  
**Use Case:** Sends money to family in Kenya monthly  
**Tech Savvy:** High  
**Income:** Mid-range  
**Transaction Frequency:** Weekly

### User Goals

✅ Send money to family quickly and cheaply  
✅ Receive payments from international clients  
✅ Track spending and savings  
✅ Secure storage of digital assets  
✅ Easy-to-use interface

---

### Individual User Flow: Complete Journey

```
┌─────────────────────────────────────────────────────────────────┐
│              INDIVIDUAL USER: COMPLETE JOURNEY                   │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: DISCOVERY & SIGN UP
───────────────────────────────
Friend Recommends Rowell
  │
  ├─> Visit Website/App
  │    ├─ View landing page
  │    ├─ Compare fees with traditional services
  │    └─ See: Save 90% on fees!
  │
  ├─> Sign Up
  │    ├─ Email + Password
  │    ├─ Phone verification
  │    └─ Select: "Individual User"
  │
  └─> Email Verification
       └─> Account created! ✅

PHASE 2: ONBOARDING
───────────────────
Dashboard Welcome Screen
  │
  ├─> Create Wallet
  │    ├─ Select network: Stellar
  │    ├─ Environment: Testnet (for practice)
  │    ├─ Wallet created in 10 seconds
  │    └─> Backup secret key
  │         └─> Download key file ✅
  │
  ├─> [Optional] Quick Tutorial
  │    ├─ "Send your first test transaction"
  │    ├─ Practice with test USDC
  │    └─ Learn interface
  │
  └─> Switch to Mainnet
       ├─> "Ready for real transactions?"
       ├─> KYC Verification required
       └─> Upload ID and verify

PHASE 3: KYC VERIFICATION
─────────────────────────
Prompted for Identity Verification
  │
  ├─> Personal Information
  │    ├─ Full name
  │    ├─ Date of birth
  │    ├─ Address
  │    └─ Phone (already verified)
  │
  ├─> ID Document Upload
  │    ├─ Select: Nigerian National ID
  │    ├─ Enter BVN (Bank Verification Number)
  │    ├─ Upload front photo
  │    └─ Upload back photo
  │
  ├─> Selfie Verification
  │    ├─ Take live selfie
  │    └─> Face match with ID photo
  │
  └─> Submit for Review
       ├─> "Verification usually takes < 2 hours"
       ├─> Email notification when complete
       └─> ✅ VERIFIED! (Daily limit: $10,000)

PHASE 4: FUNDING WALLET
───────────────────────
Dashboard → Add Funds
  │
  ├─> Select Amount: 50,000 NGN (≈$65 USDC)
  │
  ├─> Select Funding Method
  │    └─> Choose: Mobile Money (M-Pesa)
  │         ├─ Instant deposit
  │         ├─ Fee: 0.5%
  │         └─ Total: 50,250 NGN
  │
  ├─> Confirm Mobile Money Payment
  │    ├─> Receive payment prompt on phone
  │    ├─> Enter M-Pesa PIN
  │    └─> ✅ Payment confirmed
  │
  └─> Funds Added
       ├─> Wallet balance: 65.00 USDC
       └─> Ready to send money!

PHASE 5: FIRST REMITTANCE
──────────────────────────
Dashboard → Send Money
  │
  ├─> Enter Recipient
  │    ├─ Name: "Mom"
  │    ├─ Phone: +254 712 345 678 (Kenya)
  │    └─> Check: Recipient has Rowell wallet ✅
  │
  ├─> Enter Amount
  │    ├─ Amount: 25.00 USDC
  │    ├─> Convert: ≈ 3,375 KES
  │    └─ Fee: 0.025 USDC (0.1%)
  │
  ├─> Review Details
  │    ├─ To: Mom (Kenya)
  │    ├─ Amount: 25.00 USDC → 3,375 KES
  │    ├─ Fee: 0.025 USDC
  │    ├─ Total: 25.025 USDC
  │    └─ Memo: "For house expenses"
  │
  ├─> Confirm with PIN
  │    └─> Enter 4-digit PIN
  │
  ├─> Processing (3 seconds)
  │    └─> Blockchain confirmation...
  │
  └─> ✅ SUCCESS!
       ├─> Receipt available
       ├─> Mom notified via SMS
       └─> Balance: 39.975 USDC remaining

PHASE 6: REPEAT TRANSACTIONS
─────────────────────────────
Subsequent Transactions (Much Faster!)

Dashboard → Quick Send Widget
  │
  ├─> Tap "Mom" recipient card
  │    └─> Pre-filled with last amount
  │
  ├─> Confirm amount: 25.00 USDC
  │
  ├─> Biometric auth (Face ID)
  │
  └─> ✅ DONE! (< 30 seconds total)

OR

Set Up Recurring Payment
  │
  ├─> Wallet → Recurring Payments
  ├─> Create new: "Monthly to Mom"
  ├─> Amount: 25.00 USDC
  ├─> Schedule: 1st of every month
  └─> ✅ Automatic sending!

PHASE 7: RECEIVING MONEY
─────────────────────────
International Client Pays for Freelance Work

Email from Client: "I've sent payment to your Rowell wallet"
  │
  ├─> Push Notification
  │    └─> "💰 You received 500.00 USDC!"
  │
  ├─> Open App
  │    ├─> New balance: 539.975 USDC
  │    └─> Transaction details shown
  │
  ├─> View Receipt
  │    ├─ From: Client Inc.
  │    ├─ Amount: 500.00 USDC
  │    ├─ Date: Oct 6, 2025
  │    └─ Memo: "Invoice #1234 payment"
  │
  └─> [Optional] Send Thank You
       └─> Quick message feature

PHASE 8: WITHDRAWING FUNDS
───────────────────────────
Convert Some USDC to Local Bank Account

Wallet → Withdraw
  │
  ├─> Amount: 200.00 USDC
  │
  ├─> Withdraw to: Nigerian Bank Account
  │    ├─ Bank: GTBank
  │    ├─ Account: 0123456789
  │    └─ Account Name: Sarah Adebayo
  │
  ├─> Fee: 2.00 USDC (1%)
  │
  ├─> Convert: 200 USDC → 310,000 NGN
  │
  ├─> Review
  │    ├─ Amount: 200.00 USDC
  │    ├─ Fee: 2.00 USDC
  │    ├─ You'll receive: 306,900 NGN
  │    └─ Arrival: 1-2 business days
  │
  └─> Confirm
       ├─> Processing...
       └─> ✅ Withdrawal initiated
            └─> Email confirmation sent

PHASE 9: ONGOING USAGE
──────────────────────
Daily/Weekly Activities

Monday Morning:
  └─> Check balance (widget on phone home screen)
       └─> Balance: 339.975 USDC

Wednesday:
  └─> Pay for coffee at local shop
       ├─> Merchant has Rowell QR code
       ├─> Scan QR → Auto-fills amount
       ├─> Confirm with Face ID
       └─> ✅ Paid 5.00 USDC

Friday:
  └─> Send money to brother
       ├─> Quick send from dashboard
       └─> 15.00 USDC sent in 20 seconds

End of Month:
  └─> View spending analytics
       ├─> Total sent: 125.00 USDC
       ├─> Total received: 500.00 USDC
       ├─> Net change: +375.00 USDC
       └─> Export CSV for personal records
```

---

## 🏪 PERSONA 2: Merchant

### Profile

**Business:** Bob's Coffee Shop  
**Location:** Nairobi, Kenya  
**Business Type:** Small retail café  
**Use Case:** Accept customer payments, pay suppliers  
**Tech Savvy:** Medium  
**Transaction Volume:** 50-100 daily  
**Average Ticket:** $3-$10

### Merchant Goals

✅ Accept payments with low fees  
✅ Quick checkout process  
✅ Track sales and revenue  
✅ Pay suppliers easily  
✅ Generate financial reports

---

### Merchant Flow: Complete Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                 MERCHANT: COMPLETE JOURNEY                       │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: MERCHANT ONBOARDING
─────────────────────────────
Discover Rowell for Business
  │
  ├─> Visit Rowell for Business page
  │    ├─ See benefits: 0.1% fees vs 2.5% card fees
  │    ├─ Calculate savings
  │    └─> "Save $900/month on fees!"
  │
  ├─> Sign Up as Merchant
  │    ├─ Business email
  │    ├─ Business phone
  │    └─ Select: "Merchant" account type
  │
  └─> Business Profile Setup
       ├─ Business name: "Bob's Coffee Shop"
       ├─ Business type: "Café/Restaurant"
       ├─ Location: Nairobi, Kenya
       ├─ Website/Social media links
       └─ Tax ID/Business registration number

PHASE 2: BUSINESS VERIFICATION (KYC-B)
───────────────────────────────────────
Enhanced Verification for Merchants
  │
  ├─> Business Documents
  │    ├─ Business registration certificate
  │    ├─ Tax clearance certificate
  │    ├─ Proof of business address
  │    └─ Bank statement
  │
  ├─> Owner/Director Verification
  │    ├─ Owner ID document
  │    ├─ Proof of address
  │    └─> Selfie verification
  │
  ├─> Business Details
  │    ├─ Expected monthly volume
  │    ├─ Average transaction size
  │    ├─ Business category
  │    └─ Number of locations
  │
  └─> Submit for Review
       ├─> Review time: 1-2 business days
       └─> ✅ VERIFIED!
            ├─ Daily limit: $50,000
            └─ Monthly limit: $1,000,000

PHASE 3: MERCHANT WALLET SETUP
───────────────────────────────
Create Business Wallet
  │
  ├─> Primary Business Wallet
  │    ├─ Network: Stellar (recommended)
  │    ├─ Environment: Mainnet
  │    ├─> Wallet created
  │    └─> Backup keys securely
  │
  ├─> [Optional] Multiple Wallets
  │    ├─ Sales Wallet (customer payments)
  │    ├─ Operating Wallet (supplier payments)
  │    └─ Payroll Wallet (staff payments)
  │
  └─> Configure Settings
       ├─ Default currency: KES
       ├─ Auto-convert to fiat: Yes
       └─ Notification preferences

PHASE 4: PAYMENT ACCEPTANCE SETUP
──────────────────────────────────
Set Up Payment Methods

Option 1: QR CODE (Most Common)
┌──────────────────────────────────────┐
│ 🏪 Merchant Dashboard                 │
│ → Accept Payments → QR Code          │
├──────────────────────────────────────┤
│                                       │
│ STATIC QR CODE                       │
│ ┌──────────────────────────────┐    │
│ │                               │    │
│ │     [Large QR Code]           │    │
│ │                               │    │
│ │  Bob's Coffee Shop            │    │
│ │  Scan to pay                  │    │
│ └──────────────────────────────┘    │
│                                       │
│ [📥 Download] [🖨️ Print] [📧 Email] │
│                                       │
│ DYNAMIC QR (with amount)             │
│ Amount: [____] KES                   │
│ [Generate QR Code]                   │
└──────────────────────────────────────┘

Option 2: POS INTEGRATION
┌──────────────────────────────────────┐
│ 📱 Point of Sale Integration          │
├──────────────────────────────────────┤
│                                       │
│ Connect your POS system:             │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🔌 API Integration             │  │
│ │ For custom POS systems         │  │
│ │ [View API Docs] [Get API Key]  │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 📱 Rowell POS App              │  │
│ │ Turn tablet/phone into POS     │  │
│ │ [Download App]                 │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🔗 E-commerce Plugin           │  │
│ │ WooCommerce, Shopify, etc.     │  │
│ │ [Browse Plugins]               │  │
│ └────────────────────────────────┘  │
└──────────────────────────────────────┘

Option 3: PAYMENT LINKS
┌──────────────────────────────────────┐
│ 🔗 Payment Links                      │
├──────────────────────────────────────┤
│                                       │
│ Create payment link:                 │
│                                       │
│ Amount: [300] KES                    │
│ Description: [Coffee and pastry]     │
│                                       │
│ [Generate Link]                      │
│                                       │
│ Generated Link:                      │
│ rowel.li/pay/coffee-shop-ABC123      │
│                                       │
│ [Copy] [Share via WhatsApp]          │
└──────────────────────────────────────┘

PHASE 5: FIRST CUSTOMER PAYMENT
────────────────────────────────
Customer Orders Coffee (350 KES)

AT THE COUNTER:
  │
  ├─> Cashier: "That'll be 350 KES"
  │
  ├─> Customer: "Can I pay with Rowell?"
  │
  ├─> Cashier shows QR code
  │    └─> Static QR displayed at counter
  │
  ├─> Customer scans QR
  │    ├─ Rowell app opens
  │    ├─ Merchant details shown
  │    ├─ Enter amount: 350 KES
  │    ├─> Customer confirms
  │    └─> Processes in 3 seconds
  │
  ├─> INSTANT NOTIFICATION
  │    ┌────────────────────────────────────┐
  │    │ 💰 Payment Received                 │
  │    │ +350 KES from John Doe             │
  │    │ [Tablet/Phone beeps and shows]     │
  │    └────────────────────────────────────┘
  │
  └─> ✅ CONFIRMED!
       ├─> Cashier sees confirmation
       ├─> Receipt printed (optional)
       └─> Customer served

MERCHANT TABLET VIEW:
┌──────────────────────────────────────┐
│ 📱 Rowell Merchant POS                │
├──────────────────────────────────────┤
│                                       │
│ TODAY'S SALES: 45,280 KES            │
│ Transactions: 127                    │
│                                       │
│ ✅ PAYMENT RECEIVED                  │
│                                       │
│ Amount: 350 KES                      │
│ From: John Doe                       │
│ Time: 10:32 AM                       │
│                                       │
│ [Print Receipt] [Send Email Receipt] │
│                                       │
│ ─────────────────────────────────────│
│                                       │
│ RECENT TRANSACTIONS                  │
│ 10:32 AM  350 KES  ✅                │
│ 10:28 AM  420 KES  ✅                │
│ 10:15 AM  280 KES  ✅                │
│                                       │
└──────────────────────────────────────┘

PHASE 6: DAILY OPERATIONS
──────────────────────────
Typical Business Day

MORNING (8:00 AM):
  ├─> Check previous day's sales
  │    └─> Dashboard shows: 48,000 KES yesterday
  │
  └─> Review pending transactions (none)

THROUGHOUT DAY:
  ├─> Accept customer payments
  │    ├─ Average: 1-2 transactions per 10 min
  │    └─> Real-time balance updates
  │
  ├─> Monitor sales on tablet
  │    └─> Live dashboard showing:
  │         ├─ Total sales today
  │         ├─ Number of transactions
  │         └─ Average transaction value
  │
  └─> [Optional] Quick withdrawal
       ├─> Need cash for change
       ├─> Withdraw 10,000 KES to M-Pesa
       └─> Available in 30 seconds

AFTERNOON (2:00 PM):
  ├─> Supplier calls: "Can you pay for beans?"
  │    └─> Dashboard → Send Money
  │         ├─ To: Coffee Supplier
  │         ├─ Amount: 25,000 KES
  │         ├─ Memo: "Bean order #1234"
  │         └─> ✅ Paid instantly
  │
  └─> Continue accepting customer payments

END OF DAY (6:00 PM):
  └─> Close till and reconcile
       ├─> Dashboard → Today's Report
       │    ├─ Total sales: 52,340 KES
       │    ├─ Transactions: 143
       │    ├─ Average: 366 KES
       │    ├─ Fees paid: 52.34 KES (0.1%)
       │    └─ Net: 52,287.66 KES
       │
       └─> Export report
            ├─> Download CSV
            └─> Email to accountant

PHASE 7: END OF MONTH
──────────────────────
Financial Reporting & Analysis

Dashboard → Reports → Monthly
┌──────────────────────────────────────┐
│ 📊 October 2025 Report                │
├──────────────────────────────────────┤
│                                       │
│ REVENUE                              │
│ Total Sales:     1,568,200 KES       │
│ Transactions:    4,287               │
│ Average:         366 KES             │
│ Growth:          +15% vs Sep         │
│                                       │
│ FEES                                 │
│ Total Fees:      1,568 KES (0.1%)    │
│ Savings vs Cards: 37,637 KES         │
│                                       │
│ TOP SELLING TIMES                    │
│ Peak hours: 8-9 AM, 12-1 PM          │
│ Slowest: 3-4 PM                      │
│                                       │
│ PAYMENT BREAKDOWN                    │
│ Rowell: 85% (3,644 transactions)     │
│ Cash: 15% (643 transactions)         │
│                                       │
│ [Export PDF] [Export CSV]            │
│ [Share with Accountant]              │
└──────────────────────────────────────┘

TAX REPORTING:
  └─> Generate tax report
       ├─> All transactions documented
       ├─> KRA-compliant format
       └─> Submit directly to accountant

PHASE 8: BUSINESS GROWTH
─────────────────────────
Expanding Operations

ADD NEW LOCATION:
  ├─> Dashboard → Settings → Locations
  ├─> Add location: "Bob's Coffee - Westlands"
  ├─> Create separate wallet (optional)
  ├─> Generate new QR code
  └─> Train staff on system

HIRE STAFF:
  ├─> Dashboard → Team Management
  ├─> Add staff member
  │    ├─ Name, email, phone
  │    ├─ Role: Cashier
  │    └─ Permissions: Accept payments only
  │
  ├─> Staff downloads Rowell Merchant app
  ├─> Login with credentials
  └─> Start accepting payments

INTEGRATE E-COMMERCE:
  ├─> Launch online ordering
  ├─> Install Rowell plugin on website
  ├─> Customers pay online
  └─> Automatic order notification

LOYALTY PROGRAM:
  ├─> Dashboard → Loyalty
  ├─> Create program: "Buy 10, get 1 free"
  ├─> Customer IDs tracked automatically
  └─> Notifications when reward earned
```

---

## 🏦 PERSONA 3: Anchor

### Profile

**Organization:** Kenya Financial Services  
**Type:** Licensed financial institution  
**Use Case:** Provide fiat on/off ramps for stablecoins  
**Tech Savvy:** High  
**Transaction Volume:** High ($1M+ daily)  
**Compliance:** Strict regulatory requirements

### Anchor Goals

✅ Provide liquidity for USDC/local currency pairs  
✅ Maintain compliance with financial regulations  
✅ Profitable operations with competitive rates  
✅ Secure custody of assets  
✅ Integrate with banking infrastructure

---

### Anchor Flow: Complete Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                   ANCHOR: COMPLETE JOURNEY                       │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: ANCHOR APPLICATION
────────────────────────────
Institution Applies to Become Anchor

Contact Rowell Enterprise Team
  │
  ├─> Initial Assessment
  │    ├─ Organization type
  │    ├─ Licensing status
  │    ├─ Expected volume
  │    └─ Geographic coverage
  │
  ├─> Due Diligence Package
  │    ├─ Banking license
  │    ├─ Financial statements (3 years)
  │    ├─ Compliance certifications
  │    ├─ AML/KYC policies
  │    ├─ Technical capabilities
  │    └─ Insurance coverage
  │
  ├─> Compliance Review (2-4 weeks)
  │    ├─ Legal team review
  │    ├─ Compliance verification
  │    ├─ Technical assessment
  │    └─> Background checks
  │
  └─> ✅ APPROVED
       ├─> Anchor Agreement signed
       ├─> Setup fee: $50,000
       └─> Monthly: $5,000 + 0.05% of volume

PHASE 2: TECHNICAL INTEGRATION
───────────────────────────────
Setting Up Anchor Infrastructure

Dashboard Access:
  ├─> Anchor Portal provided
  │    ├─ Custom enterprise dashboard
  │    ├─ Advanced analytics
  │    └─ White-label options
  │
  ├─> API Integration
  │    ├─ Dedicated API keys
  │    ├─ Webhook endpoints
  │    ├─ Rate limit: Unlimited
  │    └─> Production access
  │
  └─> Wallet Setup
       ├─> Multi-signature wallets
       │    ├─ Requires 3 of 5 signatures
       │    ├─ Cold storage integration
       │    └─> Hardware security modules (HSM)
       │
       ├─> Operational Wallets
       │    ├─ Hot wallet (liquidity)
       │    ├─ Warm wallet (reserves)
       │    └─ Cold wallet (long-term storage)
       │
       └─> Network Connections
            ├─ Stellar mainnet nodes
            ├─ Hedera mainnet nodes
            └─ Banking APIs

ASSET ISSUANCE:
  ├─> Issue Stablecoin
  │    ├─ Asset code: KKES (Kenyan Shilling)
  │    ├─ Issuing account created
  │    ├─ Distribution account setup
  │    └─> Asset listed on platform
  │
  └─> Configure Parameters
       ├─ Minimum deposit: 100 KES
       ├─ Maximum transaction: 10M KES
       ├─ Exchange rate source: CBK
       └─ Update frequency: Real-time

PHASE 3: LIQUIDITY PROVISIONING
────────────────────────────────
Setting Up Liquidity Pools

┌──────────────────────────────────────┐
│ 🏦 Anchor Dashboard                   │
│ → Liquidity Management                │
├──────────────────────────────────────┤
│                                       │
│ LIQUIDITY POOLS                      │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ KES/USDC Pool                  │  │
│ │ ├─ KES Balance:  50M          │  │
│ │ ├─ USDC Balance: 32,250        │  │
│ │ ├─ Total Value:  $64,500       │  │
│ │ └─ 24h Volume:   $2.3M         │  │
│ │ [Add Liquidity] [Remove]       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ NGN/USDC Pool                  │  │
│ │ ├─ NGN Balance: 75M            │  │
│ │ ├─ USDC Balance: 48,375        │  │
│ │ ├─ Total Value:  $96,750       │  │
│ │ └─ 24h Volume:   $1.8M         │  │
│ │ [Add Liquidity] [Remove]       │  │
│ └────────────────────────────────┘  │
│                                       │
│ [+ Create New Pool]                  │
└──────────────────────────────────────┘

ADD LIQUIDITY:
  ├─> Select pool: KES/USDC
  ├─> Add amounts:
  │    ├─ 10,000,000 KES
  │    └─ 6,452 USDC
  ├─> From account:
  │    └─> Link bank account or crypto wallet
  ├─> Confirm transaction
  └─> ✅ Liquidity added
       └─> Earning fees on transactions

PHASE 4: DEPOSIT OPERATIONS
────────────────────────────
User Deposits Fiat, Receives Stablecoin

USER INITIATES DEPOSIT:
Rowell User → Add Funds → Bank Transfer
  │
  ├─> Amount: 50,000 KES
  │
  ├─> System generates unique reference
  │    └─> REF: RW-KFS-20251006-ABC123
  │
  └─> Instructions shown:
       ├─ Bank: Kenya Commercial Bank
       ├─ Account: 1234567890
       ├─ Account Name: Rowell-KFS Liquidity
       ├─ Reference: RW-KFS-20251006-ABC123
       └─ Amount: 50,000.00 KES

ANCHOR RECEIVES NOTIFICATION:
┌──────────────────────────────────────┐
│ 🔔 New Deposit Pending                │
├──────────────────────────────────────┤
│                                       │
│ Reference: RW-KFS-20251006-ABC123    │
│ Amount: 50,000 KES                   │
│ From Bank: Detected via API          │
│ User: John Doe (verified)            │
│ Status: Pending confirmation         │
│                                       │
│ [Confirm Deposit] [Reject] [Flag]    │
└──────────────────────────────────────┘

ANCHOR PROCESS:
  ├─> Verify bank transfer received
  │    ├─ Check reference number
  │    ├─ Confirm amount
  │    └─> Validate user KYC
  │
  ├─> Calculate USDC to issue
  │    ├─ 50,000 KES ÷ 155 = 322.58 USDC
  │    ├─ Fee: 0.5% = 1.61 USDC
  │    └─> Net to user: 320.97 USDC
  │
  ├─> Issue Stablecoin
  │    ├─> Send 320.97 USDC to user wallet
  │    └─> Transaction confirmed on blockchain
  │
  └─> Update Records
       ├─> Database: Deposit completed
       ├─> Notify user: Funds available
       └─> Compliance: Transaction logged

ANCHOR DASHBOARD UPDATE:
┌──────────────────────────────────────┐
│ 📊 Today's Activity                   │
├──────────────────────────────────────┤
│                                       │
│ DEPOSITS                             │
│ Count: 127                           │
│ Volume: 12.4M KES                    │
│ Value: $80,000 USDC                  │
│                                       │
│ WITHDRAWALS                          │
│ Count: 98                            │
│ Volume: 9.2M KES                     │
│ Value: $59,355 USDC                  │
│                                       │
│ NET POSITION: +$20,645               │
│                                       │
│ [View Details]                       │
└──────────────────────────────────────┘

PHASE 5: WITHDRAWAL OPERATIONS
───────────────────────────────
User Withdraws USDC, Receives Fiat

USER INITIATES WITHDRAWAL:
Rowell User → Withdraw → Bank Account
  │
  ├─> Amount: 320 USDC
  │
  ├─> Select bank:
  │    ├─ Bank: Equity Bank
  │    ├─ Account: 0987654321
  │    └─ Account Name: John Doe
  │
  ├─> Confirm:
  │    ├─ 320 USDC → 49,600 KES
  │    ├─ Fee: 1% = 496 KES
  │    └─> Net: 49,104 KES
  │
  └─> Submit withdrawal request

ANCHOR RECEIVES NOTIFICATION:
┌──────────────────────────────────────┐
│ 🔔 New Withdrawal Request             │
├──────────────────────────────────────┤
│                                       │
│ Request ID: RW-KFS-W-20251006-XYZ789 │
│ Amount: 320 USDC → 49,104 KES        │
│ User: John Doe                       │
│ Bank: Equity Bank - 0987654321       │
│ Status: Pending processing           │
│                                       │
│ [Process] [Reject] [Request Info]    │
└──────────────────────────────────────┘

ANCHOR PROCESS:
  ├─> Verify withdrawal request
  │    ├─ Check user balance (sufficient?)
  │    ├─> Check daily limit (within limit?)
  │    └─> Compliance screening (clean?)
  │
  ├─> Receive USDC from user
  │    ├─> User's wallet debited: -320 USDC
  │    └─> Anchor wallet credited: +320 USDC
  │
  ├─> Initiate bank transfer
  │    ├─> Bank API: Transfer 49,104 KES
  │    ├─> To: Equity Bank - 0987654321
  │    └─> Reference: RW-KFS-W-20251006-XYZ789
  │
  └─> Update Status
       ├─> Pending → Processing → Complete
       ├─> Notify user: "Transfer initiated"
       └─> ETA: 1-2 business days

CONFIRMATION:
  ├─> Bank confirms transfer
  │    └─> Webhook from bank: Success
  │
  └─> Update records
       ├─> Status: Completed ✅
       ├─> User notified
       └─> Transaction archived

PHASE 6: COMPLIANCE & MONITORING
─────────────────────────────────
Ongoing Compliance Operations

┌──────────────────────────────────────┐
│ 🛡️ Compliance Dashboard               │
├──────────────────────────────────────┤
│                                       │
│ REAL-TIME MONITORING                 │
│ Active alerts: 3                     │
│ Flagged transactions: 12             │
│ Pending reviews: 8                   │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ ⚠️ Large Transaction Alert     │  │
│ │ User: Jane Smith                │  │
│ │ Amount: 95,000 USDC             │  │
│ │ Reason: Exceeds normal pattern  │  │
│ │ [Review] [Approve] [Flag]       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🔍 KYC Expiring Soon           │  │
│ │ 15 users need re-verification   │  │
│ │ [View List] [Send Reminders]    │  │
│ └────────────────────────────────┘  │
│                                       │
│ AML SCREENING (Past 24h)            │
│ ├─ Transactions screened: 2,345     │
│ ├─ Matches found: 2 (false positive)│
│ ├─ Escalated: 0                     │
│ └─ Response time: Avg 2.3 min       │
│                                       │
│ REGULATORY REPORTING                 │
│ ├─ Next report due: Oct 15           │
│ ├─ Status: Data ready                │
│ └─ [Generate Report] [Preview]       │
│                                       │
└──────────────────────────────────────┘

SUSPICIOUS ACTIVITY:
User attempts unusual pattern
  │
  ├─> Automated detection
  │    ├─ Multiple large transactions
  │    ├─ Rapid succession
  │    └─> Flag for review
  │
  ├─> Compliance Officer Review
  │    ├─ Check user history
  │    ├─ Review documentation
  │    ├─> Contact user for clarification
  │    └─> Decision: Legitimate business activity
  │
  └─> Resolution
       ├─> Clear flag
       ├─> Adjust user risk profile
       └─> Document decision

PHASE 7: REPORTING & ANALYTICS
───────────────────────────────
Business Intelligence

MONTHLY PERFORMANCE:
┌──────────────────────────────────────┐
│ 📊 October 2025 Performance           │
├──────────────────────────────────────┤
│                                       │
│ VOLUME                               │
│ Deposits: $12.4M (3,827 tx)          │
│ Withdrawals: $10.8M (3,231 tx)       │
│ Total Volume: $23.2M                 │
│ Growth: +18% MoM                     │
│                                       │
│ REVENUE                              │
│ Deposit fees: $62,000                │
│ Withdrawal fees: $108,000            │
│ Exchange spread: $58,000             │
│ Total Revenue: $228,000              │
│ Costs: $145,000                      │
│ Net Profit: $83,000                  │
│ Margin: 36.4%                        │
│                                       │
│ EFFICIENCY                           │
│ Avg deposit time: 12 minutes         │
│ Avg withdrawal time: 18 hours        │
│ Success rate: 99.7%                  │
│ Customer satisfaction: 4.7/5         │
│                                       │
│ [Export Report] [Share with Board]   │
└──────────────────────────────────────┘

REGULATORY REPORTING:
  └─> Generate quarterly report
       ├─ Transaction summary
       ├─ AML/KYC compliance
       ├─ Risk assessment
       ├─> Submit to Central Bank
       └─> Archive for audit
```

---

## 🎗️ PERSONA 4: NGO

### Profile

**Organization:** African Health Foundation  
**Type:** International NGO  
**Use Case:** Distribute aid, track donations, ensure transparency  
**Tech Savvy:** Medium  
**Transaction Volume:** Medium ($100K-$1M monthly)  
**Donor Requirements:** High transparency & reporting

### NGO Goals

✅ Transparent fund distribution  
✅ Real-time tracking for donors  
✅ Low-cost international transfers  
✅ Compliance with donor requirements  
✅ Impact reporting & analytics

---

### NGO Flow: Complete Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                     NGO: COMPLETE JOURNEY                        │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: NGO ONBOARDING
────────────────────────
Foundation Signs Up

Visit Rowell for NGOs
  │
  ├─> See features:
  │    ├─ 0.1% fees (vs 3-5% traditional)
  │    ├─ Real-time tracking
  │    ├─ Donor transparency
  │    └─> Save $50K annually on fees
  │
  ├─> Sign Up
  │    ├─ Organization email
  │    ├─ Organization name
  │    └─ Select: "NGO" account type
  │
  └─> NGO Profile Setup
       ├─ Legal name: African Health Foundation
       ├─ Registration number
       ├─ Country of registration: Kenya
       ├─ Tax-exempt status: Yes
       ├─ Focus area: Healthcare
       └─ Geographic coverage: 10 countries

PHASE 2: NGO VERIFICATION
──────────────────────────
Enhanced Due Diligence

Submit Documents:
  ├─ NGO registration certificate
  ├─ Tax exemption letter
  ├─ Board of directors list
  ├─ Latest financial audit
  ├─ Program descriptions
  ├─ Donor agreements
  └─ Compliance policies

Review Process (3-5 business days):
  ├─> Legal verification
  ├─> Financial assessment
  ├─> Program review
  └─> ✅ APPROVED
       ├─ Daily limit: $100,000
       ├─ Monthly limit: $5,000,000
       └─ Discounted fees: 0.05% (special NGO rate)

PHASE 3: PROGRAM SETUP
──────────────────────
Configure Aid Programs

┌──────────────────────────────────────┐
│ 🎗️ NGO Dashboard                      │
│ → Programs                            │
├──────────────────────────────────────┤
│                                       │
│ [+ Create New Program]               │
│                                       │
│ ACTIVE PROGRAMS                      │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 💉 COVID-19 Vaccination         │  │
│ │ Budget: $500,000                │  │
│ │ Spent: $342,000 (68%)           │  │
│ │ Countries: 5                    │  │
│ │ Beneficiaries: 15,234           │  │
│ │ [View] [Report] [Settings]      │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🏥 Healthcare Worker Support    │  │
│ │ Budget: $250,000                │  │
│ │ Spent: $180,500 (72%)           │  │
│ │ Countries: 3                    │  │
│ │ Beneficiaries: 523              │  │
│ │ [View] [Report] [Settings]      │  │
│ └────────────────────────────────┘  │
└──────────────────────────────────────┘

CREATE NEW PROGRAM:
┌──────────────────────────────────────┐
│ ➕ New Program                        │
├──────────────────────────────────────┤
│                                       │
│ Program Name:                        │
│ [Maternal Health Initiative]         │
│                                       │
│ Budget: [$100,000] USD               │
│                                       │
│ Duration:                            │
│ From: [Oct 1, 2025]                  │
│ To: [Sep 30, 2026]                   │
│                                       │
│ Countries:                           │
│ ☑ Kenya                              │
│ ☑ Uganda                             │
│ ☑ Tanzania                           │
│                                       │
│ Beneficiary Type:                    │
│ ● Direct beneficiaries               │
│ ○ Healthcare facilities              │
│ ○ Local organizations                │
│                                       │
│ Donor(s):                            │
│ [+ Add Donor]                        │
│                                       │
│ [Cancel] [Create Program]            │
└──────────────────────────────────────┘

PHASE 4: DONOR MANAGEMENT
──────────────────────────
Receiving Donations

DONOR PORTAL SETUP:
Dashboard → Donor Relations
┌──────────────────────────────────────┐
│ 💰 Donor Management                   │
├──────────────────────────────────────┤
│                                       │
│ ACTIVE DONORS                        │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🏢 Global Health Initiative     │  │
│ │ Total donated: $2,500,000       │  │
│ │ Current program: COVID-19       │  │
│ │ [View] [Report] [Contact]       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🌍 EU Health Fund               │  │
│ │ Total donated: $1,200,000       │  │
│ │ Current program: Multiple       │  │
│ │ [View] [Report] [Contact]       │  │
│ └────────────────────────────────┘  │
│                                       │
│ [+ Add New Donor]                    │
│                                       │
│ DONOR PORTAL                         │
│ Public link: rowel.li/donate/ahf     │
│ [Configure] [Preview] [Share]        │
└──────────────────────────────────────┘

DONATION RECEIVED:
Email: "New donation received"
┌──────────────────────────────────────┐
│ 💰 Donation Received                  │
├──────────────────────────────────────┤
│                                       │
│ Amount: $50,000                      │
│ From: Global Health Initiative       │
│ Program: COVID-19 Vaccination        │
│ Date: Oct 6, 2025                    │
│                                       │
│ Donor message:                       │
│ "Keep up the great work!"            │
│                                       │
│ [View Details] [Send Thank You]      │
└──────────────────────────────────────┘

AUTO-GENERATED RECEIPT:
└─> Email sent to donor
     ├─ Tax receipt (if applicable)
     ├─ Donation confirmation
     ├─ Program details
     └─> Tracking link for transparency

PHASE 5: FUND DISTRIBUTION
───────────────────────────
Distributing Aid to Beneficiaries

SCENARIO: Maternal Health Stipends
Goal: Distribute $200 to 500 pregnant women

Dashboard → Maternal Health Program → Distribute
┌──────────────────────────────────────┐
│ 💸 Distribute Funds                   │
├──────────────────────────────────────┤
│                                       │
│ Program: Maternal Health Initiative  │
│ Available: $100,000                  │
│                                       │
│ DISTRIBUTION METHOD                  │
│                                       │
│ ● Bulk distribution                  │
│ ○ Individual payments                │
│ ○ Scheduled payments                 │
│                                       │
│ [Continue]                           │
└──────────────────────────────────────┘

BULK DISTRIBUTION:
┌──────────────────────────────────────┐
│ 📄 Upload Beneficiary List            │
├──────────────────────────────────────┤
│                                       │
│ Upload CSV file with:                │
│ • Beneficiary name                   │
│ • Phone number or wallet address     │
│ • Amount                             │
│ • Location                           │
│ • Notes (optional)                   │
│                                       │
│ [Download Template]                  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 📁 Drag file here or            │  │
│ │    [Browse Files]               │  │
│ └────────────────────────────────┘  │
│                                       │
└──────────────────────────────────────┘

FILE UPLOADED:
┌──────────────────────────────────────┐
│ ✅ File Processed                     │
├──────────────────────────────────────┤
│                                       │
│ Beneficiaries found: 500             │
│ Valid entries: 497 ✅                │
│ Errors: 3 ❌                         │
│                                       │
│ [View Errors] [Fix and Re-upload]    │
│                                       │
│ SUMMARY                              │
│ Total amount: $99,400                │
│ Fee (0.05%): $49.70                  │
│ Total cost: $99,449.70               │
│                                       │
│ Estimated time: 5 minutes            │
│                                       │
│ ☑ I confirm the beneficiary list     │
│   is accurate                        │
│                                       │
│ [Cancel] [Distribute Funds]          │
└──────────────────────────────────────┘

DISTRIBUTION IN PROGRESS:
┌──────────────────────────────────────┐
│ 🔄 Processing Distributions...        │
├──────────────────────────────────────┤
│                                       │
│ ████████████░░░░░░░░░  65%           │
│                                       │
│ Completed: 323 / 497                 │
│ In progress: 12                      │
│ Pending: 162                         │
│ Failed: 0                            │
│                                       │
│ Estimated time remaining: 2 min      │
│                                       │
│ [View Details] [Pause] [Cancel]      │
└──────────────────────────────────────┘

DISTRIBUTION COMPLETE:
┌──────────────────────────────────────┐
│ ✅ Distribution Complete!             │
├──────────────────────────────────────┤
│                                       │
│ 🎉 497 payments sent successfully    │
│                                       │
│ SUMMARY                              │
│ ├─ Successful: 497 ✅                │
│ ├─ Failed: 0 ❌                      │
│ ├─ Total distributed: $99,400        │
│ ├─ Total fees: $49.70                │
│ └─ Time taken: 4 minutes             │
│                                       │
│ All beneficiaries notified via SMS   │
│                                       │
│ [View Report] [Download Receipt]     │
│ [Notify Donors]                      │
└──────────────────────────────────────┘

BENEFICIARY RECEIVES:
SMS to beneficiary:
─────────────────────────────────────
Good news! You've received $200 from
African Health Foundation for the
Maternal Health Program.

To access:
1. Download Rowell app
2. Create account: rowel.li/get
3. Your funds are waiting!

Questions? Call: +254-XXX-XXXX
─────────────────────────────────────

PHASE 6: TRACKING & TRANSPARENCY
─────────────────────────────────
Real-time Tracking for Donors

DONOR DASHBOARD:
Public link shared with donors
┌──────────────────────────────────────┐
│ 🌍 African Health Foundation          │
│ COVID-19 Vaccination Program         │
├──────────────────────────────────────┤
│                                       │
│ YOUR CONTRIBUTION                    │
│ Total donated: $50,000               │
│ Date: Oct 6, 2025                    │
│                                       │
│ PROGRAM PROGRESS                     │
│ ████████████████████░░  87%          │
│                                       │
│ Total budget: $500,000               │
│ Spent: $436,000                      │
│ Remaining: $64,000                   │
│                                       │
│ IMPACT                               │
│ ├─ 18,234 people vaccinated          │
│ ├─ 523 healthcare workers trained    │
│ ├─ 45 clinics supported              │
│ └─ 5 countries reached               │
│                                       │
│ RECENT ACTIVITY                      │
│ Oct 6: $5,000 → Clinic supplies      │
│ Oct 5: $12,000 → Healthcare workers  │
│ Oct 4: $3,500 → Transport            │
│                                       │
│ [View All Transactions]              │
│ [Download Report]                    │
└──────────────────────────────────────┘

TRANSACTION TRANSPARENCY:
Every transaction visible
┌──────────────────────────────────────┐
│ 📊 All Transactions                   │
├──────────────────────────────────────┤
│                                       │
│ [Filters: Date ▼ Type ▼ Country ▼]   │
│                                       │
│ Oct 6, 2025                          │
│ ┌────────────────────────────────┐  │
│ │ Payment to: Dr. Jane Kimani     │  │
│ │ Amount: $200                    │  │
│ │ Purpose: Maternal health visit  │  │
│ │ Location: Nairobi, Kenya        │  │
│ │ Status: ✅ Completed             │  │
│ │ [Blockchain proof]              │  │
│ └────────────────────────────────┘  │
│                                       │
│ Oct 6, 2025                          │
│ ┌────────────────────────────────┐  │
│ │ Payment to: Mercy Hospital      │  │
│ │ Amount: $5,000                  │  │
│ │ Purpose: Medical supplies       │  │
│ │ Location: Kampala, Uganda       │  │
│ │ Status: ✅ Completed             │  │
│ │ [View invoice] [Blockchain]     │  │
│ └────────────────────────────────┘  │
│                                       │
│ [Load More] [Export CSV]             │
└──────────────────────────────────────┘

PHASE 7: IMPACT REPORTING
──────────────────────────
Quarterly Donor Reports

Generate Report:
Dashboard → Reports → Quarterly
┌──────────────────────────────────────┐
│ 📊 Q3 2025 Impact Report              │
│ COVID-19 Vaccination Program         │
├──────────────────────────────────────┤
│                                       │
│ FINANCIAL SUMMARY                    │
│ Opening balance: $158,000            │
│ Donations received: $280,000         │
│ Total available: $438,000            │
│ Spent: $342,000                      │
│ Closing balance: $96,000             │
│                                       │
│ SPENDING BREAKDOWN                   │
│ ├─ Direct aid: 65% ($222,300)        │
│ ├─ Healthcare workers: 20% ($68,400) │
│ ├─ Medical supplies: 10% ($34,200)   │
│ ├─ Operations: 4% ($13,680)          │
│ └─ Fees: 0.05% ($171)               │
│                                       │
│ IMPACT METRICS                       │
│ ├─ People reached: 18,234            │
│ ├─ Vaccines administered: 17,890     │
│ ├─ Healthcare workers: 523           │
│ ├─ Clinics supported: 45             │
│ └─ Countries: Kenya, Uganda, etc.    │
│                                       │
│ TESTIMONIALS                         │
│ "This program saved my life..."      │
│ - Mary K., Beneficiary              │
│                                       │
│ PHOTOS & STORIES                     │
│ [12 photos attached]                 │
│                                       │
│ NEXT QUARTER PLANS                   │
│ • Expand to Tanzania                 │
│ • Train 200 more workers             │
│ • Target: 10,000 more people         │
│                                       │
│ [Download PDF] [Email to Donors]     │
│ [Share on Social Media]              │
└──────────────────────────────────────┘

AUTOMATED DONOR EMAILS:
  └─> Send to all donors
       ├─ Personalized message
       ├─ Their contribution highlighted
       ├─ Impact metrics
       ├─ Photos & stories
       ├─ Blockchain transaction links
       └─> Call to action: "Donate again?"

PHASE 8: COMPLIANCE & AUDIT
────────────────────────────
Annual Audit Preparation

Dashboard → Compliance → Audit
┌──────────────────────────────────────┐
│ 🔍 Audit Preparation                  │
├──────────────────────────────────────┤
│                                       │
│ FINANCIAL YEAR: 2025                 │
│                                       │
│ DOCUMENTATION STATUS                 │
│ ☑ All transactions recorded          │
│ ☑ Receipts attached (100%)           │
│ ☑ Donor agreements filed             │
│ ☑ Compliance checks passed           │
│ ☑ Blockchain proofs available        │
│                                       │
│ EXPORT OPTIONS                       │
│ [Financial Statements]               │
│ [Transaction Register]               │
│ [Donor Reports]                      │
│ [Program Summaries]                  │
│ [Blockchain Audit Trail]             │
│                                       │
│ AUDITOR ACCESS                       │
│ Grant read-only access to auditor    │
│ Email: [auditor@firm.com]            │
│ [Send Invitation]                    │
│                                       │
└──────────────────────────────────────┘

BENEFITS FOR NGO:
✅ 100% transaction transparency
✅ Real-time donor visibility
✅ Automated compliance
✅ Reduced fees (0.05% vs 3-5%)
✅ Instant global distribution
✅ Easy audit preparation
✅ Enhanced donor trust
```

---

## 🔄 Cross-Persona Interactions

### User → Merchant Payment

```
Individual User Pays Merchant

User at Coffee Shop:
  ├─> Scan merchant QR code
  ├─> Amount auto-filled: 350 KES
  ├─> Confirm payment
  └─> ✅ Merchant notified instantly

Both parties happy:
  ├─ User: Fast, low-fee payment
  └─ Merchant: Instant settlement
```

### Donor → NGO → Beneficiary Flow

```
Complete Donation Journey

1. Donor contributes
   └─> $50,000 to NGO program

2. NGO receives & allocates
   └─> Assign to maternal health program

3. NGO distributes to beneficiaries
   └─> 250 women receive $200 each

4. Donor tracks impact
   └─> Real-time dashboard shows progress

All transparent and traceable! ✅
```

### User → Anchor → User (Cross-border)

```
User A (Nigeria) → User B (Kenya)

1. User A deposits NGN with Anchor A (Nigeria)
   └─> Receives USDC

2. User A sends USDC to User B
   └─> 3-second blockchain transfer

3. User B withdraws via Anchor B (Kenya)
   └─> Receives KES

Total time: < 1 day (vs 3-5 days traditional)
Total cost: 0.6% (vs 8-12% traditional)
```

---

## 📊 Persona Comparison Matrix

| Feature | Individual | Merchant | Anchor | NGO |
|---------|-----------|----------|--------|-----|
| **Primary Goal** | Send/receive money | Accept payments | Provide liquidity | Distribute aid |
| **Verification** | Basic KYC | Business KYC | Full licensing | NGO registration |
| **Transaction Volume** | Low-Medium | Medium-High | Very High | Medium |
| **Fees** | 0.1% | 0.1% | 0.05% + spread | 0.05% (discounted) |
| **Daily Limit** | $10,000 | $50,000 | Unlimited | $100,000 |
| **Key Features** | Wallet, quick send | POS, reports | Liquidity pools, compliance | Programs, transparency |
| **Dashboard Complexity** | Low | Medium | High | Medium-High |
| **Support Level** | Self-service | Email + chat | Dedicated account manager | Priority support |

---

## ✅ UX Best Practices for Each Persona

### Individual User
- 📱 Mobile-first design
- ⚡ Quick actions for common tasks
- 👥 Easy contact management
- 📊 Simple spending insights

### Merchant
- 💻 Tablet-optimized POS interface
- 🔔 Instant payment notifications
- 📈 Business analytics & reports
- 🔗 Easy integration options

### Anchor
- 🖥️ Desktop-focused dashboard
- 📊 Advanced analytics & monitoring
- 🔐 Enterprise-grade security
- 🔌 API-first architecture

### NGO
- 🌍 Transparency features
- 📄 Donor reporting tools
- 💸 Bulk distribution capabilities
- 📸 Impact documentation

---

## 📚 Related Documentation

- [Overview User Flows](overview.md)
- [Remittance Sender Journey](remittance-sender-journey.md)
- [Wallet User Flow](wallet-user-flow.md)
- [API Documentation](../api/README.md)
- [Technical Architecture](../architecture/overview.md)

---

**Document Version:** 1.0  
**Last Updated:** October 6, 2025  
**Author:** UX Team - Rowell Infrastructure  
**Status:** ✅ Ready for Implementation

---

*Built with for Africa by the Rowell Infrastructure Team* 

