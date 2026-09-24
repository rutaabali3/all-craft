/**
 * Shared utility functions for Craft websites.
 */

/**
 * Logs a standardized welcome message for a Craft website in the developer console.
 * @param {string} craftName - Name of the craft (e.g. "StaplesCraft")
 * @param {string} [email] - Contact email address. If omitted, defaults to info@<kebab-case-craftName>.com
 */
function logWelcomeMessage(craftName, email) {
    if (!craftName) return;
    const contactEmail = email || `info@${craftName.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()}.com`;
    console.log(`
🎨 Welcome to ${craftName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${contactEmail}

Made with ❤️ by the ${craftName} team
`);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { logWelcomeMessage };
}
