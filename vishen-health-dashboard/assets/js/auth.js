/**
 * Password Protection for Vishen's Health Dashboard
 * Password: vibrant
 */

(function() {
    'use strict';

    const CORRECT_PASSWORD = 'vibrant';
    const AUTH_KEY = 'vishen_health_auth';
    const AUTH_EXPIRY_KEY = 'vishen_health_auth_expiry';
    const SESSION_DURATION = 24 * 60 * 60 * 1000; // 24 hours

    function checkAuth() {
        const authToken = sessionStorage.getItem(AUTH_KEY);
        const expiry = sessionStorage.getItem(AUTH_EXPIRY_KEY);

        if (authToken === 'authenticated' && expiry && Date.now() < parseInt(expiry)) {
            return true;
        }

        return false;
    }

    function setAuth() {
        sessionStorage.setItem(AUTH_KEY, 'authenticated');
        sessionStorage.setItem(AUTH_EXPIRY_KEY, (Date.now() + SESSION_DURATION).toString());
    }

    function clearAuth() {
        sessionStorage.removeItem(AUTH_KEY);
        sessionStorage.removeItem(AUTH_EXPIRY_KEY);
    }

    function showLoginModal() {
        // Create modal overlay
        const overlay = document.createElement('div');
        overlay.id = 'auth-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            animation: fadeIn 0.3s ease;
        `;

        // Create login box
        const loginBox = document.createElement('div');
        loginBox.style.cssText = `
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 400px;
            width: 90%;
            text-align: center;
            animation: slideUp 0.4s ease;
        `;

        loginBox.innerHTML = `
            <div style="margin-bottom: 24px;">
                <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; font-size: 32px;">
                    🔒
                </div>
                <h2 style="color: #1A1A1A; font-size: 24px; margin-bottom: 8px; font-weight: 600;">Protected Health Dashboard</h2>
                <p style="color: #6B7280; font-size: 14px; margin: 0;">Enter password to access your personal health data</p>
            </div>

            <form id="auth-form" style="margin-bottom: 16px;">
                <input
                    type="password"
                    id="password-input"
                    placeholder="Enter password"
                    autocomplete="off"
                    style="
                        width: 100%;
                        padding: 12px 16px;
                        border: 2px solid #E5E7EB;
                        border-radius: 8px;
                        font-size: 16px;
                        margin-bottom: 16px;
                        box-sizing: border-box;
                        transition: border-color 0.2s;
                    "
                />
                <button
                    type="submit"
                    style="
                        width: 100%;
                        padding: 12px 24px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 16px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: transform 0.2s, box-shadow 0.2s;
                    "
                    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px rgba(102,126,234,0.4)'"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'"
                >
                    Unlock Dashboard
                </button>
            </form>

            <div id="error-message" style="color: #EF4444; font-size: 14px; display: none; margin-top: 12px;">
                ❌ Incorrect password. Please try again.
            </div>

            <p style="color: #9CA3AF; font-size: 12px; margin-top: 20px;">
                Your session will remain active for 24 hours
            </p>
        `;

        overlay.appendChild(loginBox);
        document.body.appendChild(overlay);

        // Add animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            #password-input:focus {
                outline: none;
                border-color: #667eea;
            }
        `;
        document.head.appendChild(style);

        // Focus password input
        setTimeout(() => {
            document.getElementById('password-input').focus();
        }, 100);

        // Handle form submission
        document.getElementById('auth-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const password = document.getElementById('password-input').value;
            const errorMsg = document.getElementById('error-message');

            if (password === CORRECT_PASSWORD) {
                setAuth();
                overlay.style.animation = 'fadeIn 0.3s ease reverse';
                setTimeout(() => {
                    overlay.remove();
                }, 300);
            } else {
                errorMsg.style.display = 'block';
                document.getElementById('password-input').value = '';
                document.getElementById('password-input').focus();

                // Shake animation
                loginBox.style.animation = 'shake 0.4s ease';
                setTimeout(() => {
                    loginBox.style.animation = 'slideUp 0.4s ease';
                }, 400);
            }
        });

        // Add shake animation
        const shakeStyle = document.createElement('style');
        shakeStyle.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
        `;
        document.head.appendChild(shakeStyle);
    }

    // Check authentication on page load
    if (!checkAuth()) {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', showLoginModal);
        } else {
            showLoginModal();
        }
    }

    // Add logout functionality
    window.logout = function() {
        clearAuth();
        window.location.reload();
    };

})();
