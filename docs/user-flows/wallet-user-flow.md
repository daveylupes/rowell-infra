# Wallet User Flow

> **Complete User Experience for Digital Wallet Management**

## 📋 Overview

This document details the user experience for managing digital wallets on Rowell Infrastructure. The wallet is the core of the user experience, serving as the gateway to blockchain-based payments in Africa.

### What is a Rowell Wallet?

A **Rowell Wallet** is a blockchain-based digital wallet that allows users to:
- Store and manage stablecoins (USDC, USDT) and native tokens (XLM, HBAR)
- Send and receive money instantly across African borders
- Track transaction history and balances
- Maintain security through encryption and private keys

---

## 🎯 Wallet User Goals

### Primary Goals

✅ **Secure Storage** - Keep money safe with bank-level security  
✅ **Easy Access** - Check balance and transact anytime, anywhere  
✅ **Quick Transactions** - Send/receive money in seconds  
✅ **Clear Visibility** - See all assets and transaction history  
✅ **Control** - Manage multiple wallets and currencies

### User Concerns

❓ "Is my money safe?"  
❓ "What if I lose my phone?"  
❓ "Can I trust this new technology?"  
❓ "How do I get my money out?"  
❓ "What are the fees?"

---

## 🚀 Wallet Setup Flow

### First-Time Wallet Creation

```
┌─────────────────────────────────────────────────────────────────┐
│                     WALLET CREATION JOURNEY                      │
└─────────────────────────────────────────────────────────────────┘

START: New User Registration Complete
  │
  ├─> AUTOMATIC WALLET OFFER
  │    ┌────────────────────────────────────┐
  │    │ 🎉 Welcome to Rowell!              │
  │    ├────────────────────────────────────┤
  │    │ Let's set up your digital wallet   │
  │    │ to start sending and receiving     │
  │    │ money.                             │
  │    │                                     │
  │    │ Your wallet will be:               │
  │    │ ✓ Created instantly                │
  │    │ ✓ Secured with encryption          │
  │    │ ✓ Ready to use immediately         │
  │    │                                     │
  │    │ [Create My Wallet] [Learn More]    │
  │    └────────────────────────────────────┘
  │
  ├─> NETWORK SELECTION
  │    ┌────────────────────────────────────┐
  │    │ 📡 Choose Your Network              │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │ ⭐ RECOMMENDED FOR YOU              │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 🌟 Stellar Network           │  │
  │    │ │                               │  │
  │    │ │ • Fastest for Africa          │  │
  │    │ │ • Lowest fees (0.00001 XLM)  │  │
  │    │ │ • Best for remittances       │  │
  │    │ │                               │  │
  │    │ │ [Select Stellar] ✓           │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ ALTERNATIVE                         │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 🏢 Hedera Network            │  │
  │    │ │                               │  │
  │    │ │ • Enterprise-grade           │  │
  │    │ │ • Fixed low fees             │  │
  │    │ │ • Great for businesses       │  │
  │    │ │                               │  │
  │    │ │ [Select Hedera]              │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ 💡 You can create wallets on       │
  │    │    both networks later             │
  │    └────────────────────────────────────┘
  │
  ├─> ENVIRONMENT SELECTION
  │    ┌────────────────────────────────────┐
  │    │ 🧪 Choose Environment               │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 🧪 Testnet (Practice Mode)   │  │
  │    │ │                               │  │
  │    │ │ Perfect for:                  │  │
  │    │ │ • First-time users           │  │
  │    │ │ • Testing features           │  │
  │    │ │ • Learning the platform      │  │
  │    │ │                               │  │
  │    │ │ Uses fake money (no risk!)   │  │
  │    │ │                               │  │
  │    │ │ [Use Testnet] ⭐             │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 💰 Mainnet (Real Money)      │  │
  │    │ │                               │  │
  │    │ │ For users ready to:           │  │
  │    │ │ • Send real money            │  │
  │    │ │ • Receive payments           │  │
  │    │ │ • Use production features    │  │
  │    │ │                               │  │
  │    │ │ Requires KYC verification    │  │
  │    │ │                               │  │
  │    │ │ [Use Mainnet]                │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ [← Back]             [Continue →]  │
  │    └────────────────────────────────────┘
  │
  ├─> CREATING WALLET
  │    ┌────────────────────────────────────┐
  │    │ 🔄 Creating Your Wallet...          │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │     [Animated spinner/progress]    │
  │    │                                     │
  │    │ ✓ Generating secure keys...        │
  │    │ ✓ Creating blockchain account...   │
  │    │ ✓ Funding with base reserve...     │
  │    │ ⏳ Finalizing setup...              │
  │    │                                     │
  │    │ This will take about 10 seconds    │
  │    └────────────────────────────────────┘
  │
  ├─> WALLET CREATED SUCCESS
  │    ┌────────────────────────────────────┐
  │    │ ✅ Wallet Created Successfully!     │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │   [Large checkmark animation]      │
  │    │                                     │
  │    │ Your digital wallet is ready!      │
  │    │                                     │
  │    │ Wallet Address:                    │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ GABC123...XYZ789             │  │
  │    │ │ [📋 Copy] [📱 Share QR]      │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ Network: Stellar Testnet           │
  │    │ Balance: 0.00 USDC                 │
  │    │                                     │
  │    │ [Continue] →                        │
  │    └────────────────────────────────────┘
  │
  └─> CRITICAL: BACKUP SECRET KEY
       ┌────────────────────────────────────┐
       │ ⚠️ Important: Backup Your Keys      │
       ├────────────────────────────────────┤
       │                                     │
       │ Your SECRET KEY gives you access   │
       │ to your wallet. Keep it safe!      │
       │                                     │
       │ ⚠️ WARNING:                        │
       │ • We cannot recover this key       │
       │ • Anyone with this key can access  │
       │   your funds                       │
       │ • Keep it private and secure       │
       │                                     │
       │ ┌──────────────────────────────┐  │
       │ │ ●●●●●●●●●●●●●●●●●●●●●●●●●●   │  │
       │ │ [👁 Show Key]                │  │
       │ └──────────────────────────────┘  │
       │                                     │
       │ Backup Options:                    │
       │ [💾 Download as File]              │
       │ [📋 Copy to Clipboard]             │
       │ [📧 Email to Myself]               │
       │                                     │
       │ ☐ I have backed up my secret key   │
       │                                     │
       │ [← Back]    [I've Backed Up →]     │
       └────────────────────────────────────┘
       
       AFTER CHECKING BOX:
       ┌────────────────────────────────────┐
       │ ✅ Confirm Your Backup              │
       ├────────────────────────────────────┤
       │ To confirm you've saved your key,  │
       │ please enter the first 6          │
       │ characters:                         │
       │                                     │
       │ Your key: SAB3...                  │
       │                                     │
       │ ┌──────────────────────────────┐  │
       │ │ Enter: [______]              │  │
       │ └──────────────────────────────┘  │
       │                                     │
       │ [Verify]                           │
       └────────────────────────────────────┘
```

