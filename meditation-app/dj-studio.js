/**
 * DJ Mix Studio - Interactive Functionality
 * ============================================
 */

// State Management
const studioState = {
    isPlaying: false,
    voiceTrack: {
        loaded: true,
        name: 'Connecting with Your Intuition',
        author: 'Visavi Kumar',
        duration: 720,
        currentTime: 154,
        volume: 80,
        muted: false,
        solo: false,
        eq: { high: 0, mid: 0, low: 0 },
        effects: { reverb: false, delay: false }
    },
    soundTrack: {
        loaded: true,
        name: 'Ocean Waves',
        category: 'Nature',
        loop: true,
        volume: 40,
        muted: false,
        solo: false,
        eq: { high: -30, mid: 0, low: 20 },
        effects: { reverb: true, filter: false }
    },
    crossfader: 50,
    blendMode: 'mix',
    masterVolume: 85,
    sessionTimer: 15,
    fadeIn: 5,
    fadeOut: 10
};

// DOM Elements
const elements = {
    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),

    // Transport
    masterPlayBtn: document.getElementById('masterPlayBtn'),
    skipBackBtn: document.getElementById('skipBackBtn'),
    skipForwardBtn: document.getElementById('skipForwardBtn'),

    // Faders
    voiceVolume: document.getElementById('voiceVolume'),
    soundVolume: document.getElementById('soundVolume'),
    crossfader: document.getElementById('crossfader'),
    masterVolume: document.getElementById('masterVolume'),

    // Mute/Solo
    voiceMute: document.getElementById('voiceMute'),
    voiceSolo: document.getElementById('voiceSolo'),
    soundMute: document.getElementById('soundMute'),
    soundSolo: document.getElementById('soundSolo'),

    // Blend modes
    blendBtns: document.querySelectorAll('.blend-btn'),

    // Presets
    presetCards: document.querySelectorAll('.preset-card'),
    timerBtns: document.querySelectorAll('.timer-btn'),

    // Waveforms
    voiceWaveform: document.getElementById('voiceWaveform'),
    soundWaveform: document.getElementById('soundWaveform'),
    voicePlayhead: document.getElementById('voicePlayhead'),
    soundPlayhead: document.getElementById('soundPlayhead'),

    // Add track buttons
    addTrackBtns: document.querySelectorAll('.add-track-btn'),

    // Filter chips
    chips: document.querySelectorAll('.chip'),

    // Save/Share
    saveBtn: document.getElementById('saveBtn'),
    shareBtn: document.getElementById('shareBtn')
};

/**
 * Initialize the studio
 */
function initStudio() {
    setupEventListeners();
    initWaveforms();
    initParticles();
    updateUI();
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Tab switching
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Transport controls
    elements.masterPlayBtn?.addEventListener('click', togglePlayback);
    elements.skipBackBtn?.addEventListener('click', skipBack);
    elements.skipForwardBtn?.addEventListener('click', skipForward);

    // Volume faders
    elements.voiceVolume?.addEventListener('input', (e) => {
        studioState.voiceTrack.volume = parseInt(e.target.value);
        updateVolumeDisplay('voice');
    });

    elements.soundVolume?.addEventListener('input', (e) => {
        studioState.soundTrack.volume = parseInt(e.target.value);
        updateVolumeDisplay('sound');
    });

    elements.crossfader?.addEventListener('input', (e) => {
        studioState.crossfader = parseInt(e.target.value);
        updateCrossfader();
    });

    elements.masterVolume?.addEventListener('input', (e) => {
        studioState.masterVolume = parseInt(e.target.value);
        document.querySelector('.mv-value').textContent = `${studioState.masterVolume}%`;
    });

    // Mute/Solo buttons
    elements.voiceMute?.addEventListener('click', () => toggleMute('voice'));
    elements.voiceSolo?.addEventListener('click', () => toggleSolo('voice'));
    elements.soundMute?.addEventListener('click', () => toggleMute('sound'));
    elements.soundSolo?.addEventListener('click', () => toggleSolo('sound'));

    // Blend modes
    elements.blendBtns.forEach(btn => {
        btn.addEventListener('click', () => setBlendMode(btn.dataset.mode));
    });

    // Presets
    elements.presetCards.forEach(card => {
        card.addEventListener('click', () => applyPreset(card.dataset.preset));
    });

    // Timer buttons
    elements.timerBtns.forEach(btn => {
        btn.addEventListener('click', () => setTimer(parseInt(btn.dataset.time)));
    });

    // Filter chips
    elements.chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chip.parentElement.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
        });
    });

    // Add track buttons
    elements.addTrackBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const trackItem = btn.closest('.track-item, .sound-item');
            addTrackToChannel(trackItem);
        });
    });

    // Save/Share
    elements.saveBtn?.addEventListener('click', saveMix);
    elements.shareBtn?.addEventListener('click', shareMix);

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboard);

    // Knob interactions
    document.querySelectorAll('.knob').forEach(knob => {
        setupKnobInteraction(knob);
    });

    // Drag and drop
    setupDragAndDrop();
}

