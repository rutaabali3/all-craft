import glob
import os
import sys

def test_welcome_utility():
    print("Running verification tests for welcome utility...")

    # 1. Check assets/welcome.js exists
    welcome_js_path = os.path.join("assets", "welcome.js")
    assert os.path.exists(welcome_js_path), "assets/welcome.js does not exist!"

    with open(welcome_js_path, "r", encoding="utf-8") as f:
        welcome_content = f.read()
    assert "function logWelcomeMessage(" in welcome_content, "assets/welcome.js missing logWelcomeMessage function!"
    print("✅ assets/welcome.js verified.")

    # 2. Check all projects HTML files include welcome.js
    html_files = sorted(glob.glob("projects/*/index.html"))
    assert len(html_files) == 163, f"Expected 163 index.html files, found {len(html_files)}"

    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert '<script src="../../assets/welcome.js"></script>' in content, f"Missing welcome.js script tag in {path}"
    print("✅ All 163 project index.html files verified.")

    # 3. Check all projects JS files call logWelcomeMessage
    js_files = sorted(glob.glob("projects/*/script.js"))
    assert len(js_files) == 163, f"Expected 163 script.js files, found {len(js_files)}"

    for path in js_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "logWelcomeMessage(" in content, f"Missing logWelcomeMessage call in {path}"
        # Ensure raw console.log for welcome message is removed
        assert "🎨 Welcome to" not in content, f"Found un-extracted welcome message in {path}"
    print("✅ All 163 project script.js files verified.")

    print("\n🎉 ALL WELCOME UTILITY TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_welcome_utility()