### Import Existing Wallet

```
User Has Existing Wallet → Import Flow
  │
  ├─> SELECT IMPORT METHOD
  │    ┌────────────────────────────────────┐
  │    │ 📥 Import Existing Wallet           │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │ How do you want to import?         │
  │    │                                     │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 🔑 Enter Secret Key          │  │
  │    │ │ Manually type your key       │  │
  │    │ │ [Select]                     │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 📱 Scan QR Code              │  │
  │    │ │ From another device          │  │
  │    │ │ [Select]                     │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ 📄 Upload Key File           │  │
  │    │ │ From backup file             │  │
  │    │ │ [Select]                     │  │
  │    │ └──────────────────────────────┘  │
  │    └────────────────────────────────────┘
  │
  ├─> ENTER SECRET KEY
  │    ┌────────────────────────────────────┐
  │    │ 🔑 Import with Secret Key           │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │ Enter your secret key:             │
  │    │                                     │
  │    │ ┌──────────────────────────────┐  │
  │    │ │ SAB3DEF4GHI5JKL6MNO7PQR8...  │  │
  │    │ │                               │  │
  │    │ └──────────────────────────────┘  │
  │    │                                     │
  │    │ ⚠️ Only enter your key on trusted │
  │    │    devices                         │
  │    │                                     │
  │    │ [Clear] [Paste] [Import]           │
  │    └────────────────────────────────────┘
  │
  ├─> VALIDATING KEY
  │    ┌────────────────────────────────────┐
  │    │ 🔄 Validating Wallet...             │
  │    ├────────────────────────────────────┤
  │    │                                     │
  │    │ ✓ Key format valid                 │
  │    │ ✓ Connecting to network...         │
  │    │ ⏳ Loading wallet data...           │
  │    │                                     │
  │    └────────────────────────────────────┘
  │
  └─> IMPORT SUCCESS
       ┌────────────────────────────────────┐
       │ ✅ Wallet Imported Successfully!    │
       ├────────────────────────────────────┤
       │                                     │
       │ Wallet Address: GABC123...XYZ789   │
       │ Network: Stellar Mainnet           │
       │ Balance: 1,250.00 USDC             │
       │                                     │
       │ [View Wallet →]                    │
       └────────────────────────────────────┘
```

---

## 💰 Wallet Dashboard

### Main Wallet View

