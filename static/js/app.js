// Calorie Tracker JavaScript Application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();

    // Initialize PWA functionality
    initializePWA();
});

function initializeApp() {
    // Initialize drag and drop functionality
    initializeDragAndDrop();

    // Initialize form validation
    initializeFormValidation();

    // Initialize tooltips and popovers
    initializeBootstrapComponents();

    // Initialize auto-save functionality
    initializeAutoSave();
}

// Drag and Drop File Upload
function initializeDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');

    uploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        if (!fileInput) return;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, () => area.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, () => area.classList.remove('dragover'), false);
        });

        // Handle dropped files
        area.addEventListener('drop', (e) => handleDrop(e, fileInput), false);

        // Handle click to open file dialog
        area.addEventListener('click', () => fileInput.click());
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e, fileInput) {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect(files[0], fileInput);
    }
}

function handleFileSelect(file, input) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showAlert('Please select an image file.', 'danger');
        return false;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showAlert('File size must be less than 16MB.', 'danger');
        return false;
    }

    // Show preview if preview element exists
    const previewContainer = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');

    if (previewContainer && previewImg) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewContainer.classList.remove('d-none');

            // Add fade-in animation
            previewContainer.classList.add('fade-in-up');
        };
        reader.readAsDataURL(file);
    }

    return true;
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });

    return isValid;
}

function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    let isValid = true;
    let message = '';

    // Check if required field is empty
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required.';
    }
    // Validate email
    else if (type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Please enter a valid email address.';
    }
    // Validate password length
    else if (type === 'password' && value && value.length < 8) {
        isValid = false;
        message = 'Password must be at least 8 characters long.';
    }
    // Validate numeric inputs
    else if (type === 'number' && value) {
        const num = parseFloat(value);
        const min = input.getAttribute('min');
        const max = input.getAttribute('max');

        if (isNaN(num)) {
            isValid = false;
            message = 'Please enter a valid number.';
        } else if (min !== null && num < parseFloat(min)) {
            isValid = false;
            message = `Value must be at least ${min}.`;
        } else if (max !== null && num > parseFloat(max)) {
            isValid = false;
            message = `Value must be no more than ${max}.`;
        }
    }

    // Show/hide validation message
    showInputValidation(input, isValid, message);
    return isValid;
}

function showInputValidation(input, isValid, message) {
    // Remove existing validation classes
    input.classList.remove('is-valid', 'is-invalid');

    // Remove existing feedback
    const existingFeedback = input.parentNode.querySelector('.invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    if (!isValid) {
        input.classList.add('is-invalid');

        // Add error message
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        input.parentNode.appendChild(feedback);
    } else if (input.value.trim()) {
        input.classList.add('is-valid');
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Bootstrap Components
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Auto-save functionality for form fields
function initializeAutoSave() {
    const autoSaveFields = document.querySelectorAll('[data-auto-save]');

    autoSaveFields.forEach(field => {
        const key = field.dataset.autoSave;

        // Load saved value
        const savedValue = localStorage.getItem(`autosave_${key}`);
        if (savedValue && !field.value) {
            field.value = savedValue;
        }

        // Save on change
        field.addEventListener('input', debounce(function() {
            localStorage.setItem(`autosave_${key}`, field.value);
        }, 500));
    });
}

// Utility Functions

function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert after any existing alerts
    const existingAlerts = alertContainer.querySelectorAll('.alert');
    if (existingAlerts.length > 0) {
        existingAlerts[existingAlerts.length - 1].insertAdjacentElement('afterend', alertDiv);
    } else {
        alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    }

    // Auto-dismiss after duration
    if (duration > 0) {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    }
}

function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;

        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };

        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);

        if (callNow) func.apply(context, args);
    };
}

function formatNumber(num, decimals = 1) {
    return parseFloat(num).toFixed(decimals);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// API Helper Functions

function makeApiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };

    const finalOptions = { ...defaultOptions, ...options };

    return fetch(url, finalOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('API request failed:', error);
            showAlert('Request failed. Please try again.', 'danger');
            throw error;
        });
}

