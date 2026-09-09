# 🛡️ SecureShop — High-Assurance E-Commerce Platform

**SecureShop** is a full-stack e-commerce web application specializing in cybersecurity hardware (FIDO2 security keys, hardware-encrypted SSDs, air-gapped cold wallets, and Faraday shielding gear). It implements defense-in-depth security principles throughout its frontend, backend, and data persistence layers.

---

## ✨ Features

### 🛒 Customer & E-Commerce Flow
- **Authentication Gate**: Zero-trust product catalog access requiring login before browsing hardware, product details, or cart.
- **Product Catalog & Categorization**: Browse hardware by categories (*Hardware Security*, *Encrypted Storage*, *Network Defense*, *Privacy Defense*).
- **Search & Filtering**: Real-time filtering by category, search queries, and dynamic price/rating/newest sorting.
- **Detailed Specifications**: Technical cryptographic profiles (EAL6+ ratings, tamper-detection mechanics, zero-telemetry certification).
- **Realistic Hardware Visuals**: Clean vector hardware illustrations for all physical security devices on modern light cards.
- **AJAX Shopping Cart**: Seamless item additions with live navbar counter badges, quantity modifications, and item removal.
- **Promotional Coupons**: Integrated discount system (e.g. `SECURE20` for 20% off, `FREESHIP` for zero shipping).
- **Encrypted Checkout**: Multi-step checkout with stealth shipping destination and payment options (PCI-DSS tokenized card simulation or zero-knowledge cryptocurrency settlement).
- **Cryptographic Receipts & Order History**: Printable confirmation receipts with unique order tracking numbers (`SEC-XXXXXXXX`, `TRK-XXXXXXXXXX`).

### 🔐 Defensive Security & Authentication Features
- **Multi-Factor Authentication (MFA / 2FA)**: RFC 6238 compliant TOTP verification with QR codes, authenticator app sync (Google Authenticator, Microsoft Authenticator, 1Password), one-time emergency backup recovery codes, and live demo OTP helper.
- **Anti-CSRF Tokens**: Synchronizer token pattern enforced on all state-changing endpoints (`POST`, `PUT`, `DELETE`, `PATCH`) with dual HTTP form and `X-CSRF-Token` header support.
- **Secure Authentication & Password Policy**: High-entropy PBKDF2 salted hashing with minimum length, letter, number, and special character requirements.
- **Brute-Force Protection**: 5-attempt rate-limiting with automated 15-minute temporary account lockouts.
- **SQL Injection Prevention**: 100% parameterized queries via SQLite3.
- **Security Headers**: Standard defense-in-depth HTTP headers (`Content-Security-Policy`, `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `X-XSS-Protection: 1; mode=block`).
- **Comprehensive Audit Logging**: Event forensics logging (logins, failed attempts, account lockouts, CSRF blocks, order placements, catalog changes).

### 🛠️ Administrator Console
- **Executive Metrics**: Live sales revenue, total order count, active catalog SKUs, and low-stock alerts.
- **Catalog Management**: Add, update, and remove products with instant image preview and stock counters.
- **Order Dispatch**: Real-time fulfillment pipeline (Processing, Shipped, Delivered, Cancelled) and tracking number assignment.
- **Security Log Viewer**: Real-time inspection of forensic audit records with client IP, user agent, and event categorization.

---

## 🚀 Quick Start

### 1. Requirements & Dependencies
Ensure Python 3.9+ is installed. Install Flask (if not already installed):
```bash
pip install -r requirements.txt
```

### 2. Launching SecureShop
Run the Flask server:
```bash
python app.py
```
Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Demo Credentials

For convenience, the login page provides **One-Click Demo Autofill** buttons:

| Role | Username / Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@secureshop.io` | `Admin@123456!` | Full Admin Console (`/admin`), Inventory, Orders, Audit Logs |
| **Customer** | `user@secureshop.io` | `Customer@123456!` | Storefront browsing, Cart, Checkout, Order History |

### Available Promotional Codes:
- `SECURE20`: 20% discount on entire cart.
- `CYBER10`: 10% discount on entire cart.
- `FREESHIP`: 100% free stealth shipping.

---

## 🧪 Running Automated Tests

A test suite covers the complete application flow:
```bash
python -m unittest test_secureshop.py -v
```
All 10 automated test suites verify:
- Unauthenticated access redirects and login gate enforcement
- Security HTTP headers & Content Security Policy
- Catalog search, category filters, and product details
- CSRF blocking and synchronizer token validation
- Dynamic cart modifications, coupon discounts, and order placement
- User registration, password policy verification, and customer/admin authentication
- Brute-force account lockout enforcement
- Full Multi-Factor Authentication (MFA / 2FA) TOTP validation, backup codes, and resend
