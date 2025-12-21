function frostyMode() {
    console.log("❄ Frosties secret function!");

    createSnowfall();

    createFrostySleigh();

    playJingleBells();
    
    return "❄ Stay Cool! ❄";
}

function createSnowfall() {
    const snowflakeCount = 100;
    const container = document.createElement('div');
    container.id = 'snow-container';
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.pointerEvents = 'none';
    container.style.zIndex = '9999';
    
    for (let i = 0; i < snowflakeCount; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.innerHTML = '❄';
        snowflake.style.color = 'white';
        snowflake.style.position = 'absolute';
        snowflake.style.top = '-10px';
        snowflake.style.left = Math.random() * 100 + 'vw';
        snowflake.style.opacity = Math.random();
        snowflake.style.fontSize = (Math.random() * 20 + 10) + 'px';
        snowflake.style.animation = `fall ${Math.random() * 5 + 5}s linear infinite`;
        container.appendChild(snowflake);
    }
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fall {
            to { transform: translateY(100vh); }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(container);
    
    // Remove snow after 30 seconds
    setTimeout(() => {
        document.body.removeChild(container);
        document.head.removeChild(style);
    }, 30000);
}

function createFrostySleigh() {
    const sleigh = document.createElement('div');
    sleigh.innerHTML = 'AI Gnomes do not know the difference between left and right ☃ 🦌 🦌 🦌 🛷 ';
    sleigh.style.position = 'fixed';
    sleigh.style.top = '10%';
    sleigh.style.left = '-200px';
    sleigh.style.fontSize = '2rem';
    sleigh.style.zIndex = '10000';
    sleigh.style.transition = 'left 10s linear';
    sleigh.style.pointerEvents = 'none';

    document.body.appendChild(sleigh);

    setTimeout(() => {
        sleigh.style.left = '110%';
    }, 100);
    
    setTimeout(() => {
        document.body.removeChild(sleigh);
    }, 12000);
}

function playJingleBells() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const notes = [
        { note: 'E', duration: 0.25 },
        { note: 'E', duration: 0.25 },
        { note: 'E', duration: 0.5 },
        { note: 'E', duration: 0.25 },
        { note: 'E', duration: 0.25 },
        { note: 'E', duration: 0.5 },
        { note: 'E', duration: 0.25 },
        { note: 'G', duration: 0.25 },
        { note: 'C', duration: 0.25 },
        { note: 'D', duration: 0.25 },
        { note: 'E', duration: 1.0 }
    ];
    
    const frequencies = {
        'C': 261.63,
        'D': 293.66,
        'E': 329.63,
        'G': 392.00
    };
    
    let time = audioContext.currentTime;
    
    notes.forEach(note => {
        const oscillator = audioContext.createOscillator();
        oscillator.type = 'sine';
        oscillator.frequency.value = frequencies[note.note];
        
        const gainNode = audioContext.createGain();
        gainNode.gain.value = 0.3;
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.start(time);
        oscillator.stop(time + note.duration);
        
        time += note.duration;
    });
}

// Make it available globally
window.frostyMode = frostyMode;
