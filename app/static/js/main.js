document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const collapsedLinks = document.querySelectorAll(".collapsed-link");

    if (!sidebar || !sidebarToggle) {
        return;
    }

    sidebar.classList.add("collapsed");
    sidebarToggle.setAttribute("aria-expanded", "false");

    sidebarToggle.addEventListener("click", () => {
        const isCollapsed = sidebar.classList.contains("collapsed");
        sidebar.classList.toggle("collapsed", !isCollapsed);
        sidebarToggle.setAttribute("aria-expanded", String(isCollapsed));
    });

    collapsedLinks.forEach((link) => {
        link.addEventListener("click", () => {
            sidebar.classList.add("collapsed");
            sidebarToggle.setAttribute("aria-expanded", "false");
        });
    });
});