// ─── Reusable Weather Widget ──────────────────────────────────────────────
// Usage:  renderWeatherWidget(containerElementOrId, weatherDataObject)
//
// weatherDataObject shape (as returned by GET /user/weather → data):
//   { temp, weather_desc, city, country }
//
// Call with null / undefined to show the "unavailable" fallback.

function getWeatherIcon(desc) {
    desc = (desc || '').toLowerCase();
    if (desc.includes('clear')  || desc.includes('sunny'))   return '☀️';
    if (desc.includes('cloud'))                              return '☁️';
    if (desc.includes('rain'))                               return '🌧️';
    if (desc.includes('storm') || desc.includes('thunder'))  return '⛈️';
    if (desc.includes('snow'))                               return '❄️';
    if (desc.includes('mist')  || desc.includes('fog'))      return '🌫️';
    if (desc.includes('drizzle'))                            return '🌦️';
    return '🌤️';
}

function getWeatherGradient(desc) {
    desc = (desc || '').toLowerCase();
    if (desc.includes('clear')  || desc.includes('sunny'))              return 'weather-gradient-sunny';
    if (desc.includes('cloud'))                                         return 'weather-gradient-cloudy';
    if (desc.includes('rain') || desc.includes('drizzle'))              return 'weather-gradient-rainy';
    return 'weather-gradient';
}

function renderWeatherWidget(container, weatherData) {
    const el = typeof container === 'string'
        ? document.getElementById(container)
        : container;

    if (!el) return;

    // ── Fallback when data is missing ──
    if (!weatherData) {
        el.innerHTML = `
        <div class="bg-gray-100 rounded-3xl p-8 text-center">
            <p class="text-gray-500">Unable to load weather information</p>
        </div>`;
        return;
    }

    const temp     = Math.round(weatherData.temp);
    const desc     = weatherData.weather_desc || 'Unknown';
    const city     = weatherData.city || 'Unknown';
    const country  = weatherData.country || '';
    const humidity = weatherData.humidity || '--';
    const wind     = weatherData.wind_speed || '--';
    const gradient = getWeatherGradient(desc);
    const icon     = getWeatherIcon(desc);
    const today    = new Date().toLocaleDateString('en-IN', {
        weekday: 'long', month: 'long', day: 'numeric'
    });

    el.innerHTML = `
    <div class="${gradient} rounded-3xl shadow-2xl p-8 text-white fade-in">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-6">
            <!-- Left: text -->
            <div>
                <p class="text-white/80 text-lg mb-1">Current Weather</p>
                <h2 class="text-6xl font-extrabold tracking-tight mb-2">${temp}°C</h2>
                <p class="text-xl capitalize font-medium">${desc}</p>
                <p class="text-white/80 mt-4 flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    ${city}, ${country}
                </p>
            </div>
            <!-- Right: icon + extra stats -->
            <div class="text-center">
                <div class="text-9xl leading-none mb-3">${icon}</div>
                <p class="text-white/70 text-sm">${today}</p>
                <!-- Mini stats -->
                <div class="flex gap-6 mt-4 justify-center">
                    <div class="text-center">
                        <svg class="w-5 h-5 mx-auto text-white/60 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m8.66-12.66l-.71.71M4.05 19.95l-.71.71M21 12h-1M4 12H3m16.66 7.66l-.71-.71M4.05 4.05l-.71-.71M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                        <p class="text-xs text-white/60">Humidity</p>
                        <p class="text-sm font-bold">${humidity}%</p>
                    </div>
                    <div class="text-center">
                        <svg class="w-5 h-5 mx-auto text-white/60 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                        <p class="text-xs text-white/60">Wind</p>
                        <p class="text-sm font-bold">${wind} km/h</p>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
}