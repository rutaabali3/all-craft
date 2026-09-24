/**
 * Logs the standard welcome message for Craft websites.
 * @param {string} craftName - The name of the craft (e.g. "CalendarsCraft")
 * @param {string} [contactEmail] - Optional contact email address
 */
function logWelcomeMessage(craftName, contactEmail) {
    const email = contactEmail || `info@${craftName.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase()}.com`;
    console.log(`
🎨 Welcome to ${craftName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${email}

Made with ❤️ by the ${craftName} team
`);
}
