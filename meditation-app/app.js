/**
 * Mindvalley Meditation App - JavaScript
 * ============================================
 */

// DOM Elements
const djPlayer = document.getElementById('djPlayer');
const mixerToggle = document.getElementById('mixerToggle');
const djMixerPanel = document.getElementById('djMixerPanel');
const closeMixer = document.getElementById('closeMixer');

// State
let isPlaying = false;
let isMixerOpen = false;
let currentMeditation = {
    title: 'Connecting with Your Intuition',
    author: 'Visavi Kumar',
    duration: 720, // seconds
    currentTime: 154,
    type: 'voice', // voice, sound, or mixed
    image: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=60&h=60&fit=crop'
};

// DJ Mixer State
let mixerSettings = {
    voiceVolume: 80,
    soundVolume: 40,
    selectedSound: null
};

/**
 * Initialize the application
 */
function init() {
    setupEventListeners();
    initializeSliders();
    updateProgressBar();
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Mixer toggle
    mixerToggle?.addEventListener('click', toggleMixer);
    closeMixer?.addEventListener('click', toggleMixer);

    // Play/Pause button
    const playPauseBtn = document.querySelector('.play-pause');
    playPauseBtn?.addEventListener('click', togglePlayPause);

    // Progress bar interaction
    const progressBar = document.querySelector('.progress-bar');
    progressBar?.addEventListener('click', seekTo);

    // Card play buttons
    document.querySelectorAll('.meditation-card .play-btn, .sound-card .play-btn, .horizontal-card .play-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            handleCardPlay(e);
        });
    });

    // Card click handlers
    document.querySelectorAll('.meditation-card, .sound-card, .horizontal-card, .author-card, .topic-card, .growth-card, .practice-card').forEach(card => {
        card.addEventListener('click', handleCardClick);
    });

    // Navigation arrows
    document.querySelectorAll('.nav-arrow:not(:disabled)').forEach(arrow => {
        arrow.addEventListener('click', handleNavigation);
    });

    // Sidebar items
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.addEventListener('click', handleSidebarClick);
    });

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', handlePresetClick);
    });

    // Volume controls
    const volumeSlider = document.querySelector('.volume-slider');
    volumeSlider?.addEventListener('click', handleVolumeChange);

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboard);
}

/**
 * Toggle DJ Mixer panel
 */
function toggleMixer() {
    isMixerOpen = !isMixerOpen;
    djMixerPanel?.classList.toggle('active', isMixerOpen);
    mixerToggle?.classList.toggle('active', isMixerOpen);
}

/**
 * Toggle play/pause
 */
function togglePlayPause() {
    isPlaying = !isPlaying;
    const playPauseBtn = document.querySelector('.play-pause');

    if (isPlaying) {
        playPauseBtn.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <rect x="6" y="4" width="4" height="16"/>
                <rect x="14" y="4" width="4" height="16"/>
            </svg>
        `;
        startProgressUpdate();
    } else {
        playPauseBtn.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
        `;
        stopProgressUpdate();
    }
}

/**
 * Progress update interval
 */
let progressInterval = null;

function startProgressUpdate() {
    progressInterval = setInterval(() => {
        if (currentMeditation.currentTime < currentMeditation.duration) {
            currentMeditation.currentTime++;
            updateProgressBar();
        } else {
            stopProgressUpdate();
            isPlaying = false;
            togglePlayPause();
        }
    }, 1000);
}

function stopProgressUpdate() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
}

/**
 * Update progress bar display
 */
function updateProgressBar() {
    const progress = (currentMeditation.currentTime / currentMeditation.duration) * 100;
    const progressFill = document.querySelector('.progress-fill');
    const currentTimeEl = document.querySelector('.time-current');
    const totalTimeEl = document.querySelector('.time-total');

    if (progressFill) {
        progressFill.style.width = `${progress}%`;
    }

    if (currentTimeEl) {
        currentTimeEl.textContent = formatTime(currentMeditation.currentTime);
    }

    if (totalTimeEl) {
        totalTimeEl.textContent = formatTime(currentMeditation.duration);
    }
}

/**
 * Format seconds to MM:SS
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Seek to position in track
 */
