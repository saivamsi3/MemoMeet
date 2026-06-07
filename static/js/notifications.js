document.addEventListener('DOMContentLoaded', function() {
    const markReadBtns = document.querySelectorAll('.mark-read');
    markReadBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const row = this.closest('.list-group-item');
            row.classList.remove('list-group-item-primary');
        });
    });
});
