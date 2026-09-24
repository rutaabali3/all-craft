/**
 * Shared utility for logging a standardized website welcome message to the browser console.
 * @param {string} craftName - The name of the craft website (e.g., 'FilesCraft')
 * @param {string} [email] - The contact email address (defaults to info@<craftName>.com)
 * @param {string} [teamName] - The team name (defaults to craftName)
 */
function logWelcomeMessage(craftName, email, teamName = craftName) {
    const contactEmail = email || `info@${craftName.toLowerCase()}.com`;
    console.log(`
🎨 Welcome to ${craftName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${contactEmail}

Made with ❤️ by the ${teamName} team
`);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { logWelcomeMessage };
}
