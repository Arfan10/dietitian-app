
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Pikaday date picker
    const picker = new Pikaday({
        field: document.getElementById('date_picker'),
        format: 'YYYY-MM-DD',
        minDate: new Date(), // disable past dates
        onSelect: function(date) {
            // Format the date as YYYY-MM-DD
            const dateStr = date.toISOString().split('T')[0];
            
            // Update hidden date input
            document.getElementById('id_date').value = dateStr;
            
            // Fetch available time slots for the selected date
            fetchAvailableTimeSlots(dateStr);
        }
    });

    // Function to fetch available time slots from the server
    function fetchAvailableTimeSlots(date) {
        const timeSelect = document.getElementById('id_time');
        timeSelect.innerHTML = '<option value="">Loading available times...</option>';
        
        fetch(`/get_available_slots/?date=${date}`)
            .then(response => response.json())
            .then(data => {
                timeSelect.innerHTML = '<option value="">Select a time slot</option>';
                
                if (data.available_slots && data.available_slots.length > 0) {
                    data.available_slots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot;
                        option.textContent = slot;
                        timeSelect.appendChild(option);
                    });
                } else {
                    timeSelect.innerHTML = '<option value="">No available slots for this date</option>';

                    console.log('Server response:', data); // Debug logging
                }
            })
            .catch(error => {
                console.error('Error fetching time slots:', error);
                timeSelect.innerHTML = '<option value="">Error loading time slots</option>';
            });
    }

    // Form submission with validation
    const form = document.getElementById('appointmentForm');
    form.addEventListener('submit', function(event) {
        const fullName = document.getElementById('id_full_name').value.trim();
        const email = document.getElementById('id_email').value.trim();
        const date = document.getElementById('id_date').value;
        const time = document.getElementById('id_time').value;
        const messageEl = document.getElementById('formMessage');
        
        // Simple validation
        if (!fullName || !email || !date || !time) {
            event.preventDefault();
            messageEl.textContent = 'Please fill in all required fields';
            messageEl.className = 'mt-4 text-center text-sm font-medium text-red-600';
            return false;
        }
        
        // Disable submit button to prevent double submission
        document.getElementById('submitBtn').disabled = true;
        document.getElementById('submitBtn').textContent = 'Booking...';
    });
     const toggleBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');

        toggleBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle ('hidden');
  });
});