function seekTo(e) {
    const progressBar = e.currentTarget;
    const rect = progressBar.getBoundingClientRect();
    const clickPosition = (e.clientX - rect.left) / rect.width;
    currentMeditation.currentTime = Math.floor(clickPosition * currentMeditation.duration);
    updateProgressBar();
}

/**
 * Handle card play button click
 */
function handleCardPlay(e) {
    const card = e.target.closest('.meditation-card, .sound-card, .horizontal-card');
    if (!card) return;

    // Update now playing info
    const title = card.querySelector('.card-title, h4')?.textContent || 'Unknown';
    const author = card.querySelector('.author')?.textContent || 'Unknown Artist';
    const image = card.querySelector('.card-image img, .horizontal-card-image img, .sound-card-image')?.src || currentMeditation.image;

    currentMeditation.title = title;
    currentMeditation.author = author;
    currentMeditation.currentTime = 0;
    currentMeditation.duration = Math.floor(Math.random() * 600) + 300; // Random duration 5-15 min

    // Update player UI
    updateNowPlaying();
    updateProgressBar();

    // Start playing
    if (!isPlaying) {
        togglePlayPause();
    }

    // Show notification
    showNotification(`Now playing: ${title}`);
}

/**
 * Update now playing section
 */
function updateNowPlaying() {
    const titleEl = document.querySelector('.now-playing-title');
    const authorEl = document.querySelector('.now-playing-author');

    if (titleEl) titleEl.textContent = currentMeditation.title;
    if (authorEl) authorEl.textContent = currentMeditation.author;
}

/**
 * Handle card click (navigation)
 */
function handleCardClick(e) {
    // Don't navigate if clicking play button
    if (e.target.closest('.play-btn')) return;

    const card = e.currentTarget;
    const title = card.querySelector('.card-title, h4, h3')?.textContent || 'Unknown';

    // In a real app, this would navigate to the detail page
    console.log(`Navigating to: ${title}`);
    showNotification(`Opening: ${title}`);
}

/**
 * Handle carousel navigation
 */
function handleNavigation(e) {
    const section = e.target.closest('.content-section');
    const cardsRow = section?.querySelector('.cards-row, .horizontal-cards-grid, .practice-grid');

    if (!cardsRow) return;

    const isNext = e.target.closest('.nav-arrow')?.querySelector('polyline[points="9 18 15 12 9 6"]');
    const scrollAmount = 300;

    cardsRow.scrollBy({
        left: isNext ? scrollAmount : -scrollAmount,
        behavior: 'smooth'
    });
}

/**
 * Handle sidebar navigation
 */
function handleSidebarClick(e) {
    e.preventDefault();

    // Update active state
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    e.currentTarget.classList.add('active');

    // Get label
    const label = e.currentTarget.querySelector('span:not(.category-dot)')?.textContent;

    // In a real app, this would filter/navigate
    showNotification(`Viewing: ${label}`);
}

/**
 * Handle preset button click
 */
function handlePresetClick(e) {
    const preset = e.target.textContent;

    // Update active state
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.style.background = 'rgba(255, 255, 255, 0.1)';
    });
    e.target.style.background = 'var(--primary-purple)';

    // Apply preset settings
    switch (preset) {
        case 'Deep Focus':
            mixerSettings.voiceVolume = 70;
            mixerSettings.soundVolume = 30;
            break;
        case 'Sleep Mode':
            mixerSettings.voiceVolume = 50;
            mixerSettings.soundVolume = 70;
            break;
        case 'Energize':
            mixerSettings.voiceVolume = 90;
            mixerSettings.soundVolume = 50;
            break;
        case 'Relaxation':
            mixerSettings.voiceVolume = 60;
            mixerSettings.soundVolume = 60;
            break;
    }

    // Update sliders
    updateMixerSliders();
    showNotification(`Applied preset: ${preset}`);
}

/**
 * Update mixer sliders to reflect settings
 */
function updateMixerSliders() {
    const sliders = document.querySelectorAll('.track-volume .slider');
    if (sliders[0]) sliders[0].value = mixerSettings.voiceVolume;
    if (sliders[1]) sliders[1].value = mixerSettings.soundVolume;
}

/**
 * Initialize volume sliders
 */
