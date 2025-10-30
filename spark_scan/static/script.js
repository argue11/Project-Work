// citizen_portal/static/citizen_portal/js/script.js

// Image Upload Preview
document.addEventListener('DOMContentLoaded', function() {
    // Handle image upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const uploadBox = this.closest('.upload-box');
            
            if (files.length > 0) {
                // Show file count
                const fileCount = files.length;
                uploadBox.innerHTML = `
                    <div class="upload-icon">📸</div>
                    <div>${fileCount} photo(s) selected</div>
                    <small>Click to change</small>
                `;
                
                // You can add image preview functionality here
            }
        });
    });
    
    // OTP input auto-tab (if you want to implement 6 separate inputs)
    const otpInput = document.querySelector('.otp-input');
    if (otpInput) {
        otpInput.addEventListener('input', function(e) {
            if (this.value.length === 6) {
                this.form.submit();
            }
        });
    }
    
    // Mobile number formatting
    const mobileInput = document.querySelector('input[type="tel"]');
    if (mobileInput) {
        mobileInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('91')) {
                value = '+' + value;
            } else if (value.length === 10) {
                value = '+91 ' + value;
            }
            e.target.value = value;
        });
    }
});

// Form validation
function validateForm(form) {
    const mobile = form.querySelector('input[type="tel"]');
    const description = form.querySelector('textarea');
    
    if (mobile && mobile.value.replace(/\D/g, '').length < 10) {
        alert('Please enter a valid mobile number');
        return false;
    }
    
    if (description && description.value.trim().length < 10) {
        alert('Please provide a detailed description (minimum 10 characters)');
        return false;
    }
    
    return true;
}