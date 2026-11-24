from playwright.sync_api import Page, expect


def test_add_item_to_cart_from_inventory(page: Page):
    # Open the demo store login page and sign in with standard credentials
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Confirm navigation to the inventory page using a web-first URL assertion
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # Locate the specific product card by visible text before clicking its Add button
    backpack_card = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    backpack_card.get_by_role("button", name="Add to cart").click()

    # Verify the button flips to Remove and the cart badge updates to 1
    expect(backpack_card.get_by_role("button", name="Remove")).to_be_visible()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")


def test_sort_inventory_price_low_to_high(page: Page):
    # Log in to reach the inventory catalog
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # Select "Price (low to high)" from the sort dropdown
    sort_dropdown = page.locator(".product_sort_container")
    sort_dropdown.select_option("lohi")

    # Extract displayed price strings (e.g., "$7.99"), strip "$", and convert to floats
    price_texts = page.locator(".inventory_item_price").all_inner_texts()
    prices = [float(price.replace("$", "").strip()) for price in price_texts]

    # Verify prices are sorted in ascending order and match the expected lowest price
    assert len(prices) > 0
    assert prices == sorted(prices)
    assert prices[0] == 7.99


def test_mock_network_response_in_ui(page: Page):
    # Intercept matching API/data requests and return a controlled JSON response
    page.route(
        "**/api/v1/inventory-status",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"maintenanceMode": false, "featuredLabel": "Sydney Pick"}',
        ),
    )

    # Navigate to the target page after registering the route handler
    page.goto("https://www.saucedemo.com/")
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    # Remove the route handler when done so later tests on the same page are unaffected
    page.unroute("**/api/v1/inventory-status")