function initializeSliders() {
    const sliders = document.querySelectorAll('.track-volume .slider');

    sliders.forEach((slider, index) => {
        slider.addEventListener('input', (e) => {
            const value = e.target.value;
            if (index === 0) {
                mixerSettings.voiceVolume = value;
            } else {
                mixerSettings.soundVolume = value;
            }
        });
    });
}

/**
 * Handle volume change
 */
function handleVolumeChange(e) {
    const slider = e.currentTarget;
    const rect = slider.getBoundingClientRect();
    const clickPosition = (e.clientX - rect.left) / rect.width;
    const volume = Math.floor(clickPosition * 100);

    const volumeFill = slider.querySelector('.volume-fill');
    if (volumeFill) {
        volumeFill.style.width = `${volume}%`;
    }
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboard(e) {
    // Space to play/pause
    if (e.code === 'Space' && !e.target.matches('input, textarea')) {
        e.preventDefault();
        togglePlayPause();
    }

    // M to toggle mixer
    if (e.code === 'KeyM' && !e.target.matches('input, textarea')) {
        e.preventDefault();
        toggleMixer();
    }

    // Arrow keys for seeking
    if (e.code === 'ArrowRight' && !e.target.matches('input, textarea')) {
        currentMeditation.currentTime = Math.min(
            currentMeditation.currentTime + 10,
            currentMeditation.duration
        );
        updateProgressBar();
    }

    if (e.code === 'ArrowLeft' && !e.target.matches('input, textarea')) {
        currentMeditation.currentTime = Math.max(currentMeditation.currentTime - 10, 0);
        updateProgressBar();
    }
}

/**
 * Show notification toast
 */
function showNotification(message) {
    // Remove existing notification
    const existing = document.querySelector('.notification-toast');
    if (existing) existing.remove();

    // Create notification
    const notification = document.createElement('div');
    notification.className = 'notification-toast';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 100px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--text-primary);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 300;
        animation: slideUp 0.3s ease, fadeOut 0.3s ease 2.7s;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(notification);

    // Remove after animation
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);

/**
 * Meditation Data Store
 * In a real app, this would come from an API
 */
const meditationData = {
    featured: [
        {
            id: 1,
            title: 'Connecting with Your Intuition to Spark Creativity',
            author: 'Visavi Kumar',
            duration: 720,
            rating: 4.9,
            type: 'voice',
            category: 'visualization',
            growthArea: 'intuition'
        },
        {
            id: 2,
            title: 'Removing Inner Blocks to Success',
            author: 'Marisa Peer',
            duration: 1080,
            rating: 4.8,
            type: 'voice',
            category: 'hypnotherapy',
            growthArea: 'manifesting'
        },
        {
            id: 3,
            title: 'Hypnotic Trance Getting Motivated',
            author: 'Paul McKenna',
            duration: 480,
            rating: 5.0,
            type: 'voice',
            category: 'hypnotherapy',
            growthArea: 'confidence'
        },
        {
            id: 4,
            title: 'Deep Healing & Repair',
            author: 'Summer McStravick',
            duration: 1500,
            rating: 4.7,
            type: 'mixed',
            category: 'sound-healing',
            growthArea: 'longevity'
        }
    ],
    voiceCategories: [
        'hypnotherapy',
        'sound-healing',
        'affirmations',
        'meditation',
        'creative-visualization'
    ],
    soundCategories: [
        'altered-state',
        'binaural-focus',
        'sleep'
    ],
    growthAreas: [
        'better-grades',
        'manifesting',
        'longevity',
        'abundance-mindset',
        'intuition',
        'creativity',
        'relationships',
        'confidence'
    ],
    authors: [
        { name: 'Marie Diamond', specialty: 'Feng Shui', tracks: 16 },
        { name: 'Paul McKenna', specialty: 'Hypnotherapy', tracks: 24 },
        { name: 'Niraj Naik', specialty: 'Breathwork', tracks: 18 },
        { name: 'Marisa Peer', specialty: 'RTT', tracks: 32 },
        { name: 'Vishen Lakhiani', specialty: 'Meditation', tracks: 12 },
        { name: 'Jeffrey Allen', specialty: 'Energy Work', tracks: 20 }
    ]
};

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { meditationData, currentMeditation, mixerSettings };
}
