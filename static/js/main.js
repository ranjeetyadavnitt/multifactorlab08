// SecureShop - Interactive UI & Client Logic

document.addEventListener('DOMContentLoaded', () => {
    initToastContainer();
    initAddToCartButtons();
    initDemoLoginButtons();
    initPasswordStrength();
    initCardFormatter();
    initMfaInputs();
    initMfaTimer();
    initKeyboardShortcuts();
    initUserMenu();
});

// Toast notification system
function initToastContainer() {
    if (!document.getElementById('toastContainer')) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer') || document.body;
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    let icon = '<i class="fas fa-check-circle" style="color: var(--primary);"></i>';
    if (type === 'error') {
        toast.style.borderLeftColor = '#ef4444';
        icon = '<i class="fas fa-exclamation-triangle" style="color: #ef4444;"></i>';
    } else if (type === 'info') {
        toast.style.borderLeftColor = '#06b6d4';
        icon = '<i class="fas fa-info-circle" style="color: #06b6d4;"></i>';
    }

    toast.innerHTML = `
        ${icon}
        <span style="flex: 1;">${escapeHTML(message)}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function escapeHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    const input = document.querySelector('input[name="csrf_token"]');
    if (input) return input.value;
    return '';
}

// Copy promo code from topbar
function copyPromoCode(code, btn) {
    navigator.clipboard.writeText(code).then(() => {
        const span = btn.querySelector('span');
        const orig = span ? span.textContent : btn.innerHTML;
        if (span) span.textContent = 'Copied!';
        showToast(`Promo code '${code}' copied to clipboard!`, 'info');
        setTimeout(() => {
            if (span) span.textContent = orig;
        }, 2000);
    });
}

// Global Keyboard Shortcuts (Ctrl+K or / to search)
function initKeyboardShortcuts() {
    const searchInput = document.getElementById('globalSearchInput');
    if (!searchInput) return;

    window.addEventListener('keydown', (e) => {
        const isInput = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName);
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        } else if (e.key === '/' && !isInput) {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
    });
}

// Add to Bag buttons with spring feedback
function initAddToCartButtons() {
    document.querySelectorAll('.btn-add-cart').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const productId = button.dataset.productId;
            const quantityInput = document.getElementById(`qty-${productId}`);
            const quantity = quantityInput ? parseInt(quantityInput.value, 10) : 1;

            button.disabled = true;
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';

            try {
                const response = await fetch('/api/cart/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': getCsrfToken()
                    },
                    body: JSON.stringify({ product_id: productId, quantity: quantity })
                });

                const data = await response.json();
                if (response.ok && data.success) {
                    showToast(data.message || 'Added to bag!', 'success');
                    updateCartBadge(data.cart_count);
                } else {
                    showToast(data.message || 'Failed to add item', 'error');
                }
            } catch (err) {
                console.error(err);
                showToast('Network error while adding to bag.', 'error');
            } finally {
                button.disabled = false;
                button.innerHTML = originalHTML;
            }
        });
    });
}

function updateCartBadge(count) {
    const badge = document.getElementById('navCartBadge') || document.querySelector('.cart-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.transform = 'scale(1.4)';
        badge.style.transition = 'transform 0.2s cubic-bezier(0.16, 1, 0.3, 1)';
        setTimeout(() => {
            badge.style.transform = 'scale(1)';
        }, 250);
    }
}

// Cart Quantity Updaters
async function updateCartQty(cartId, delta) {
    const valElem = document.getElementById(`cart-qty-${cartId}`);
    if (!valElem) return;
    let currentQty = parseInt(valElem.textContent, 10);
    let newQty = currentQty + delta;

    if (newQty < 1) {
        if (!confirm('Remove this item from your cart?')) return;
        newQty = 0;
    }

    try {
        const response = await fetch('/api/cart/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': getCsrfToken()
            },
            body: JSON.stringify({ cart_id: cartId, quantity: newQty })
        });

        const data = await response.json();
        if (response.ok && data.success) {
            window.location.reload();
        } else {
            showToast(data.message || 'Could not update item.', 'error');
        }
    } catch (e) {
        showToast('Error updating cart', 'error');
    }
}

async function removeCartItem(cartId) {
    if (!confirm('Are you sure you want to remove this item?')) return;

    try {
        const response = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': getCsrfToken()
            },
            body: JSON.stringify({ cart_id: cartId })
        });

        const data = await response.json();
        if (response.ok && data.success) {
            window.location.reload();
        } else {
            showToast(data.message || 'Could not remove item.', 'error');
        }
    } catch (e) {
        showToast('Error removing item from cart', 'error');
    }
}

// Apply Coupon Code
async function applyCoupon() {
    const input = document.getElementById('couponCodeInput');
    if (!input || !input.value.trim()) {
        showToast('Please enter a coupon code.', 'error');
        return;
    }

    try {
        const response = await fetch('/api/cart/apply-coupon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': getCsrfToken()
            },
            body: JSON.stringify({ code: input.value.trim() })
        });

        const data = await response.json();
        if (response.ok && data.success) {
            showToast(data.message || 'Coupon applied!', 'success');
            setTimeout(() => window.location.reload(), 600);
        } else {
            showToast(data.message || 'Invalid coupon code.', 'error');
        }
    } catch (e) {
        showToast('Error applying coupon', 'error');
    }
}

// Demo Login Auto-fill Helper
function initDemoLoginButtons() {
    const fillAdminBtn = document.getElementById('btnFillAdmin');
    const fillCustomerBtn = document.getElementById('btnFillCustomer');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    if (fillAdminBtn && usernameInput && passwordInput) {
        fillAdminBtn.addEventListener('click', () => {
            usernameInput.value = 'admin@secureshop.io';
            passwordInput.value = 'Admin@123456!';
            showToast('Filled demo Admin credentials. Click Continue!', 'info');
        });
    }

    if (fillCustomerBtn && usernameInput && passwordInput) {
        fillCustomerBtn.addEventListener('click', () => {
            usernameInput.value = 'user@secureshop.io';
            passwordInput.value = 'Customer@123456!';
            showToast('Filled demo Customer credentials. Click Continue!', 'info');
        });
    }
}

// Multi-Factor Authentication (MFA / 2FA) Interactive Inputs
function initMfaInputs() {
    const container = document.getElementById('otpBoxContainer');
    if (!container) return;

    const boxes = Array.from(container.querySelectorAll('.otp-box'));
    const hiddenInput = document.getElementById('hiddenFullCode');
    const mfaForm = document.getElementById('mfaForm');
    const autofillBtn = document.getElementById('btnAutofillCode');
    const sampleDisplay = document.getElementById('sampleOtpDisplay');

    function syncHiddenCode() {
        const code = boxes.map(b => b.value.trim()).join('');
        if (hiddenInput) hiddenInput.value = code;
        return code;
    }

    boxes.forEach((box, idx) => {
        box.addEventListener('input', (e) => {
            const val = box.value.replace(/\D/g, '');
            box.value = val ? val.slice(-1) : '';

            if (box.value && idx < boxes.length - 1) {
                boxes[idx + 1].focus();
                boxes[idx + 1].select();
            }

            const fullCode = syncHiddenCode();
            if (fullCode.length === 6 && mfaForm) {
                // Auto submit when all 6 digits entered
                setTimeout(() => mfaForm.submit(), 200);
            }
        });

        box.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace') {
                if (!box.value && idx > 0) {
                    boxes[idx - 1].focus();
                    boxes[idx - 1].value = '';
                    syncHiddenCode();
                }
            } else if (e.key === 'ArrowLeft' && idx > 0) {
                boxes[idx - 1].focus();
            } else if (e.key === 'ArrowRight' && idx < boxes.length - 1) {
                boxes[idx + 1].focus();
            }
        });

        box.addEventListener('paste', (e) => {
            e.preventDefault();
            const text = (e.clipboardData || window.clipboardData).getData('text');
            const clean = text.replace(/\D/g, '').slice(0, 6);
            if (!clean) return;

            clean.split('').forEach((char, i) => {
                if (boxes[i]) boxes[i].value = char;
            });

            syncHiddenCode();
            const focusIdx = Math.min(clean.length, boxes.length - 1);
            boxes[focusIdx].focus();

            if (clean.length === 6 && mfaForm) {
                setTimeout(() => mfaForm.submit(), 200);
            }
        });
    });

    if (autofillBtn && sampleDisplay) {
        autofillBtn.addEventListener('click', () => {
            const code = sampleDisplay.textContent.trim().replace(/\D/g, '').slice(0, 6);
            if (code.length === 6) {
                code.split('').forEach((digit, i) => {
                    if (boxes[i]) boxes[i].value = digit;
                });
                syncHiddenCode();
                showToast(`Filled passcode: ${code}. Verifying...`, 'success');
                if (mfaForm) {
                    setTimeout(() => mfaForm.submit(), 300);
                }
            }
        });
    }

    if (mfaForm) {
        mfaForm.addEventListener('submit', () => {
            syncHiddenCode();
        });
    }
}

// Live Countdown Timer for 2FA Passcode
function initMfaTimer() {
    const timerElem = document.getElementById('mfaCountdown');
    if (!timerElem) return;

    let seconds = parseInt(timerElem.dataset.seconds, 10);
    if (isNaN(seconds) || seconds <= 0) return;

    const interval = setInterval(() => {
        seconds--;
        if (seconds <= 0) {
            clearInterval(interval);
            timerElem.textContent = 'Expired';
            timerElem.style.color = '#ef4444';
        } else {
            const m = Math.floor(seconds / 60).toString().padStart(2, '0');
            const s = (seconds % 60).toString().padStart(2, '0');
            timerElem.textContent = `${m}:${s}`;
        }
    }, 1000);
}

// User Profile Menu Click Outside Handler
function initUserMenu() {
    const trigger = document.getElementById('userMenuBtn');
    const menu = document.getElementById('userDropdownMenu');
    if (!trigger || !menu) return;

    trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = menu.style.display === 'block';
        menu.style.display = isOpen ? 'none' : 'block';
    });

    document.addEventListener('click', () => {
        menu.style.display = '';
    });
}

// Password Strength Meter
function initPasswordStrength() {
    const passInput = document.getElementById('regPassword');
    const meterBar = document.getElementById('passwordMeterBar');
    const meterText = document.getElementById('passwordMeterText');

    if (!passInput || !meterBar) return;

    passInput.addEventListener('input', () => {
        const val = passInput.value;
        let score = 0;
        if (val.length >= 8) score += 25;
        if (/[A-Z]/.test(val)) score += 25;
        if (/[0-9]/.test(val)) score += 25;
        if (/[\W_]/.test(val)) score += 25;

        meterBar.style.width = score + '%';
        if (score <= 25) {
            meterBar.style.backgroundColor = '#ef4444';
            if (meterText) {
                meterText.textContent = 'Weak';
                meterText.style.color = '#ef4444';
            }
        } else if (score <= 50) {
            meterBar.style.backgroundColor = '#f59e0b';
            if (meterText) {
                meterText.textContent = 'Fair';
                meterText.style.color = '#f59e0b';
            }
        } else if (score <= 75) {
            meterBar.style.backgroundColor = '#06b6d4';
            if (meterText) {
                meterText.textContent = 'Good';
                meterText.style.color = '#06b6d4';
            }
        } else {
            meterBar.style.backgroundColor = '#10b981';
            if (meterText) {
                meterText.textContent = 'Strong & Secure';
                meterText.style.color = '#10b981';
            }
        }
    });
}

// Simulated Credit Card Formatter
function initCardFormatter() {
    const cardInput = document.getElementById('cardNumber');
    const expInput = document.getElementById('cardExpiry');
    const cvvInput = document.getElementById('cardCvv');

    if (cardInput) {
        cardInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '').substring(0, 16);
            let formatted = val.match(/.{1,4}/g)?.join(' ') || val;
            e.target.value = formatted;
        });
    }

    if (expInput) {
        expInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '').substring(0, 4);
            if (val.length >= 2) {
                e.target.value = val.substring(0, 2) + '/' + val.substring(2);
            } else {
                e.target.value = val;
            }
        });
    }

    if (cvvInput) {
        cvvInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '').substring(0, 4);
        });
    }
}
