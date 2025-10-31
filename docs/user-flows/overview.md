# User Flow Documentation - Rowell Infrastructure

> **Comprehensive User Experience Flows for African Fintech Platform**

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Core User Flows](#core-user-flows)
3. [Authentication & Onboarding](#authentication--onboarding)
4. [Account Management](#account-management)
5. [Transaction Flows](#transaction-flows)
6. [Compliance & Verification](#compliance--verification)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

---

## Introduction

This document outlines the user experience flows for Rowell Infrastructure, a blockchain-based payment platform designed for African fintech applications. The platform supports multiple user personas and use cases, with a focus on simplicity, security, and compliance.

### Platform Overview

**Rowell Infrastructure** provides:
- ⚡ **Instant cross-border payments** (3-second settlements)
- 💰 **Low-cost transactions** (0.1% fees)
- 🔐 **Built-in compliance** (KYC/AML for African markets)
- 🌍 **Multi-network support** (Stellar & Hedera blockchains)

### User Personas

The platform serves four primary personas:

1. **👤 Individual Users** - Send/receive money, manage personal wallets
2. **🏪 Merchants** - Accept payments, manage business transactions
3. **🏦 Anchors** - Financial institutions providing fiat on/off ramps
4. **🎗️ NGOs** - Distribute aid, manage donor funds transparently

---

## Core User Flows

### High-Level User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER JOURNEY OVERVIEW                        │
└─────────────────────────────────────────────────────────────────┘

1. DISCOVER
   └─> Landing page → Learn about platform → Sign up

2. ONBOARD
   └─> Create account → Verify identity → Setup wallet

3. TRANSACT
   └─> Fund wallet → Send/receive money → Track transactions

4. MANAGE
   └─> View balances → Check history → Manage settings

5. GROW
   └─> Explore features → Integrate APIs → Build applications
```

### Primary User Actions

| Action | User Type | Priority | Complexity |
|--------|-----------|----------|------------|
| **Send Money** | All | High | Medium |
| **Receive Money** | All | High | Low |
| **Create Account** | All | High | Low |
| **Verify Identity** | All | High | Medium |
| **Check Balance** | All | High | Low |
| **View History** | All | Medium | Low |
| **Accept Payments** | Merchant | High | Medium |
| **Distribute Funds** | NGO | High | Medium |
| **Provide Liquidity** | Anchor | Medium | High |

---

## Authentication & Onboarding

### User Registration Flow

```
START → Landing Page
  │
  ├─→ NEW USER
  │    └─> Click "Sign Up"
  │         │
  │         ├─> Enter Email & Password
  │         │    ├─ Validate: Email format
  │         │    ├─ Validate: Password strength
  │         │    └─ Check: Email not already registered
  │         │
  │         ├─> Select Account Type
  │         │    ├─ Individual User
  │         │    ├─ Merchant
  │         │    ├─ Anchor
  │         │    └─ NGO
  │         │
  │         ├─> Select Country
  │         │    └─ List: 20+ African countries
  │         │
  │         ├─> Verify Email
  │         │    ├─> Send verification code
  │         │    ├─> Enter code
  │         │    └─> Confirm email
  │         │
  │         └─> CREATE ACCOUNT → Dashboard
  │
  └─→ EXISTING USER
       └─> Click "Log In"
            │
            ├─> Enter Credentials
            │    ├─ Email/Username
            │    └─ Password
            │
            ├─> [Optional] 2FA
            │    └─ Enter 2FA code
            │
            └─> LOGIN SUCCESS → Dashboard
```

### Account Type Selection Guide

**Decision Matrix:**

| If you want to... | Choose... |
|-------------------|-----------|
| Send money to family/friends | **Individual User** |
| Accept payments for your business | **Merchant** |
| Provide banking services | **Anchor** |
| Distribute aid or donations | **NGO** |

### Onboarding Checklist

```
☐ Step 1: Create Account (2 minutes)
   ├─ Enter basic information
   ├─ Select account type
   └─ Verify email

☐ Step 2: Verify Identity (5 minutes)
   ├─ Upload ID document
   ├─ Enter ID number (BVN, National ID, etc.)
   └─ Wait for verification

☐ Step 3: Setup Blockchain Wallet (1 minute)
   ├─ Choose network (Stellar/Hedera)
   ├─ Auto-generate wallet address
   └─ Backup secret key

☐ Step 4: Fund Wallet (5 minutes)
   ├─ Select funding method
   ├─ Complete payment
   └─ Wait for confirmation

☐ Step 5: Start Transacting! 🎉
```

---

## Account Management

### Wallet Setup Flow

```
Dashboard → Wallet Section
  │
  ├─→ CREATE NEW WALLET
  │    │
  │    ├─> Select Network
  │    │    ├─ Stellar (Recommended for most users)
  │    │    └─ Hedera (For enterprises)
  │    │
  │    ├─> Select Environment
  │    │    ├─ Testnet (For testing)
  │    │    └─ Mainnet (For real transactions)
  │    │
  │    ├─> GENERATE WALLET
  │    │    ├─ Creating keypair...
  │    │    ├─ Funding account...
  │    │    └─ Success!
  │    │
  │    └─> BACKUP SECRET KEY ⚠️
  │         ├─> Display secret key
  │         ├─> Warning: "Store securely!"
  │         ├─> User confirms backup
  │         │    ├─ Download as file
  │         │    ├─ Copy to clipboard
  │         │    └─ Write down manually
  │         │
  │         └─> WALLET CREATED → Dashboard
  │
  └─→ IMPORT EXISTING WALLET
       │
       ├─> Enter Secret Key
       │    └─ Validate key format
       │
       ├─> Verify Ownership
       │    └─ Sign test message
       │
       └─> IMPORT SUCCESS → Dashboard
```

### Balance & Assets View

```
Wallet Dashboard
  │
  ├─→ TOTAL BALANCE
  │    ├─ Display in USD
  │    ├─ Display in local currency
  │    └─ Refresh button
  │
  ├─→ ASSET LIST
  │    ├─ USDC balance
  │    ├─ Native token balance (XLM/HBAR)
  │    ├─ Other tokens
  │    └─ [Button] Add custom asset
  │
  ├─→ RECENT TRANSACTIONS
  │    ├─ Last 5 transactions
  │    ├─ Amount & direction (↑/↓)
  │    ├─ Status indicator
  │    └─ [Link] View all
  │
  └─→ QUICK ACTIONS
       ├─ [Button] Send Money
       ├─ [Button] Receive Money
       ├─ [Button] Add Funds
       └─ [Button] Request Payment
```

---

## Transaction Flows

### Send Money Flow

*Detailed in [remittance-sender-journey.md](remittance-sender-journey.md)*

```
Dashboard → Send Money
  │
  ├─> ENTER RECIPIENT
  │    ├─ Scan QR code
  │    ├─ Select from contacts
  │    ├─ Enter wallet address
  │    └─ Enter phone/email (if integrated)
  │
  ├─> ENTER AMOUNT
  │    ├─ Input amount
  │    ├─ Select currency (USDC, local)
  │    ├─ View conversion rate
  │    └─ Display fee (0.1%)
  │
  ├─> REVIEW DETAILS
  │    ├─ Recipient address
  │    ├─ Amount to send
  │    ├─ Estimated fee
  │    ├─ Total cost
  │    └─ [Optional] Add memo
  │
  ├─> CONFIRM TRANSACTION
  │    ├─ Enter password/PIN
  │    ├─ [Optional] 2FA
  │    └─ Submit transaction
  │
  ├─> PROCESSING (3 seconds)
  │    ├─ Broadcasting to network...
  │    ├─ Waiting for confirmation...
  │    └─ Success! ✅
  │
  └─> TRANSACTION COMPLETE
       ├─ Show transaction hash
       ├─ Receipt available
       ├─ [Button] Share receipt
       └─ [Button] Send another
```

### Receive Money Flow

```
Dashboard → Receive Money
  │
  ├─> SHARE YOUR ADDRESS
  │    ├─ Display QR code
  │    ├─ Display wallet address
  │    ├─ [Button] Copy address
  │    └─ [Button] Share via...
  │         ├─ WhatsApp
  │         ├─ Email
  │         ├─ SMS
  │         └─ More options
  │
  ├─> [Optional] REQUEST SPECIFIC AMOUNT
  │    ├─> Enter amount
  │    ├─> Select currency
  │    ├─> Add note/description
  │    └─> Generate payment request
  │         ├─ QR code with amount
  │         ├─ Shareable link
  │         └─ [Button] Share request
  │
  └─> INCOMING PAYMENT NOTIFICATION
       ├─ Push notification
       ├─ Email notification
       ├─ In-app notification
       └─ [Button] View transaction
```

---

## Compliance & Verification

### KYC Verification Flow

```
Dashboard → Account Settings → Verify Identity
  │
  ├─> SELECT VERIFICATION TYPE
  │    ├─ Individual
  │    ├─ Business
  │    └─ NGO
  │
  ├─> ENTER PERSONAL INFORMATION
  │    ├─ First Name
  │    ├─ Last Name
  │    ├─ Date of Birth
  │    ├─ Phone Number
  │    └─ Address
  │
  ├─> UPLOAD DOCUMENTS
  │    │
  │    ├─> Select ID Type
  │    │    ├─ National ID
  │    │    ├─ Passport
  │    │    ├─ Driver's License
  │    │    └─ BVN (Nigeria)
  │    │
  │    ├─> Upload Front Image
  │    │    ├─ Take photo
  │    │    ├─ Upload from device
  │    │    └─ Validate image quality
  │    │
  │    └─> [If passport/ID card] Upload Back
  │
  ├─> [Optional] SELFIE VERIFICATION
  │    ├─ Take live selfie
  │    ├─ Face liveness check
  │    └─ Match with ID photo
  │
  ├─> SUBMIT FOR REVIEW
  │    ├─ Processing...
  │    └─ "Verification submitted!"
  │
  └─> VERIFICATION STATUS
       ├─ Pending (1-24 hours)
       ├─ Under Review (Receive updates)
       ├─ Approved ✅ (Full access)
       └─ Rejected ❌ (Reason provided)
            └─> [Button] Resubmit with corrections
```

### Transaction Compliance Check

```
User Initiates Transaction
  │
  ├─> AUTOMATIC COMPLIANCE CHECK
  │    │
  │    ├─> KYC Status Check
  │    │    ├─ Verified → Continue
  │    │    └─ Not Verified → Prompt verification
  │    │
  │    ├─> AML Screening
  │    │    ├─ Check sender reputation
  │    │    ├─ Check recipient reputation
  │    │    └─ Analyze transaction pattern
  │    │
  │    ├─> Transaction Limits
  │    │    ├─ Check daily limit
  │    │    ├─ Check monthly limit
  │    │    └─ Check per-transaction limit
  │    │
  │    └─> Risk Assessment
  │         ├─ Low Risk → Auto-approve
  │         ├─ Medium Risk → Additional verification
  │         └─ High Risk → Manual review
  │
  └─> RESULT
       ├─ APPROVED → Process transaction
       ├─ FLAGGED → Request more info
       └─ BLOCKED → Show reason & next steps
```

---

## Error Handling

### Common Error Scenarios

#### 1. Insufficient Balance

```
User attempts to send $100
Wallet balance: $50
  │
  └─> ERROR: "Insufficient balance"
       │
       ├─> Show current balance
       ├─> Show amount needed
       └─> [Button] Add Funds
            └─> Redirect to funding flow
```

#### 2. Invalid Recipient Address

```
User enters recipient address
Validation fails
  │
  └─> ERROR: "Invalid wallet address"
       │
       ├─> Highlight error field
       ├─> Show format example
       ├─> Suggest: "Scan QR code instead?"
       └─> [Button] Scan QR Code
```

#### 3. Network Error

```
Transaction submission fails
Network timeout/error
  │
  └─> ERROR: "Network error"
       │
       ├─> Show error message
       ├─> "Transaction not submitted"
       ├─> [Button] Try Again
       └─> [Button] Check Network Status
```

#### 4. KYC Not Complete

```
User attempts large transaction
KYC not verified
  │
  └─> WARNING: "Verification required"
       │
       ├─> Explain transaction limits
       ├─> Show current limit vs requested
       ├─> Benefits of verification
       └─> [Button] Verify Identity Now
            └─> Redirect to KYC flow
```

### Error Message Best Practices

**❌ Bad Error Message:**
```
"Error code: 500. Transaction failed."
```

**✅ Good Error Message:**
```
"Unable to send payment"
"The recipient's wallet might be temporarily unavailable. 
Please try again in a few minutes or contact support if the problem persists."
[Button] Try Again  [Button] Contact Support
```

---

## Best Practices

### UX Principles

1. **🎯 Progressive Disclosure**
   - Show essential information first
   - Reveal advanced features as needed
   - Keep primary actions prominent

2. **⚡ Speed & Efficiency**
   - Minimize steps in critical flows
   - Pre-fill information when possible
   - Show loading states (3-second rule)

3. **🛡️ Security & Trust**
   - Confirm destructive actions
   - Show security indicators
   - Explain why information is needed

4. **🌍 Localization**
   - Support local languages
   - Show amounts in local currency
   - Adapt to local payment preferences

5. **📱 Mobile-First**
   - Design for small screens first
   - Touch-friendly buttons (44px minimum)
   - Optimize for slow connections

### Accessibility Considerations

- **Visual**: High contrast, large text options, screen reader support
- **Cognitive**: Clear language, consistent patterns, undo options
- **Motor**: Large touch targets, keyboard navigation, voice input
- **Network**: Offline mode, low-data mode, progressive enhancement

### Transaction Confirmation Pattern

```
BEFORE TRANSACTION
  ├─ Clear summary of what will happen
  ├─ Total cost breakdown (amount + fees)
  ├─ Estimated time to completion
  └─ Confirm/Cancel options (equal prominence)

DURING TRANSACTION
  ├─ Progress indicator with steps
  ├─ Estimated time remaining
  ├─ "Cancel" option (if possible)
  └─ What's happening explanation

AFTER TRANSACTION
  ├─ Clear success/failure message
  ├─ Transaction details
  ├─ Receipt/proof
  └─ Next steps / suggested actions
```

---

## Navigation Structure

### Primary Navigation

```
┌─────────────────────────────────────────────────────────┐
│ [Logo] Rowell                    [Notifications] [User] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Dashboard  |  Wallet  |  Transactions  |  Analytics    │
│                                                          │
└─────────────────────────────────────────────────────────┘

MOBILE:
┌──────────────────────┐
│ ≡ Rowell    🔔 👤   │
├──────────────────────┤
│                      │
│  [Content Area]      │
│                      │
├──────────────────────┤
│ 🏠  💰  📊  ⚙️      │
└──────────────────────┘
```

### Information Architecture

```
Rowell Infrastructure
│
├─ Dashboard (Home)
│  ├─ Quick stats
│  ├─ Recent activity
│  └─ Quick actions
│
├─ Wallet
│  ├─ Balances
│  ├─ Send money
│  ├─ Receive money
│  └─ Transaction history
│
├─ Transactions
│  ├─ All transactions
│  ├─ Pending
│  ├─ Completed
│  └─ Failed
│
├─ Analytics (Merchant/NGO/Anchor)
│  ├─ Payment flows
│  ├─ Revenue reports
│  ├─ Customer insights
│  └─ Export data
│
└─ Settings
   ├─ Profile
   ├─ Security
   ├─ Verification
   ├─ Notifications
   └─ Support
```

---

## Notification Strategy

### Notification Types

| Type | Trigger | Channel | Priority |
|------|---------|---------|----------|
| **Transaction Sent** | Money sent successfully | Push + Email | High |
| **Transaction Received** | Money received | Push + SMS + Email | High |
| **Transaction Failed** | Transaction failed | Push + Email | High |
| **Low Balance** | Balance below threshold | Push | Medium |
| **KYC Approved** | Verification complete | Push + Email | High |
| **Security Alert** | Suspicious activity | Push + SMS + Email | Critical |
| **New Feature** | Product updates | Email | Low |

### Notification Format

```
PUSH NOTIFICATION:
┌────────────────────────────────┐
│ 💰 Payment Received            │
│ +$100.00 USDC from John Doe    │
│ Tap to view transaction        │
└────────────────────────────────┘

EMAIL NOTIFICATION:
Subject: ✅ Payment Received - $100.00

Hi Sarah,

You've received $100.00 USDC from John Doe.

Transaction Details:
- Amount: $100.00 USDC
- From: John Doe (GD2K...3F4H)
- Date: Oct 6, 2025 at 2:45 PM
- Status: Completed ✅

[View Transaction] [View Wallet]

Best regards,
The Rowell Team
```

---

## Success Metrics

### Key UX Metrics to Track

1. **Time to First Transaction** (Target: < 10 minutes)
2. **Transaction Success Rate** (Target: > 99%)
3. **User Onboarding Completion** (Target: > 80%)
4. **KYC Verification Time** (Target: < 24 hours)
5. **User Satisfaction Score** (Target: > 4.5/5)

### User Journey Analytics

```
Funnel Analysis:
- Landing Page Views: 10,000
  └─> Sign Up Started: 3,000 (30%)
      └─> Account Created: 2,400 (80%)
          └─> KYC Submitted: 1,920 (80%)
              └─> KYC Approved: 1,728 (90%)
                  └─> First Transaction: 1,382 (80%)

Drop-off Points to Optimize:
1. Landing → Sign Up (70% drop-off) - Improve value prop
2. KYC → First Transaction (20% drop-off) - Simplify funding
```

---

## Related Documentation

- 📱 [Remittance Sender Journey](remittance-sender-journey.md)
- 💰 [Wallet User Flow](wallet-user-flow.md)
- 👥 [Persona Interaction Flows](persona-interaction-flows.md)
- 🏪 [Merchant-Specific Flows](merchant-flows.md)
- 🎗️ [NGO-Specific Flows](ngo-flows.md)
- 🏦 [Anchor-Specific Flows](anchor-flows.md)

---

**Document Version:** 1.0  
**Last Updated:** October 6, 2025  
**Author:** UX Team - Rowell Infrastructure  
**Status:** ✅ Ready for Review

---

*Built with ❤️ for Africa by the Rowell Infrastructure Team* 🌍

