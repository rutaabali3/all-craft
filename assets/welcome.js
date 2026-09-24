/**
 * Logs a standardized welcome message to the browser console.
 * @param {string} craftName - Name of the craft project (e.g. 'PencilBoxesCraft')
 * @param {string} [contactEmail] - Contact email for the craft project
 */
function logWelcomeMessage(craftName, contactEmail) {
    const email = contactEmail || `info@${craftName.toLowerCase().replace(/\s+/g, '')}.com`;
    console.log(`
🎨 Welcome to ${craftName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${email}

Made with ❤️ by the ${craftName} team
`);
}
