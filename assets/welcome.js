/**
 * Logs a standardized welcome message to the console for Craft websites.
 *
 * @param {string} craftName - The name of the craft website (e.g. "StencilsCraft").
 * @param {string} [contactEmail] - Optional contact email address. If omitted, defaults to info@<kebab-case-craftName>.com.
 */
function logWelcomeMessage(craftName, contactEmail) {
    if (!contactEmail) {
        // Convert craft name to kebab-case for default email
        const slug = craftName
            .replace(/([a-z])([A-Z])/g, '$1-$2')
            .replace(/[\s_]+/g, '-')
            .toLowerCase();
        contactEmail = `info@${slug}.com`;
    }

    console.log(`
🎨 Welcome to ${craftName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${contactEmail}

Made with ❤️ by the ${craftName} team
`);
}