// Food Search Functionality
function searchFood(query, callback) {
    if (query.length < 2) {
        callback([]);
        return;
    }

    makeApiRequest(`/api/search_food?q=${encodeURIComponent(query)}`)
        .then(foods => {
            callback(foods);
        })
        .catch(error => {
            console.error('Food search failed:', error);
            callback([]);
        });
}

// Loading States
function showLoading(element, text = 'Loading...') {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }

    if (element) {
        element.innerHTML = `
            <div class="text-center p-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="mt-2">${text}</div>
            </div>
        `;
    }
}

function hideLoading(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }

    if (element) {
        element.innerHTML = '';
    }
}

// Image Compression (for large images)
function compressImage(file, maxWidth = 1024, maxHeight = 1024, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = function() {
            // Calculate new dimensions
            let { width, height } = img;

            if (width > height) {
                if (width > maxWidth) {
                    height *= maxWidth / width;
                    width = maxWidth;
                }
            } else {
                if (height > maxHeight) {
                    width *= maxHeight / height;
                    height = maxHeight;
                }
            }

            // Set canvas dimensions
            canvas.width = width;
            canvas.height = height;

            // Draw and compress
            ctx.drawImage(img, 0, 0, width, height);

            canvas.toBlob(resolve, 'image/jpeg', quality);
        };

        img.src = URL.createObjectURL(file);
    });
}

// PWA Functionality
let deferredPrompt;

function initializePWA() {
    // Check if service worker is supported
    if ('serviceWorker' in navigator) {
        registerServiceWorker();
    }

    // Handle PWA install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent the mini-infobar from appearing on mobile
        e.preventDefault();
        // Stash the event so it can be triggered later
        deferredPrompt = e;

        // Show install banner if not dismissed before
        if (!localStorage.getItem('pwa-dismissed')) {
            showInstallBanner();
        }
    });

    // Handle PWA install success
    window.addEventListener('appinstalled', () => {
        console.log('PWA was installed');
        hideInstallBanner();
        showAlert('App installed successfully! You can now use CalorieApp offline.', 'success');
    });

    // Set up install banner buttons
    const installBtn = document.getElementById('pwa-install-btn');
    const dismissBtn = document.getElementById('pwa-dismiss-btn');

    if (installBtn) {
        installBtn.addEventListener('click', installPWA);
    }

    if (dismissBtn) {
        dismissBtn.addEventListener('click', dismissInstallBanner);
    }

    // Hide address bar on mobile when running as standalone
    if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone) {
        document.body.classList.add('standalone');
    }
}

function registerServiceWorker() {
    navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
            console.log('Service Worker registered successfully:', registration.scope);

            // Check for updates
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        showAlert('New version available! Refresh to update.', 'info');
                    }
                });
            });
        })
        .catch((error) => {
            console.log('Service Worker registration failed:', error);
        });
}

function showInstallBanner() {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) {
        banner.style.display = 'block';

        // Add slide up animation
        setTimeout(() => {
            banner.style.transform = 'translateY(0)';
        }, 100);
    }
}

function hideInstallBanner() {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) {
        banner.style.display = 'none';
    }
}

function installPWA() {
    if (deferredPrompt) {
        // Show the install prompt
        deferredPrompt.prompt();

        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the PWA install prompt');
                hideInstallBanner();
            } else {
                console.log('User dismissed the PWA install prompt');
            }
            deferredPrompt = null;
        });
    }
}

function dismissInstallBanner() {
    hideInstallBanner();
    // Remember that user dismissed it
    localStorage.setItem('pwa-dismissed', 'true');
}

// Check if running as PWA
function isPWA() {
    return window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone ||
           document.referrer.includes('android-app://');
}

// Export for use in other scripts
window.CalorieTracker = {
    showAlert,
    makeApiRequest,
    searchFood,
    showLoading,
    hideLoading,
    compressImage,
    formatNumber,
    formatDate,
    isPWA,
    showInstallBanner,
    hideInstallBanner
};