```
┌─────────────────────────────────────────────────────────────────┐
│ 💼 My Wallet                              [Settings ⚙️] [+ Add] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ TOTAL BALANCE                                                    │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │                                                             │ │
│ │  $1,250.00 USD                                             │ │
│ │  ≈ 1,937,500.00 NGN                                        │ │
│ │                                                             │ │
│ │  [Refresh] Last updated: 2 seconds ago                     │ │
│ │                                                             │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ QUICK ACTIONS                                                    │
│ ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐               │
│ │   💸   │  │   📥   │  │   💳   │  │   📊   │               │
│ │  Send  │  │Receive │  │Add     │  │History │               │
│ │  Money │  │ Money  │  │Funds   │  │        │               │
│ └────────┘  └────────┘  └────────┘  └────────┘               │
│                                                                  │
│ MY ASSETS                                         [+ Add Asset]  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ 💵 USDC (USD Coin)                                         │ │
│ │    1,200.00 USDC ≈ $1,200.00                              │ │
│ │    [Send] [Receive] [Swap]                                │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ ⭐ XLM (Stellar Lumens)                                    │ │
│ │    500.00 XLM ≈ $50.00                                    │ │
│ │    [Send] [Receive] [Swap]                                │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ 🪙 Native NGN Token                                        │ │
│ │    0.00 NGN                                               │ │
│ │    [Add to Wallet]                                        │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ RECENT TRANSACTIONS                              [View All →]   │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ ↓ Received from John Doe              +100.00 USDC        │ │
│ │   Oct 6, 2025 • 3:45 PM                    ✅ Completed   │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ ↑ Sent to Mom                         -50.00 USDC         │ │
│ │   Oct 5, 2025 • 10:30 AM                   ✅ Completed   │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ ↓ Received from Acme Corp            +500.00 USDC         │ │
│ │   Oct 4, 2025 • 2:15 PM                    ✅ Completed   │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ WALLET INFO                                                      │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ Address: GABC123...XYZ789      [Copy] [QR Code] [Share]   │ │
│ │ Network: Stellar Mainnet       Status: ✅ Active           │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Multiple Wallets View

```
User with Multiple Wallets
┌──────────────────────────────────────┐
│ 💼 My Wallets                         │
├──────────────────────────────────────┤
│                                       │
│ ┌────────────────────────────────┐  │
│ │ ⭐ Primary Wallet              │  │
│ │    Stellar Mainnet             │  │
│ │    $1,250.00                   │  │
│ │    [View] [Set as Primary]     │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 💼 Business Wallet             │  │
│ │    Hedera Mainnet              │  │
│ │    $5,430.00                   │  │
│ │    [View]                      │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🧪 Test Wallet                 │  │
│ │    Stellar Testnet             │  │
│ │    100.00 Test USDC            │  │
│ │    [View]                      │  │
│ └────────────────────────────────┘  │
│                                       │
│ [+ Create New Wallet]                │
└──────────────────────────────────────┘
```

---

## 💸 Wallet Operations

### Send Money from Wallet

```
Wallet → Send Money
  │
  ├─> SELECT ASSET TO SEND
  │    ┌────────────────────────────────────┐
  │    │ 💸 Send Money                       │
  │    ├────────────────────────────────────┤
  │    │ Select asset to send:              │
  │    │                                     │
  │    │ ● 💵 USDC (1,200.00 available)     │
  │    │ ○ ⭐ XLM (500.00 available)        │
  │    │                                     │
  │    │ [Continue]                         │
  │    └────────────────────────────────────┘
  │
  ├─> ENTER RECIPIENT & AMOUNT
  │    (See remittance-sender-journey.md)
  │
  └─> COMPLETE TRANSACTION
       └─> Update wallet balance in real-time
```

### Receive Money

```
Wallet → Receive Money
┌──────────────────────────────────────┐
│ 📥 Receive Money                      │
├──────────────────────────────────────┤
│                                       │
│ Share your wallet address:           │
│                                       │
│     [Large QR Code Display]          │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ GABC123DEF456GHI789JKL012      │  │
│ │ [📋 Copy Address]              │  │
│ └────────────────────────────────┘  │
│                                       │
│ Share via:                           │
│ [📱 WhatsApp] [✉️ Email] [💬 SMS]   │
│ [🔗 Copy Link]                       │
│                                       │
│ ───────────────────────────────────  │
│                                       │
│ 💡 Request Specific Amount           │
│                                       │
│ Amount: [____] USDC                  │
│ Note: [Optional message]             │
│                                       │
│ [Generate Payment Request]           │
│                                       │
└──────────────────────────────────────┘

