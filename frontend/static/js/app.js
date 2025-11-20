// Form handling - Direct Google Sheets submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('emailForm');
    const messageDiv = document.getElementById('formMessage');
    const buttonText = document.getElementById('buttonText');
    const buttonLoader = document.getElementById('buttonLoader');
    const submitBtn = form.querySelector('button');
    
    // Google Sheets Apps Script URL
    const SHEETS_URL = 'https://script.google.com/macros/s/AKfycbxCayIgmmTsOjG2PdoZL-tAs3cWnFe3F_Ham1B3jgdv3IYkcp2zlcCYJaIPlKotQbk5/exec';

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();

            // Validate inputs
            if (!name || !email) {
                showMessage('Please fill in all fields', 'error');
                trackEvent('form_validation_error', { field: !name ? 'name' : 'email' });
                return;
            }

            if (!isValidEmail(email)) {
                showMessage('Please enter a valid email address', 'error');
                trackEvent('form_validation_error', { field: 'email_format' });
                return;
            }

            // Show loading state
            setButtonLoading(true);
            trackEvent('form_submit_start', { name, email });

            // Create FormData for Google Sheets
            const formData = new FormData();
            formData.append('name', name);
            formData.append('email', email);
            formData.append('timestamp', new Date().toISOString());

            fetch(SHEETS_URL, { 
                method: 'POST', 
                body: formData 
            })
                .then(response => {
                    if (response.ok) {
                        showMessage('✓ Success! Check your email for the PDF guide.', 'success');
                        trackEvent('form_submit_success', { email });
                        form.reset();
                    } else {
                        throw new Error('Network response was not ok');
                    }
                })
                .catch(error => {
                    console.error('Form submission error:', error);
                    showMessage('✗ Error submitting form. Please try again.', 'error');
                    trackEvent('form_submit_error', { error: error.message });
                })
                .finally(() => {
                    setButtonLoading(false);
                });
        });
    }
});

/**
 * Show message to user
 */
function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.classList.remove('success', 'error');
    messageDiv.classList.add(type);
}

/**
 * Set button loading state
 */
function setButtonLoading(isLoading) {
    submitBtn.disabled = isLoading;
    
    if (isLoading) {
        buttonText.style.display = 'none';
        buttonLoader.style.display = 'inline';
    } else {
        buttonText.style.display = 'inline';
        buttonLoader.style.display = 'none';
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Smooth scroll to sections
 */
document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

/**
 * Track form interactions for analytics
 */
function trackEvent(eventName, data = {}) {
    console.log(`Event: ${eventName}`, data);
    
    // Google Analytics tracking (if gtag is loaded)
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, data);
    }
}
