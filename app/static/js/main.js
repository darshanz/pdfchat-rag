$(document).ready(function () {
    const mainNav = $('#main-nav');
    mainNav.on('sl-select', (event) => {
        const selectedValue = event.detail.item.value;
        console.log(`Selected: ${selectedValue}`);
        switch (selectedValue) {
            case 'index':
                window.location.href = '/';
                break;
        }
    });
});