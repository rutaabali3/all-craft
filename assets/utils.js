/**
 * Logs a welcome message for Craft websites in the console.
 * @param {string} craftName - Name of the craft site (e.g. 'DocumentWalletsCraft')
 * @param {string} [email] - Contact email address (e.g. 'info@document-wallets-craft.com')
 */
function logWelcomeMessage(craftName, email) {
    const contactEmail = email || `info@${craftName.toLowerCase()}.com`;
    console.log(`
🎨 Welcome to ${craftName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${contactEmail}

Made with ❤️ by the ${craftName} team
`);
}
