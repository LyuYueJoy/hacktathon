document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const navLinks = document.querySelectorAll(".nav-link, .collapsed-link");

    if (!sidebar || !sidebarToggle) {
        return;
    }

    const setCollapsed = (collapsed) => {
        sidebar.classList.toggle("collapsed", collapsed);
        sidebarToggle.setAttribute("aria-expanded", String(!collapsed));
    };

    setCollapsed(true);

    sidebarToggle.addEventListener("click", () => {
        const shouldCollapse = !sidebar.classList.contains("collapsed");
        setCollapsed(shouldCollapse);
    });

    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            setCollapsed(true);
        });
    });
});