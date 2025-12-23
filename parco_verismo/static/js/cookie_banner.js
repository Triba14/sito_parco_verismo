// Cookie Banner GDPR - Parco Letterario Giovanni Verga e Luigi Capuana
// Gestione consenso cookie conforme normativa italiana

(function () {
    'use strict';

    const COOKIE_NAME = 'cookie_consent';
    const COOKIE_DURATION = 365; // giorni

    // Funzioni helper per cookie
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/;SameSite=Lax";
    }

    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    function deleteCookie(name) {
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
    }

    function getStoredPreferences() {
        const consent = getCookie(COOKIE_NAME);
        if (consent) {
            try {
                return JSON.parse(consent);
            } catch (e) {
                return null;
            }
        }
        return null;
    }

    function saveConsent(preferences) {
        const consent = JSON.stringify(preferences);
        setCookie(COOKIE_NAME, consent, COOKIE_DURATION);

        // Applica le preferenze
        applyConsent(preferences);

        // Nascondi banner e modal
        hideBanner();
        hidePreferencesModal();

        // Dispatch evento per notificare altri script
        window.dispatchEvent(new CustomEvent('cookieConsentUpdated', { detail: preferences }));
    }

    function applyConsent(preferences) {
        // Cookie tecnici sempre attivi (necessari per il funzionamento)

        // Cookie analytics
        if (preferences.analytics) {
            enableAnalytics();
        } else {
            disableAnalytics();
        }

        // Cookie marketing/social
        if (preferences.marketing) {
            enableMarketing();
        } else {
            disableMarketing();
        }
    }

    function enableAnalytics() {
        console.log('Analytics cookies enabled');
        document.body.classList.add('analytics-enabled');

        // Carica Google Analytics GA4
        const gaMeasurementId = window.GA_MEASUREMENT_ID;
        if (gaMeasurementId && !window.gtag) {
            // Carica gtag.js
            const script = document.createElement('script');
            script.async = true;
            script.src = 'https://www.googletagmanager.com/gtag/js?id=' + gaMeasurementId;
            document.head.appendChild(script);

            // Inizializza gtag
            window.dataLayer = window.dataLayer || [];
            window.gtag = function () { dataLayer.push(arguments); };
            gtag('js', new Date());
            gtag('config', gaMeasurementId, {
                'anonymize_ip': true,  // Anonimizza IP per GDPR
                'cookie_flags': 'SameSite=None;Secure'
            });

            console.log('Google Analytics loaded:', gaMeasurementId);
        }
    }

    function disableAnalytics() {
        console.log('Analytics cookies disabled');
        document.body.classList.remove('analytics-enabled');

        // Disabilita Google Analytics
        const gaMeasurementId = window.GA_MEASUREMENT_ID;
        if (gaMeasurementId) {
            window['ga-disable-' + gaMeasurementId] = true;
        }

        // Rimuovi cookie GA esistenti
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('_ga') || cookie.startsWith('_gid') || cookie.startsWith('_gat')) {
                const name = cookie.split('=')[0];
                document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;';
                document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=.' + window.location.hostname;
            }
        }
    }

    function enableMarketing() {
        console.log('Marketing cookies enabled');
        document.body.classList.add('marketing-enabled');
    }

    function disableMarketing() {
        console.log('Marketing cookies disabled');
        document.body.classList.remove('marketing-enabled');
    }

    function showBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.add('show');
            banner.setAttribute('aria-hidden', 'false');
        }
    }

    function hideBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('show');
            banner.setAttribute('aria-hidden', 'true');
        }
    }

    function showPreferencesModal() {
        const modal = document.getElementById('cookie-preferences-modal');
        if (modal) {
            // Carica preferenze salvate nei toggle
            loadPreferencesIntoModal();

            modal.classList.add('show');
            modal.setAttribute('aria-hidden', 'false');

            // Focus trap per accessibilità
            const firstFocusable = modal.querySelector('button, input:not([disabled])');
            if (firstFocusable) {
                firstFocusable.focus();
            }
        }
    }

    function hidePreferencesModal() {
        const modal = document.getElementById('cookie-preferences-modal');
        if (modal) {
            modal.classList.remove('show');
            modal.setAttribute('aria-hidden', 'true');
        }
    }

    function loadPreferencesIntoModal() {
        const preferences = getStoredPreferences() || {
            necessary: true,
            analytics: false,
            marketing: false
        };

        const analyticsCheckbox = document.getElementById('analytics-cookies');
        const marketingCheckbox = document.getElementById('marketing-cookies');

        if (analyticsCheckbox) {
            analyticsCheckbox.checked = preferences.analytics || false;
        }
        if (marketingCheckbox) {
            marketingCheckbox.checked = preferences.marketing || false;
        }
    }

    function getPreferencesFromModal() {
        const analyticsCheckbox = document.getElementById('analytics-cookies');
        const marketingCheckbox = document.getElementById('marketing-cookies');

        return {
            necessary: true,
            analytics: analyticsCheckbox ? analyticsCheckbox.checked : false,
            marketing: marketingCheckbox ? marketingCheckbox.checked : false,
            timestamp: new Date().toISOString()
        };
    }

    function revokeConsent() {
        deleteCookie(COOKIE_NAME);
        document.body.classList.remove('analytics-enabled', 'marketing-enabled');
        showBanner();
    }

    // Inizializzazione
    function init() {
        const preferences = getStoredPreferences();

        if (!preferences) {
            showBanner();
        } else {
            applyConsent(preferences);
        }

        // Event listeners per i pulsanti del banner
        const acceptAllBtn = document.getElementById('accept-all-cookies');
        const acceptNecessaryBtn = document.getElementById('accept-necessary-cookies');
        const customizeBtn = document.getElementById('customize-cookies');

        if (acceptAllBtn) {
            acceptAllBtn.addEventListener('click', function () {
                saveConsent({
                    necessary: true,
                    analytics: true,
                    marketing: true,
                    timestamp: new Date().toISOString()
                });
            });
        }

        if (acceptNecessaryBtn) {
            acceptNecessaryBtn.addEventListener('click', function () {
                saveConsent({
                    necessary: true,
                    analytics: false,
                    marketing: false,
                    timestamp: new Date().toISOString()
                });
            });
        }

        if (customizeBtn) {
            customizeBtn.addEventListener('click', function () {
                showPreferencesModal();
            });
        }

        // Event listeners per il modal
        const savePreferencesBtn = document.getElementById('save-preferences');
        const closeModalBtn = document.querySelector('.cookie-modal-close');

        if (savePreferencesBtn) {
            savePreferencesBtn.addEventListener('click', function () {
                const preferences = getPreferencesFromModal();
                saveConsent(preferences);
            });
        }

        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', function () {
                hidePreferencesModal();
            });
        }

        // Chiudi modal cliccando fuori o premendo ESC
        const modal = document.getElementById('cookie-preferences-modal');
        if (modal) {
            modal.addEventListener('click', function (e) {
                if (e.target === modal) {
                    hidePreferencesModal();
                }
            });
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                hidePreferencesModal();
            }
        });

        // Link "Gestisci cookie" nel footer o altrove
        document.querySelectorAll('[data-cookie-preferences]').forEach(function (el) {
            el.addEventListener('click', function (e) {
                e.preventDefault();
                showPreferencesModal();
            });
        });

        // Link "Revoca consenso"
        document.querySelectorAll('[data-cookie-revoke]').forEach(function (el) {
            el.addEventListener('click', function (e) {
                e.preventDefault();
                revokeConsent();
            });
        });
    }

    // Avvia quando il DOM è pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Esponi funzioni globali
    window.CookieConsent = {
        showBanner: showBanner,
        showPreferences: showPreferencesModal,
        getPreferences: getStoredPreferences,
        revokeConsent: revokeConsent,
        saveConsent: saveConsent
    };

    // Retrocompatibilità
    window.reopenCookiePreferences = showPreferencesModal;

})();
