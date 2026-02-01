// Authentication Handler
const auth = {
    BASE_URL: 'http://localhost:8000',

    // ─── Cookie Helpers ───────────────────────────────────────────
    getCookie(name) {
        const match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
        return match ? decodeURIComponent(match[1]) : null;
    },

    setCookie(name, value, days = 7) {
        const expires = new Date(Date.now() + days * 86400000).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
    },

    clearCookie(name) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
    },

    // ─── Token / State ────────────────────────────────────────────
    getToken() {
        return this.getCookie('access_token');
    },

    getRole() {
        return this.getCookie('user_role'); // "USER" or "ADMIN"
    },

    getUserId() {
        return this.getCookie('user_id');
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    // ─── Login ────────────────────────────────────────────────────
    async login(userId, password) {
        try {
            const response = await fetch(`${this.BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, password: password })
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || data.message || 'Login failed' };
            }

            // Store token & meta in cookies
            if (data.access_token) this.setCookie('access_token', data.access_token);
            if (data.role)         this.setCookie('user_role', data.role);
            if (data.user_id)      this.setCookie('user_id', data.user_id);

            return { success: true, data };
        } catch (err) {
            console.error('Login error:', err);
            return { success: false, error: 'Network error. Please try again.' };
        }
    },

    // ─── Register ─────────────────────────────────────────────────
    async registerUser(userData) {
        try {
            const response = await fetch(`${this.BASE_URL}/auth/register/user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || data.message || 'Registration failed' };
            }

            return { success: true, data };
        } catch (err) {
            console.error('Register error:', err);
            return { success: false, error: 'Network error. Please try again.' };
        }
    },

    async registerAdmin(adminData) {
        try {
            const response = await fetch(`${this.BASE_URL}/auth/register/admin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(adminData)
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || data.message || 'Registration failed' };
            }

            return { success: true, data };
        } catch (err) {
            console.error('Register error:', err);
            return { success: false, error: 'Network error. Please try again.' };
        }
    },

    // ─── Logout ───────────────────────────────────────────────────
    logout() {
        this.clearCookie('access_token');
        this.clearCookie('user_role');
        this.clearCookie('user_id');
        window.location.href = '/index.html';
    },

    // ─── Route Guards ─────────────────────────────────────────────
    /**
     * Call at top of every protected page.
     * @param {string[]} allowedRoles  e.g. ['USER'] or ['ADMIN']
     * If token missing or role not allowed → redirects to login.
     */
    requireAuth(allowedRoles = []) {
        if (!this.isAuthenticated()) {
            window.location.href = '/index.html';
            return;
        }

        const role = this.getRole();
        if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
            // Wrong role → send to their own home
            this.redirectToHome();
        }
    },

    // ─── Smart Redirect ───────────────────────────────────────────
    redirectToHome() {
        const role = this.getRole();
        if (role === 'ADMIN') {
            window.location.href = '/admin/dashboard.html';
        } else {
            window.location.href = '/user/dashboard.html';
        }
    }
};