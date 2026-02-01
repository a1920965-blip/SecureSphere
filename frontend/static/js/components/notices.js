// ─── Reusable Notice Renderer ─────────────────────────────────────────────
// Usage:  renderNoticeList(containerElementOrId, noticesArray)
//
// Each notice object expected shape:  { Type, Body | body }
// Renders styled cards matching the blue-left-border design used site-wide.

function renderNoticeList(container, notices) {
    // Accept either a DOM element or a string ID
    const el = typeof container === 'string'
        ? document.getElementById(container)
        : container;

    if (!el) return;

    if (!notices || notices.length === 0) {
        el.innerHTML = getEmptyState('No notices at the moment', '📢');
        return;
    }

    // Type → accent colour
    const typeColours = {
        General:     { border: 'border-blue-500',   bg: 'bg-blue-50',   badge: 'bg-blue-600' },
        Maintenance: { border: 'border-orange-500', bg: 'bg-orange-50', badge: 'bg-orange-600' },
        Security:    { border: 'border-red-500',    bg: 'bg-red-50',    badge: 'bg-red-600' },
        Event:       { border: 'border-purple-500', bg: 'bg-purple-50', badge: 'bg-purple-600' },
        Urgent:      { border: 'border-red-500',    bg: 'bg-red-50',    badge: 'bg-red-600' }
    };

    el.innerHTML = notices.map(n => {
        const type   = n.Type || 'General';
        const body   = n.Body || n.body || '';
        const style  = typeColours[type] || typeColours.General;

        return `
        <div class="p-4 ${style.bg} border-l-4 ${style.border} rounded-lg mb-3 fade-in">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center mb-2">
                        <span class="px-2 py-1 ${style.badge} text-white text-xs font-semibold rounded mr-2">${type}</span>
                    </div>
                    <p class="text-gray-700">${body}</p>
                </div>
            </div>
        </div>`;
    }).join('');
}