/**
 * Switch between Voice and Sounds tabs
 */
function switchTab(tabName) {
    elements.tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    elements.tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
}

/**
 * Toggle playback
 */
function togglePlayback() {
    studioState.isPlaying = !studioState.isPlaying;

    elements.masterPlayBtn?.classList.toggle('playing', studioState.isPlaying);

    if (studioState.isPlaying) {
        startPlayback();
        showNotification('Playback started');
    } else {
        stopPlayback();
        showNotification('Playback paused');
    }
}

let playbackInterval = null;

function startPlayback() {
    animateWaveforms();

    playbackInterval = setInterval(() => {
        if (studioState.voiceTrack.loaded) {
            studioState.voiceTrack.currentTime++;
            updatePlayhead('voice');

            if (studioState.voiceTrack.currentTime >= studioState.voiceTrack.duration) {
                studioState.voiceTrack.currentTime = 0;
            }
        }
    }, 1000);
}

function stopPlayback() {
    if (playbackInterval) {
        clearInterval(playbackInterval);
        playbackInterval = null;
    }
}

/**
 * Skip controls
 */
function skipBack() {
    studioState.voiceTrack.currentTime = Math.max(0, studioState.voiceTrack.currentTime - 15);
    updatePlayhead('voice');
}

function skipForward() {
    studioState.voiceTrack.currentTime = Math.min(
        studioState.voiceTrack.duration,
        studioState.voiceTrack.currentTime + 15
    );
    updatePlayhead('voice');
}

/**
 * Update playhead position
 */
function updatePlayhead(channel) {
    const track = channel === 'voice' ? studioState.voiceTrack : studioState.soundTrack;
    const playhead = channel === 'voice' ? elements.voicePlayhead : elements.soundPlayhead;

    if (playhead && track.duration) {
        const progress = (track.currentTime / track.duration) * 100;
        playhead.style.left = `${16 + (progress * 0.68)}%`;
    }

    // Update time display
    const container = playhead?.closest('.waveform-container');
    const currentTimeEl = container?.querySelector('.current');
    if (currentTimeEl) {
        currentTimeEl.textContent = formatTime(track.currentTime);
    }
}

/**
 * Update volume displays
 */
function updateVolumeDisplay(channel) {
    const track = channel === 'voice' ? studioState.voiceTrack : studioState.soundTrack;
    const valueEl = document.getElementById(`${channel}VolValue`);
    const meterFill = document.querySelector(`.${channel}-channel .meter-fill`);

    if (valueEl) valueEl.textContent = `${track.volume}%`;
    if (meterFill) meterFill.style.height = `${track.volume}%`;
}

/**
 * Update crossfader visual
 */
function updateCrossfader() {
    const leftFill = document.querySelector('.cf-fill.left');
    const rightFill = document.querySelector('.cf-fill.right');

    if (leftFill) leftFill.style.width = `${studioState.crossfader}%`;
    if (rightFill) rightFill.style.width = `${100 - studioState.crossfader}%`;
}

/**
 * Toggle mute
 */
function toggleMute(channel) {
    const track = channel === 'voice' ? studioState.voiceTrack : studioState.soundTrack;
    track.muted = !track.muted;

    const btn = channel === 'voice' ? elements.voiceMute : elements.soundMute;
    btn?.classList.toggle('active', track.muted);

    showNotification(`${channel === 'voice' ? 'Voice' : 'Sound'} track ${track.muted ? 'muted' : 'unmuted'}`);
}

