const test = require('node:test');
const assert = require('node:assert/strict');
const { addLoadingScreen } = require('../assets/utils.js');

function createMockEnvironment() {
    const eventListeners = {};
    const bodyChildren = [];
    const headChildren = [];

    const mockDocument = {
        readyState: 'loading',
        body: {
            appendChild(el) {
                bodyChildren.push(el);
                el.parentNode = mockDocument.body;
            }
        },
        head: {
            appendChild(el) {
                headChildren.push(el);
                el.parentNode = mockDocument.head;
            }
        },
        createElement(tagName) {
            const el = {
                tagName,
                id: '',
                style: {},
                innerHTML: '',
                textContent: '',
                parentNode: null,
                remove() {
                    if (el.parentNode === mockDocument.body) {
                        const idx = bodyChildren.indexOf(el);
                        if (idx !== -1) bodyChildren.splice(idx, 1);
                    }
                    if (el.parentNode === mockDocument.head) {
                        const idx = headChildren.indexOf(el);
                        if (idx !== -1) headChildren.splice(idx, 1);
                    }
                    el.parentNode = null;
                }
            };
            return el;
        },
        getElementById(id) {
            return bodyChildren.find(e => e.id === id) || headChildren.find(e => e.id === id) || null;
        }
    };

    const mockWindow = {
        addEventListener(event, handler) {
            if (!eventListeners[event]) eventListeners[event] = [];
            eventListeners[event].push(handler);
        },
        trigger(event) {
            if (eventListeners[event]) {
                eventListeners[event].forEach(h => h());
            }
        }
    };

    return { mockDocument, mockWindow, bodyChildren, headChildren };
}

test('addLoadingScreen appends loader with correct project name', () => {
    const { mockDocument, mockWindow } = createMockEnvironment();
    global.document = mockDocument;
    global.window = mockWindow;

    addLoadingScreen('WritingSetsCraft');

    const loader = mockDocument.getElementById('loader');
    assert.notEqual(loader, null);
    assert.ok(loader.innerHTML.includes('Loading WritingSetsCraft...'));

    const spinStyle = mockDocument.getElementById('spin-animation-style');
    assert.notEqual(spinStyle, null);

    delete global.document;
    delete global.window;
});

test('addLoadingScreen fades out and removes loader on load', (t, done) => {
    const { mockDocument, mockWindow, bodyChildren } = createMockEnvironment();
    global.document = mockDocument;
    global.window = mockWindow;

    addLoadingScreen('WritingSetsCraft');

    assert.equal(bodyChildren.length, 1);

    // Trigger window load event
    mockWindow.trigger('load');

    // Loader should fade out and be removed after timeouts (1000ms + 500ms)
    setTimeout(() => {
        assert.equal(bodyChildren.length, 0);
        assert.equal(mockDocument.getElementById('loader'), null);

        delete global.document;
        delete global.window;
        done();
    }, 1600);
});
