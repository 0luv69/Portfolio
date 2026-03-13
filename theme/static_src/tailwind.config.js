/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            fontFamily: {
            sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
            display: ['Poppins', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
            },
            colors: {
            brand: {
                50: '#ecfdf5',
                100: '#d1fae5',
                200: '#a7f3d0',
                300: '#6ee7b7',
                400: '#34d399',
                500: '#10b981',
                600: '#059669',
                700: '#047857',
            },
            surface: {
                900: '#0f172a',
                800: '#111827',
                700: '#1f2937',
            },
            },
            boxShadow: {
            soft: '0 8px 30px rgba(0,0,0,0.24)',
            softLg: '0 18px 50px rgba(0,0,0,0.35)',
            },
            borderRadius: {
            xl2: '1rem',
            },
            transitionTimingFunction: {
            premium: 'cubic-bezier(0.22, 1, 0.36, 1)',
            },
        },
    },
    plugins: [

        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
