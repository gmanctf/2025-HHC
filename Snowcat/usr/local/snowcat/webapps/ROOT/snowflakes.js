document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    for (let i = 0; i < 100; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.style.left = Math.random() * 100 + 'vw';
        snowflake.style.top = Math.random() * 100 + 'vh';
        snowflake.style.animationDuration = Math.random() * 3 + 7 + 's';
        snowflake.style.fontSize = Math.random() * 10 + 10 + 'px';
        snowflake.textContent = '❄';
        body.appendChild(snowflake);
    }
});