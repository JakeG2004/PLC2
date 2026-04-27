document.addEventListener('DOMContentLoaded', () => {
    // Select all <td> elements that have the attribute tag="type"
    const types = document.getElementsByClassName("log_type")

    for(var i = 0; i < types.length; i++) {
        cur_td = types[i];

        const typeValue = cur_td.textContent.trim();
        const className = getTypeClass(typeValue);

        if(className) {
            cur_td.classList.add(`${className}`);
        }
    }
});

// Helper to color-code the "Type" column based on severity
function getTypeClass(type) {
    const t = type.toUpperCase();
    if (t.includes('ERROR') || t.includes('SAFETY')) return 'bg-danger';
    if (t.includes('OPERATION MODE')) return 'bg-warning';
    if (t.includes('COMPLETE')) return 'bg-success';
    if (t.includes('CHECKPOINT')) return 'bg-info';
    return 'bg-primary';
}