/**
 * Toggle solo
 */
function toggleSolo(channel) {
    const track = channel === 'voice' ? studioState.voiceTrack : studioState.soundTrack;
    track.solo = !track.solo;

    const btn = channel === 'voice' ? elements.voiceSolo : elements.soundSolo;
    btn?.classList.toggle('active', track.solo);

    showNotification(`${channel === 'voice' ? 'Voice' : 'Sound'} track ${track.solo ? 'soloed' : 'unsoloed'}`);
}

/**
 * Set blend mode
 */
function setBlendMode(mode) {
    studioState.blendMode = mode;

    elements.blendBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    showNotification(`Blend mode: ${mode.toUpperCase()}`);
}

/**
 * Apply preset
 */
function applyPreset(presetName) {
    const presets = {
        'deep-focus': { voiceVol: 70, soundVol: 30, crossfader: 65 },
        'sleep': { voiceVol: 50, soundVol: 70, crossfader: 35 },
        'energize': { voiceVol: 90, soundVol: 50, crossfader: 70 },
        'relaxation': { voiceVol: 60, soundVol: 60, crossfader: 50 }
    };

    const preset = presets[presetName];
    if (!preset) return;

    // Apply preset values
    studioState.voiceTrack.volume = preset.voiceVol;
    studioState.soundTrack.volume = preset.soundVol;
    studioState.crossfader = preset.crossfader;

    // Update UI
    if (elements.voiceVolume) elements.voiceVolume.value = preset.voiceVol;
    if (elements.soundVolume) elements.soundVolume.value = preset.soundVol;
    if (elements.crossfader) elements.crossfader.value = preset.crossfader;

    updateVolumeDisplay('voice');
    updateVolumeDisplay('sound');
    updateCrossfader();

    // Update active state
    elements.presetCards.forEach(card => {
        card.classList.toggle('active', card.dataset.preset === presetName);
    });

    showNotification(`Applied preset: ${presetName.replace('-', ' ')}`);
}

/**
 * Set session timer
 */
function setTimer(minutes) {
    studioState.sessionTimer = minutes;

    elements.timerBtns.forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.time) === minutes);
    });

    // Update display
    document.querySelector('.timer-minutes').textContent = minutes;

    // Update ring progress (visual only)
    const progress = document.querySelector('.timer-progress');
    if (progress) {
        const circumference = 339.292;
        const offset = circumference * (1 - minutes / 60);
        progress.style.strokeDashoffset = offset;
    }

    showNotification(`Timer set to ${minutes} minutes`);
}

/**
 * Add track to channel
 */
function addTrackToChannel(trackItem) {
    const isVoice = trackItem.classList.contains('track-item');
    const channel = isVoice ? 'voiceTrack' : 'soundTrack';

    const name = trackItem.querySelector('.track-name, .sound-name')?.textContent;
    const author = trackItem.querySelector('.track-author, .sound-category')?.textContent;

    studioState[channel].name = name;
    studioState[channel].author = author;
    studioState[channel].loaded = true;

    showNotification(`Added: ${name}`);
}

/**
 * Save mix
 */
function saveMix() {
    const mixData = {
        ...studioState,
        savedAt: new Date().toISOString()
    };

    // In a real app, this would save to a backend
    localStorage.setItem('savedMix', JSON.stringify(mixData));

    showNotification('Mix saved successfully!', 'success');
}

/**
 * Share mix
 */
