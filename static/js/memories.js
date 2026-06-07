document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.memory-filter');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
