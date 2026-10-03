/**
 * Shared utility functions for Craft projects.
 */

/**
 * Adds a loading screen overlay to the page that automatically fades out and removes itself on load.
 * @param {string} projectName - The name of the project to display on the loading screen.
 */
function addLoadingScreen(projectName) {
    if (typeof document === 'undefined') return;

    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        transition: opacity 0.5s ease-out;
    `;

    loader.innerHTML = `
        <div style="text-align: center;">
            <div style="width: 60px; height: 60px; border: 4px solid var(--gray-200); border-top: 4px solid var(--primary-color); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem;"></div>
            <h4 style="color: var(--primary-color); font-family: var(--font-display);">Loading ${projectName}...</h4>
        </div>
    `;

    if (document.body) {
        document.body.appendChild(loader);
    }

    if (!document.getElementById('spin-animation-style')) {
        const spinStyle = document.createElement('style');
        spinStyle.id = 'spin-animation-style';
        spinStyle.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        if (document.head) {
            document.head.appendChild(spinStyle);
        }
    }

    if (typeof window !== 'undefined') {
        const handleLoad = () => {
            setTimeout(() => {
                loader.style.opacity = '0';
                setTimeout(() => {
                    if (loader.parentNode) {
                        loader.remove();
                    }
                }, 500);
            }, 1000);
        };

        if (document.readyState === 'complete') {
            handleLoad();
        } else {
            window.addEventListener('load', handleLoad);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { addLoadingScreen };
}