function shareMix() {
    // In a real app, this would generate a shareable link
    showNotification('Share link copied to clipboard!', 'success');
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboard(e) {
    if (e.target.matches('input, textarea')) return;

    switch (e.code) {
        case 'Space':
            e.preventDefault();
            togglePlayback();
            break;
        case 'KeyM':
            toggleMute('voice');
            break;
        case 'KeyN':
            toggleMute('sound');
            break;
        case 'ArrowLeft':
            skipBack();
            break;
        case 'ArrowRight':
            skipForward();
            break;
        case 'Digit1':
            applyPreset('deep-focus');
            break;
        case 'Digit2':
            applyPreset('sleep');
            break;
        case 'Digit3':
            applyPreset('energize');
            break;
        case 'Digit4':
            applyPreset('relaxation');
            break;
    }
}

/**
 * Setup knob interaction
 */
function setupKnobInteraction(knob) {
    let isDragging = false;
    let startY = 0;
    let startRotation = 0;

    knob.addEventListener('mousedown', (e) => {
        isDragging = true;
        startY = e.clientY;
        const dial = knob.querySelector('.knob-dial');
        const transform = dial.style.transform;
        startRotation = parseInt(transform.replace(/[^-\d]/g, '')) || 0;
        document.body.style.cursor = 'grabbing';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const deltaY = startY - e.clientY;
        const newRotation = Math.max(-135, Math.min(135, startRotation + deltaY));

        const dial = knob.querySelector('.knob-dial');
        dial.style.transform = `rotate(${newRotation}deg)`;
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        document.body.style.cursor = '';
    });
}

/**
 * Setup drag and drop
 */
function setupDragAndDrop() {
    const trackItems = document.querySelectorAll('.track-item, .sound-item');
    const dropZones = document.querySelectorAll('.track-drop-zone');

    trackItems.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', item.dataset.track || item.dataset.sound);
            item.classList.add('dragging');
        });

        item.addEventListener('dragend', () => {
            item.classList.remove('dragging');
        });
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('drag-over');
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');
            const trackId = e.dataTransfer.getData('text/plain');
            showNotification(`Dropped track: ${trackId}`);
        });
    });
}

/**
 * Initialize waveforms
 */
function initWaveforms() {
    drawWaveform(elements.voiceWaveform, '#8b5cf6');
    drawWaveform(elements.soundWaveform, '#06b6d4');
}

function drawWaveform(canvas, color) {
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.offsetWidth * 2;
    const height = canvas.height = canvas.offsetHeight * 2;
    ctx.scale(2, 2);

    const centerY = height / 4;
    const bars = 100;
    const barWidth = (width / 2) / bars;
    const gap = 2;

    ctx.fillStyle = color;

    for (let i = 0; i < bars; i++) {
        const barHeight = Math.random() * (height / 3) + 10;
        const x = i * barWidth;
        const y = centerY - barHeight / 2;

        ctx.globalAlpha = 0.3 + Math.random() * 0.4;
        ctx.fillRect(x, y, barWidth - gap, barHeight);
    }
}

function animateWaveforms() {
    // Add animation class or redraw waveforms periodically
    if (studioState.isPlaying) {
        requestAnimationFrame(animateWaveforms);
    }
}

/**
 * Initialize particles
 */
function initParticles() {
    const container = document.getElementById('particles');
    if (!container) return;

    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${2 + Math.random() * 4}px;
            height: ${2 + Math.random() * 4}px;
            background: rgba(139, 92, 246, ${0.2 + Math.random() * 0.3});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: particleFloat ${5 + Math.random() * 10}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        container.appendChild(particle);
    }

    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleFloat {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
            50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1.5); opacity: 0.6; }
        }
    `;
    document.head.appendChild(style);
}

/**
 * Update UI to reflect current state
 */
function updateUI() {
    updateVolumeDisplay('voice');
    updateVolumeDisplay('sound');
    updateCrossfader();
    updatePlayhead('voice');
}

/**
 * Format time
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.studio-notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = `studio-notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
    `;
    notification.style.cssText = `
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        padding: 12px 24px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10b981, #059669)' : 'linear-gradient(135deg, #8b5cf6, #7c3aed)'};
        color: white;
        font-size: 13px;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        z-index: 1000;
        animation: slideUp 0.3s ease, fadeOut 0.3s ease 2.7s;
    `;

    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Add notification animation styles
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideUp {
        from { opacity: 0; transform: translateX(-50%) translateY(20px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    .drag-over {
        background: rgba(139, 92, 246, 0.1) !important;
        border: 2px dashed var(--accent-purple) !important;
    }
    .dragging {
        opacity: 0.5;
    }
`;
document.head.appendChild(notificationStyle);

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initStudio);
