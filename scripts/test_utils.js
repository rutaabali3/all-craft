const assert = require('assert');
const { logWelcomeMessage } = require('../assets/utils.js');

function testLogWelcomeMessage() {
    let capturedOutput = '';
    const originalLog = console.log;
    console.log = (msg) => {
        capturedOutput += msg;
    };

    try {
        logWelcomeMessage('StaplesCraft', 'info@staples-craft.com');
        const expected = `
🎨 Welcome to StaplesCraft Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: info@staples-craft.com

Made with ❤️ by the StaplesCraft team
`;
        assert.strictEqual(capturedOutput, expected, 'Output should match exact greeting format');

        // Test fallback email generation
        capturedOutput = '';
        logWelcomeMessage('MaskingTapeCraft');
        const expectedFallback = `
🎨 Welcome to MaskingTapeCraft Website!
✨ Built with love using HTML, CSS, JavaScript & Bootstrap
🚀 Featuring smooth scrolling and animations
📧 Contact: info@masking-tape-craft.com

Made with ❤️ by the MaskingTapeCraft team
`;
        assert.strictEqual(capturedOutput, expectedFallback, 'Fallback email output should match expected format');

        console.log = originalLog;
        console.log('✅ logWelcomeMessage unit tests passed successfully!');
    } catch (err) {
        console.log = originalLog;
        console.error('❌ logWelcomeMessage unit tests failed:', err);
        process.exit(1);
    }
}

testLogWelcomeMessage();
