// API Handler
class API {
    constructor() {
        this.baseURL = 'http://0.0.0.0:8000'; // Change this to your backend URL
    }

    // Get authorization header
    getAuthHeader() {
        const token = auth.getCookie('access_token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    // Generic API call
 // Generic API call
    async call(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...this.getAuthHeader(),
                ...options.headers
            }
        };

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                headers: defaultOptions.headers
            });

            // Handle token expiration
            if (response.status === 401) {
                auth.logout();
                return { success: false, message: "Session expired" };
            }

            const responseData = await response.json();

            // FIX: Don't wrap it. 
            // If the backend sends { success: true, data: ... }, we return exactly that.
            
            if (!response.ok) {
                // If backend sent an error message, use it.
                // We normalize it to always return { success: false, message: ... }
                throw new Error(responseData.message || responseData.detail || 'Request failed');
            }

            // If the backend forgot to send "success", we assume true if HTTP was 200
            if (responseData.success === undefined) {
                responseData.success = true; 
            }

            return responseData;

        } catch (error) {
            console.error('API Error:', error);
            // Ensure frontend always gets a consistent error format
            return { success: false, message: error.message };
        }
    }

    // User APIs
        async getWeather() {
        return await this.call('/user/weather');
    }

    async getUserProfile() {
        return await this.call('/user/profile/');
    }

    async updatePersonal(data) {
        return await this.call('/user/personal/', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async updateResident(data) {
        return await this.call('/user/resident/', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async addVehicle(data) {
        return await this.call('/user/vehicle/add/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async deleteVehicle(data) {
        return await this.call('/user/vehicle/remove/', {
            method: 'DELETE',
            body: JSON.stringify(data)
        });
    }


    async getNotices() {
        return await this.call('/user/notice');
    }

    // Support APIs
    async getTicketsStatus() {
        return await this.call('/user/support/status/');
    }

    async submitComplaint(data) {
        return await this.call('/user/support/complaint', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getComplaint(ticketId) {
        return await this.call(`/user/support/complaint?ticket_id=${ticketId}`);
    }

    async submitEpass(data) {
        return await this.call('/user/support/epass', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getEpass(ticketId) {
        return await this.call(`/user/support/epass?ticket_id=${ticketId}`);
    }

    // Admin APIs
    async getAdminDashboard() {
        return await this.call('/admin/');
    }
    async getUsersActivity(){
        return await this.call('/admin/users/logs')
    }

    async updateComplaint(ticketId, data) {
        return await this.call(`/admin/complaint/action?ticket_id=${ticketId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async updateEpass(ticketId, data) {
        return await this.call(`/admin/epass/action?ticket_id=${ticketId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async postNotice(data) {
        return await this.call('/admin/notice', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getAdminNotices() {
        return await this.call('/admin/notice');
    }

    async getUsers() {
        return await this.call('/admin/users');
    }

    async getUserProfileforadmin(userId) {
        return await this.call(`/admin/user/?user_id=${userId}`);
    }

    // QR Verification
    async verifyToken(tokenId) {
        return await this.call(`/verify/?token_id=${tokenId}`);
    }
}

// Initialize API instance
const api = new API();