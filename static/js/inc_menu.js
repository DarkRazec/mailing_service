const checkbox = document.getElementById('darkModeSwitch');
if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
    checkbox.checked = !checkbox.checked;
}

document.getElementById('darkModeSwitch').addEventListener('click',()=>{
    if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
        document.documentElement.setAttribute('data-bs-theme', 'light');
        localStorage.removeItem('isDark');
    }
    
    else {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        localStorage.setItem('isDark', 'dark');
    }
})