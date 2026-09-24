/**
 * Shared utility functions for Craft websites.
 */

/**
 * Logs a standardized console welcome message for Craft websites.
 * @param {string|object} options - Site name string or configuration object.
 * @param {string} [email] - Contact email address (if first parameter is a string).
 * @param {string} [team] - Team name (if first parameter is a string, defaults to siteName).
 */
function logConsoleWelcome(options, email, team) {
  let siteName, contactEmail, teamName;
  if (typeof options === 'object' && options !== null) {
    siteName = options.siteName;
    contactEmail = options.contactEmail;
    teamName = options.teamName || siteName;
  } else {
    siteName = options;
    contactEmail = email;
    teamName = team || siteName;
  }

  console.log(`
🎨 Welcome to ${siteName} Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: ${contactEmail}

Made with ❤️ by the ${teamName} team
`);
}
