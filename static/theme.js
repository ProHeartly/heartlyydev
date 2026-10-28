const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    updateIcon(savedTheme);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            const apply = () => {
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);

                updateIcon(newTheme);
            };
            
            if (document.startViewTransition) {
                const t = document.startViewTransition(apply);
                t.ready.then(() => {
                    const r = toggleBtn.getBoundingClientRect();
                    const x = r.left + r.width / 2;
                    const y = r.top + r.height / 2;
                    const radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));

                    document.documentElement.animate(
                        { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`] },
                        { duration: 1000, easing: 'ease-in', pseudoElement: '::view-transition-new(root)' }
                    )
                })
            } else {
                apply();
            }
        });
    }

    function updateIcon(theme) {
        if (theme === 'light') {
            themeIcon.className = 'ph-duotone ph-sun';
        } else {
            themeIcon.className = 'ph-duotone ph-moon';
        }
    }
});

if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js");
}