PAYMENT REQUEST GENERATED:
┌──────────────────────────────────────┐
│ 📄 Payment Request Created            │
├──────────────────────────────────────┤
│                                       │
│ Requesting: 100.00 USDC              │
│ From: Anyone                         │
│                                       │
│     [QR Code with amount]            │
│                                       │
│ Link: rowel.li/pay/ABC123            │
│ [Copy Link] [Share]                  │
│                                       │
│ This request expires in 24 hours     │
└──────────────────────────────────────┘
```

### Add Funds to Wallet

```
Wallet → Add Funds
┌──────────────────────────────────────┐
│ 💳 Add Funds to Wallet                │
├──────────────────────────────────────┤
│                                       │
│ How much do you want to add?         │
│                                       │
│ ┌──────────────────────────────────┐│
│ │ Amount: [1,000] USDC             ││
│ │ ≈ 1,550,000 NGN                  ││
│ └──────────────────────────────────┘│
│                                       │
│ Choose funding method:               │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 📱 Mobile Money    ⚡ Instant  │   │
│ │ M-Pesa, MTN, Airtel            │   │
│ │ Fee: 0.5%                      │   │
│ │ [Select]                       │   │
│ └──────────────────────────────┘    │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 🏦 Bank Transfer   ⏱ 1-2 days │   │
│ │ Direct bank transfer           │   │
│ │ Fee: Free                      │   │
│ │ [Select]                       │   │
│ └──────────────────────────────┘    │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 💳 Debit Card      ⚡ Instant  │   │
│ │ Visa, Mastercard               │   │
│ │ Fee: 2.5%                      │   │
│ │ [Select]                       │   │
│ └──────────────────────────────┘    │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 🪙 Crypto Deposit  ⚡ Instant  │   │
│ │ Send from another wallet       │   │
│ │ Fee: Network fee only          │   │
│ │ [Select]                       │   │
│ └──────────────────────────────┘    │
│                                       │
└──────────────────────────────────────┘

MOBILE MONEY FLOW:
┌──────────────────────────────────────┐
│ 📱 Add Funds via Mobile Money         │
├──────────────────────────────────────┤
│                                       │
│ Amount: 1,000 USDC                   │
│ You'll pay: 1,550,000 NGN + 7,750 fee│
│ Total: 1,557,750 NGN                 │
│                                       │
│ Select provider:                     │
│ ● M-Pesa (Kenya)                     │
│ ○ MTN Mobile Money                   │
│ ○ Airtel Money                       │
│                                       │
│ Phone number:                        │
│ ┌──────────────────────────────┐    │
│ │ +254 [___________]           │    │
│ └──────────────────────────────┘    │
│                                       │
│ [Continue]                           │
└──────────────────────────────────────┘

