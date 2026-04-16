document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const pendingDeletes = new Set();

    document.querySelectorAll('.instant-delete-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const btn = this;
            const imageId = btn.getAttribute('data-image-id');
            const row = btn.closest('tr');

            // Hide the row visually
            row.style.display = 'none';

            // Add to deletion queue
            pendingDeletes.add(imageId);

            // Create Toast
            const toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.top = (20 + (document.querySelectorAll('.undo-toast').length * 70)) + 'px';
            toast.className = 'undo-toast';
            toast.style.left = '20px';
            toast.style.backgroundColor = '#333';
            toast.style.color = 'white';
            toast.style.padding = '15px 25px';
            toast.style.borderRadius = '5px';
            toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
            toast.style.zIndex = '9999';
            toast.style.display = 'flex';
            toast.style.alignItems = 'center';
            toast.style.gap = '15px';
            toast.style.overflow = 'hidden';

            toast.innerHTML = `
                <span style="font-weight: 500;">Image deleted.</span>
                <button type="button" class="undo-btn" style="background: transparent; color: #4dc0b5; border: 1px solid #4dc0b5; padding: 4px 12px; border-radius: 4px; font-weight: bold; cursor: pointer; transition: all 0.2s;">Undo</button>
                <div class="progress-bar" style="position: absolute; bottom: 0; left: 0; height: 4px; background-color: #4dc0b5; width: 100%; transition: width 10s linear;"></div>
            `;

            document.body.appendChild(toast);

            // Animate progress bar slightly after insertion to trigger CSS transition
            setTimeout(() => {
                const pb = toast.querySelector('.progress-bar');
                if (pb) pb.style.width = '0%';
            }, 50);

            // Undo button logic
            const undoBtn = toast.querySelector('.undo-btn');
            undoBtn.addEventListener('click', function () {
                pendingDeletes.delete(imageId); // Remove from queue
                row.style.display = ''; // Restore row
                toast.remove(); // Remove toast
            });

            // 10 second timeout for actual deletion if they stay on page
            setTimeout(() => {
                if (pendingDeletes.has(imageId)) {
                    pendingDeletes.delete(imageId);
                    toast.remove();

                    // Actually delete from server
                    fetch(`/ajax/delete-product-image/${imageId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken,
                            'Content-Type': 'application/json'
                        },
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                row.remove(); // Permanently remove DOM element
                            } else {
                                alert('Failed to delete image.');
                                row.style.display = ''; // Restore on failure
                            }
                        })
                        .catch(err => {
                            row.style.display = '';
                        });
                }
            }, 10000); // 10 seconds empty
        });
    });

    // Failsafe: if they navigate to storefront or hit "Save" before 10s is up
    window.addEventListener('beforeunload', function () {
        if (pendingDeletes.size > 0) {
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrftoken);

            pendingDeletes.forEach(id => {
                // sendBeacon synchronously fires the POST request as the page unloads
                navigator.sendBeacon(`/ajax/delete-product-image/${id}/`, formData);
            });
            pendingDeletes.clear();
        }
    });

    // Enforce single primary image selection on the frontend
    const primaryCheckboxes = document.querySelectorAll('input[name^="images-"][name$="-is_primary"]');
    primaryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                // If this is checked, uncheck all others
                primaryCheckboxes.forEach(cb => {
                    if (cb !== this) {
                        cb.checked = false;
                    }
                });
            }
        });
    });
});
