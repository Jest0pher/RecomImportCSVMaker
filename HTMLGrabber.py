from playwright.sync_api import sync_playwright

def fetch_authenticated_html(url: str, username: str, password: str) -> str:
    """
    Logs into the specified simplecell page using provided credentials
    and returns the page's HTML content after logging in.
    """
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Navigate to the page
            page.goto(url, wait_until="networkidle")

            # 2. Fill in login credentials
            # Adjust selectors below if the target page uses different input names/IDs
            page.fill('input[type="email"], input[name="email"], input[name="username"]', username)
            page.fill('input[type="password"], input[name="password"]', password)

            # 3. Submit the login form
            page.click('button[type="submit"], input[type="submit"]')

            # 4. Wait for navigation/redirection after login completes
            page.wait_for_load_state("networkidle")


            page.goto(url, wait_until="networkidle")

            # 5. Capture and return the HTML content
            html_content = page.content()
            return html_content

        finally:
            browser.close()

# Example usage:
# html = fetch_authenticated_html("https://simplecell.recomapp.com", "your_user", "your_pass")
# print(html)