CONFIRM MOBILE MONEY:
┌──────────────────────────────────────┐
│ 📱 Confirm Mobile Money Payment       │
├──────────────────────────────────────┤
│                                       │
│ You'll receive a payment prompt      │
│ on your phone:                       │
│                                       │
│ +254 712 345 678                     │
│                                       │
│ 1. Check your phone                  │
│ 2. Enter your M-Pesa PIN             │
│ 3. Confirm payment                   │
│                                       │
│ Amount: 1,557,750 KES                │
│ To: Rowell Infrastructure            │
│                                       │
│ ⏳ Waiting for payment...             │
│    (This usually takes 30 seconds)   │
│                                       │
│ [I've Completed Payment]             │
│ [Cancel]                             │
└──────────────────────────────────────┘

SUCCESS:
┌──────────────────────────────────────┐
│ ✅ Funds Added Successfully!          │
├──────────────────────────────────────┤
│                                       │
│ 1,000 USDC has been added to        │
│ your wallet.                         │
│                                       │
│ New Balance: 2,200.00 USDC           │
│                                       │
│ [View Wallet] [Add More Funds]       │
└──────────────────────────────────────┘
```

### Withdraw Funds

```
Wallet → Withdraw
┌──────────────────────────────────────┐
│ 💰 Withdraw Funds                     │
├──────────────────────────────────────┤
│                                       │
│ How much do you want to withdraw?    │
│                                       │
│ Available: 1,200.00 USDC             │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ Amount: [500] USDC           │    │
│ │ ≈ 775,000 NGN                │    │
│ └──────────────────────────────┘    │
│                                       │
│ Withdraw to:                         │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 🏦 Bank Account   ⏱ 1-2 days  │   │
│ │ Direct to your bank           │    │
│ │ Fee: 1%                       │    │
│ │ [Select]                      │    │
│ └──────────────────────────────┘    │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 📱 Mobile Money   ⚡ Instant   │   │
│ │ M-Pesa, MTN, Airtel           │    │
│ │ Fee: 2%                       │    │
│ │ [Select]                      │    │
│ └──────────────────────────────┘    │
│                                       │
│ ┌──────────────────────────────┐    │
│ │ 🪙 Crypto Wallet  ⚡ Instant   │   │
│ │ Send to another wallet        │    │
│ │ Fee: Network fee only         │    │
│ │ [Select]                      │    │
│ └──────────────────────────────┘    │
│                                       │
└──────────────────────────────────────┘
```

### Swap Assets

```
Wallet → Swap
┌──────────────────────────────────────┐
│ 🔄 Swap Assets                        │
├──────────────────────────────────────┤
│                                       │
│ FROM                                 │
│ ┌──────────────────────────────┐    │
│ │ USDC ▼        [100.00]       │    │
│ │ Available: 1,200.00          │    │
│ └──────────────────────────────┘    │
│                                       │
│        [↓ Swap ↑]                    │
│                                       │
│ TO                                   │
│ ┌──────────────────────────────┐    │
│ │ XLM ▼         [1,000.00]     │    │
│ │ Rate: 1 USDC = 10 XLM        │    │
│ └──────────────────────────────┘    │
│                                       │
│ Exchange Details:                    │
│ ├─ Rate: 1 USDC = 10 XLM            │
│ ├─ Fee: 0.3%                        │
│ ├─ You pay: 100.00 USDC             │
│ └─ You receive: ≈ 997.00 XLM        │
│                                       │
│ ⏱ Rate locked for: 58 seconds       │
│                                       │
│ [Swap Now]                           │
└──────────────────────────────────────┘
```

---

## 📊 Transaction History

### Transaction List View

```
Wallet → Transaction History
┌──────────────────────────────────────────────────────────────┐
│ 📊 Transaction History                     [Filters ▼] [📥] │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ [All] [Sent] [Received] [Pending] [Failed]                   │
│                                                               │
│ TODAY                                                         │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ ↓ Received                              +100.00 USDC   │  │
│ │   From: John Doe                                       │  │
│ │   3:45 PM                                   ✅ Success │  │
│ │   [View Details]                                       │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ ↑ Sent                                  -25.00 USDC    │  │
│ │   To: Coffee Shop                                      │  │
│ │   1:20 PM                                   ✅ Success │  │
│ │   [View Details]                                       │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
│ YESTERDAY                                                     │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ ↑ Sent                                  -50.00 USDC    │  │
│ │   To: Mom (+254 712 345 678)                           │  │
│ │   10:30 AM                                  ✅ Success │  │
│ │   [View Details]                                       │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
│ [Load More]                                                   │
└──────────────────────────────────────────────────────────────┘
```

### Transaction Detail View

```
Transaction History → Select Transaction
┌──────────────────────────────────────┐
│ 📄 Transaction Details        [✕]    │
├──────────────────────────────────────┤
│                                       │
│ ✅ Payment Successful                │
│                                       │
│ ↑ SENT                               │
│ 50.00 USDC                           │
│                                       │
│ ───────────────────────────────────  │
│                                       │
│ TO                                   │
│ Mom (Jane Doe)                       │
│ +254 712 345 678                     │
│ GDEF456...UVW012                     │
│                                       │
│ FROM                                 │
│ Me (John Doe)                        │
│ GABC123...XYZ789                     │
│                                       │
│ ───────────────────────────────────  │
│                                       │
│ DETAILS                              │
│ ├─ Date: Oct 5, 2025                │
│ ├─ Time: 10:30:23 AM WAT            │
│ ├─ Amount: 50.00 USDC               │
│ ├─ Fee: 0.05 USDC                   │
│ ├─ Total: 50.05 USDC                │
│ ├─ Memo: "For house expenses"       │
│ ├─ Processing Time: 3 seconds       │
│ └─ Status: Completed ✅             │
│                                       │
│ BLOCKCHAIN INFO                      │
│ ├─ Network: Stellar Mainnet         │
│ ├─ Transaction ID: #RW20251005...   │
│ ├─ Hash: ABC123DEF...789            │
│ └─ [View on Explorer →]             │
│                                       │
│ [📄 Download Receipt]                │
│ [📱 Share Transaction]               │
│ [📞 Get Support]                     │
│                                       │
└──────────────────────────────────────┘
```

### Filter & Search

```
Transaction History → Filters
┌──────────────────────────────────────┐
│ 🔍 Filter Transactions                │
├──────────────────────────────────────┤
│                                       │
│ DATE RANGE                           │
│ From: [Oct 1, 2025] ▼               │
│ To:   [Oct 6, 2025] ▼               │
│                                       │
│ TYPE                                 │
│ ☑ Sent                               │
│ ☑ Received                           │
│ ☐ Swapped                            │
│ ☐ Deposits                           │
│ ☐ Withdrawals                        │
│                                       │
│ STATUS                               │
│ ☑ Success                            │
│ ☐ Pending                            │
│ ☐ Failed                             │
│                                       │
│ AMOUNT RANGE                         │
│ Min: [0] USDC                        │
│ Max: [1000] USDC                     │
│                                       │
│ ASSET                                │
│ ☑ USDC                               │
│ ☑ XLM                                │
│ ☐ All Assets                         │
│                                       │
│ [Clear Filters] [Apply Filters]      │
└──────────────────────────────────────┘

SEARCH:
┌──────────────────────────────────────┐
│ [🔍 Search transactions...]           │
│                                       │
│ Search by:                           │
│ • Recipient name                     │
│ • Transaction ID                     │
│ • Amount                             │
│ • Memo/Note                          │
└──────────────────────────────────────┘
```

### Export Transactions

```
Transaction History → Export
┌──────────────────────────────────────┐
│ 📥 Export Transactions                │
├──────────────────────────────────────┤
│                                       │
│ Export transactions for:             │
│                                       │
│ ● This Month (Oct 2025)              │
│ ○ Last 3 Months                      │
│ ○ Last 6 Months                      │
│ ○ This Year (2025)                   │
│ ○ All Time                           │
│ ○ Custom Range                       │
│                                       │
│ Format:                              │
│ ● PDF Report                         │
│ ○ CSV Spreadsheet                    │
│ ○ Excel (.xlsx)                      │
│ ○ JSON (for developers)              │
│                                       │
│ Include:                             │
│ ☑ Transaction details                │
│ ☑ Fee information                    │
│ ☑ Blockchain references              │
│ ☐ Balance snapshots                  │
│                                       │
│ [Cancel] [Export]                    │
└──────────────────────────────────────┘
```

---

## 🔐 Wallet Security

### Security Settings

```
Wallet → Settings → Security
┌──────────────────────────────────────┐
│ 🔐 Wallet Security                    │
├──────────────────────────────────────┤
│                                       │
│ AUTHENTICATION                       │
│ ┌────────────────────────────────┐  │
│ │ 🔢 PIN Code            ✅ Active│  │
│ │ 4-digit PIN for transactions   │  │
│ │ [Change PIN]                   │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 👆 Biometrics      ✅ Enabled  │  │
│ │ Use fingerprint or Face ID     │  │
│ │ [Manage]                       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 📱 2FA                ❌ Disabled│  │
│ │ Extra security for login       │  │
│ │ [Enable 2FA]                   │  │
│ └────────────────────────────────┘  │
│                                       │
│ BACKUP & RECOVERY                    │
│ ┌────────────────────────────────┐  │
│ │ 🔑 Secret Key      ✅ Backed Up │  │
│ │ Last backup: Oct 1, 2025       │  │
│ │ [View Key] [Re-backup]         │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 📧 Recovery Email  ✅ Set      │  │
│ │ john@example.com               │  │
│ │ [Change Email]                 │  │
│ └────────────────────────────────┘  │
│                                       │
│ TRANSACTION LIMITS                   │
│ ┌────────────────────────────────┐  │
│ │ Daily Limit:    $10,000        │  │
│ │ Monthly Limit:  $50,000        │  │
│ │ Current (Oct):  $1,250 (2.5%)  │  │
│ │ [Request Increase]             │  │
│ └────────────────────────────────┘  │
│                                       │
│ ACTIVITY MONITORING                  │
│ ┌────────────────────────────────┐  │
│ │ 🔔 Alert Preferences           │  │
│ │ ☑ Large transactions (>$1000)  │  │
│ │ ☑ New device login             │  │
│ │ ☑ Password changes             │  │
│ │ [Manage Alerts]                │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 📱 Active Devices: 2           │  │
│ │ • iPhone 13 (this device)      │  │
│ │ • MacBook Pro                  │  │
│ │ [Manage Devices]               │  │
│ └────────────────────────────────┘  │
│                                       │
└──────────────────────────────────────┘
```

### Device Management

```
Security → Active Devices
┌──────────────────────────────────────┐
│ 📱 Active Devices                     │
├──────────────────────────────────────┤
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 📱 iPhone 13 (This Device)     │  │
│ │ Last active: Just now           │  │
│ │ Location: Lagos, Nigeria        │  │
│ │ [Current Device]                │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 💻 MacBook Pro                 │  │
│ │ Last active: 2 hours ago        │  │
│ │ Location: Lagos, Nigeria        │  │
│ │ [Remove Device]                 │  │
│ └────────────────────────────────┘  │
│                                       │
│ ⚠️ Don't recognize a device?         │
│ [Remove All Other Devices]           │
│                                       │
└──────────────────────────────────────┘
```

---

## 🌟 Advanced Wallet Features

### Multi-Wallet Management

```
Wallet → Add Wallet
┌──────────────────────────────────────┐
│ ➕ Create New Wallet                  │
├──────────────────────────────────────┤
│                                       │
│ What type of wallet?                 │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 💼 Business Wallet             │  │
│ │ Separate for business use       │  │
│ │ [Create]                       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 👨‍👩‍👧‍👦 Family Wallet        │  │
│ │ Shared with family members      │  │
│ │ [Create]                       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 💰 Savings Wallet              │  │
│ │ For long-term savings           │  │
│ │ [Create]                       │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 🧪 Test Wallet                 │  │
│ │ For testing and development     │  │
│ │ [Create]                       │  │
│ └────────────────────────────────┘  │
│                                       │
└──────────────────────────────────────┘
```

### Wallet Contacts

```
Wallet → Contacts
┌──────────────────────────────────────┐
│ 📇 My Contacts                        │
├──────────────────────────────────────┤
│                                       │
│ [🔍 Search contacts...]               │
│                                       │
│ FAVORITES (⭐)                        │
│ ┌────────────────────────────────┐  │
│ │ 👤 Mom                         │  │
│ │    +254 712 345 678 🇰🇪        │  │
│ │    Last sent: Yesterday         │  │
│ │    [Send] [Request] [More...]  │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ 👤 Brother                     │  │
│ │    GDEF456...UVW012             │  │
│ │    Last sent: Last week         │  │
│ │    [Send] [Request] [More...]  │  │
│ └────────────────────────────────┘  │
│                                       │
│ ALL CONTACTS (A-Z)                   │
│ A                                     │
│ ┌────────────────────────────────┐  │
│ │ 👤 Alice Johnson               │  │
│ │    GABC...789                   │  │
│ └────────────────────────────────┘  │
│                                       │
│ B                                     │
│ ┌────────────────────────────────┐  │
│ │ 🏪 Bob's Coffee Shop           │  │
│ │    GBOB...456                   │  │
│ └────────────────────────────────┘  │
│                                       │
│ [+ Add New Contact]                  │
└──────────────────────────────────────┘
```

### Recurring Payments

```
Wallet → Recurring Payments
┌──────────────────────────────────────┐
│ 📅 Recurring Payments                 │
├──────────────────────────────────────┤
│                                       │
│ ACTIVE                               │
│ ┌────────────────────────────────┐  │
│ │ Monthly to Mom                 │  │
│ │ 50.00 USDC every 1st of month  │  │
│ │ Next payment: Nov 1, 2025      │  │
│ │ [Edit] [Pause] [Cancel]        │  │
│ └────────────────────────────────┘  │
│                                       │
│ ┌────────────────────────────────┐  │
│ │ Weekly to Brother              │  │
│ │ 20.00 USDC every Monday        │  │
│ │ Next payment: Oct 13, 2025     │  │
│ │ [Edit] [Pause] [Cancel]        │  │
│ └────────────────────────────────┘  │
│                                       │
│ PAUSED                               │
│ ┌────────────────────────────────┐  │
│ │ Monthly Savings                │  │
│ │ 100.00 USDC (Paused)           │  │
│ │ [Resume] [Edit] [Delete]       │  │
│ └────────────────────────────────┘  │
│                                       │
│ [+ New Recurring Payment]            │
└──────────────────────────────────────┘

CREATE RECURRING PAYMENT:
┌──────────────────────────────────────┐
│ ➕ New Recurring Payment              │
├──────────────────────────────────────┤
│                                       │
│ To: [Select recipient] ▼             │
│                                       │
│ Amount: [____] USDC                  │
│                                       │
│ Frequency:                           │
│ ● Daily                              │
│ ○ Weekly (on Monday ▼)               │
│ ○ Monthly (on 1st ▼)                 │
│ ○ Custom                             │
│                                       │
│ Start date: [Oct 7, 2025] ▼         │
│                                       │
│ End: ○ Never  ● After [12] payments  │
│                                       │
│ [Cancel] [Create Payment]            │
└──────────────────────────────────────┘
```

---

## 📱 Mobile-Specific Features

### Widgets

```
HOME SCREEN WIDGET:
┌────────────────────────────────┐
│ Rowell Wallet                  │
├────────────────────────────────┤
│ Balance: $1,250.00             │
│                                 │
│ [Send] [Receive]               │
└────────────────────────────────┘

LOCK SCREEN WIDGET:
┌────────────────────────────────┐
│ 💼 Rowell                       │
│ $1,250.00                      │
│ ↑ $50 sent to Mom              │
└────────────────────────────────┘
```

### Quick Actions (3D Touch / Long Press)

```
Long Press App Icon →
┌────────────────────────────────┐
│ ⚡ Quick Actions                │
├────────────────────────────────┤
│ 💸 Send Money                  │
│ 📥 Receive Money               │
│ 📊 View Balance                │
│ 📇 Send to Mom                 │
└────────────────────────────────┘
```

### Apple Pay / Google Pay Integration

```
Add Rowell Card to Apple Pay
┌──────────────────────────────────────┐
│ 🍎 Add to Apple Pay                   │
├──────────────────────────────────────┤
│                                       │
│ Use your Rowell wallet with           │
│ Apple Pay for easy payments.          │
│                                       │
│ [Rowell Virtual Card]                │
│ Balance: $1,250.00                   │
│                                       │
│ Benefits:                            │
│ ✓ Pay at millions of stores          │
│ ✓ Use online and in apps             │
│ ✓ Secure with Face ID                │
│                                       │
│ [Add to Apple Wallet]                │
└──────────────────────────────────────┘
```

---

## 📊 Analytics & Insights

### Spending Analysis

```
Wallet → Analytics
┌──────────────────────────────────────┐
│ 📊 Spending Insights                  │
├──────────────────────────────────────┤
│                                       │
│ THIS MONTH (October 2025)            │
│                                       │
│ Total Spent:    $250.00 ↓ 15%       │
│ Total Received: $600.00 ↑ 25%       │
│ Net Change:     +$350.00             │
│                                       │
│ SPENDING BY CATEGORY                 │
│ ┌────────────────────────────────┐  │
│ │ 🏠 Family Support    60% $150  │  │
│ │ ☕ Merchants         30% $75   │  │
│ │ 🎓 Education         10% $25   │  │
│ └────────────────────────────────┘  │
│                                       │
│ TOP RECIPIENTS                       │
│ 1. Mom                  $150         │
│ 2. Coffee Shop          $50          │
│ 3. Brother              $25          │
│                                       │
│ COMPARISON                           │
│ vs Last Month:  ↓ 15% less spending │
│ Average per day: $8.33               │
│                                       │
│ [View Detailed Report →]            │
└──────────────────────────────────────┘
```

### Balance History

```
Wallet → Balance History
┌──────────────────────────────────────┐
│ 📈 Balance Over Time                  │
├──────────────────────────────────────┤
│                                       │
│ [Chart showing balance trends]       │
│                                       │
│ $1,250 ─────────┐                    │
│              ┌──┘                     │
│        ┌─────┘                        │
│ $500 ──┘                             │
│                                       │
│ Sep     Sep     Oct     Oct          │
│  15      30      15     (Now)        │
│                                       │
│ STATISTICS                           │
│ ├─ Peak Balance: $1,350 (Oct 3)     │
│ ├─ Lowest: $485 (Sep 15)            │
│ ├─ Average: $892                     │
│ └─ Growth: +158% (30 days)          │
│                                       │
│ [Export Data] [Share]                │
└──────────────────────────────────────┘
```

---

## 🆘 Help & Support

### In-Wallet Help

```
Wallet → Help
┌──────────────────────────────────────┐
│ 💬 How can we help?                   │
├──────────────────────────────────────┤
│                                       │
│ [🔍 Search help articles...]          │
│                                       │
│ POPULAR TOPICS                       │
│ • How do I send money?               │
│ • How do I add funds?                │
│ • What are the fees?                 │
│ • How do I secure my wallet?         │
│ • What if I lose my phone?           │
│                                       │
│ QUICK ACTIONS                        │
│ [💬 Chat with Support]               │
│ [📧 Email Us]                        │
│ [📞 Call Us]                         │
│ [📚 View Tutorials]                  │
│                                       │
│ WALLET STATUS                        │
│ All systems operational ✅           │
│ Last updated: 2 min ago              │
│                                       │
└──────────────────────────────────────┘
```

---

## ✅ Wallet UX Checklist

### Design Principles

```
☑ SECURITY FIRST
├─ Clear security indicators
├─ Biometric authentication
├─ Encrypted backups
└─ Activity monitoring

☑ SIMPLICITY
├─ Minimal steps to transact
├─ Clear visual hierarchy
├─ Progressive disclosure
└─ Contextual help

☑ TRANSPARENCY
├─ Real-time balance updates
├─ Clear fee disclosure
├─ Transaction status visibility
└─ Network information

☑ ACCESSIBILITY
├─ High contrast mode
├─ Screen reader support
├─ Large touch targets
└─ Simple language

☑ PERFORMANCE
├─ < 2s page load
├─ Instant balance refresh
├─ Smooth animations
└─ Offline viewing

☑ TRUST
├─ Professional design
├─ Consistent branding
├─ Clear error messages
└─ Responsive support
```

---

## 📚 Related Documentation

- [Overview User Flows](overview.md)
- [Remittance Sender Journey](remittance-sender-journey.md)
- [Persona Interaction Flows](persona-interaction-flows.md)
- [Security Best Practices](../guides/security.md)
- [Technical Implementation](../api/README.md)

---

**Document Version:** 1.0  
**Last Updated:** October 6, 2025  
**Author:** UX Team - Rowell Infrastructure  
**Status:** ✅ Ready for Implementation

---

*Built with ❤️ for Africa by the Rowell Infrastructure Team* 🌍💚

