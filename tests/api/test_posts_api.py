from playwright.sync_api import APIRequestContext, expect


def test_get_post_by_id(api_client: APIRequestContext):
    # Send a GET request to fetch a single post resource by ID
    response = api_client.get("/posts/1")

    # Verify HTTP status is in the 2xx success range and explicitly check 200 OK
    expect(response).to_be_ok()
    assert response.status == 200

    # Parse JSON response body and validate expected fields and types
    post = response.json()
    assert post["id"] == 1
    assert isinstance(post["title"], str) and len(post["title"]) > 0


def test_get_posts_with_query_params(api_client: APIRequestContext):
    # Pass query parameters (?userId=1) to filter returned posts
    response = api_client.get("/posts", params={"userId": 1})
    expect(response).to_be_ok()
    assert response.status == 200

    posts = response.json()
    # Ensure results are non-empty and every item matches the filter
    assert len(posts) > 0
    assert all(item["userId"] == 1 for item in posts)


def test_create_post_with_post_request(api_client: APIRequestContext):
    # Define the request payload to create a new post
    payload = {
        "title": "Playwright Sydney API Portfolio",
        "body": "Testing POST endpoint with APIRequestContext",
        "userId": 1,
    }

    # Send a POST request with JSON body and expect HTTP 201 Created
    response = api_client.post("/posts",data=payload)
    assert response.status == 201

    # Confirm echoed fields match the sent payload and a new ID is returned
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert "id" in created

    def test_update_post_with_put_request(api_client: APIRequestContext):
        # Define the full replacement payload for post ID 1
        updated_payload = {
            "id": 1,
            "title": "Updated Post Title via PUT",
            "body": "Full replacement body content for Sydney portfolio",
            "userId": 1,
        }

        # Send a PUT request to replace the existing resource
        response = api_client.put("/posts/1", data=updated_payload)
        expect(response).to_be_ok()
        assert response.status == 200

        # Verify the response reflects the replaced resource fields
        updated = response.json()
        assert updated["id"] == 1
        assert updated["title"] == updated_payload["title"]
        assert updated["body"] == updated_payload["body"]
        assert updated["userId"] == updated_payload["userId"]

    def test_partial_update_post_with_patch_request(api_client: APIRequestContext):
        # Define only the specific field(s) to partially update
        patch_payload = {
            "title": "Partially Updated Title via PATCH",
        }

        # Send a PATCH request to modify only the targeted field
        response = api_client.patch("/posts/1", data=patch_payload)
        expect(response).to_be_ok()
        assert response.status == 200

        # Confirm the patched title updated while existing fields remain present
        patched = response.json()
        assert patched["id"] == 1
        assert patched["title"] == patch_payload["title"]
        assert "body" in patched

    def test_delete_post_with_delete_request(api_client: APIRequestContext):
        # Send a DELETE request to remove post ID 1
        response = api_client.delete("/posts/1")

        # Verify HTTP status indicates successful deletion (200 or 204 depending on API)
        assert response.status in (200, 204)

        def test_get_nonexistent_post_returns_404(api_client: APIRequestContext):
            # Request a post ID that does not exist on the server
            response = api_client.get("/posts/999999")

            # Confirm HTTP 404 Not Found and that Playwright marks the response as not ok
            assert response.status == 404
            assert not response.ok

        def test_post_response_headers_and_content_type(api_client: APIRequestContext):
            # Fetch an existing post and inspect its HTTP response headers
            response = api_client.get("/posts/1")
            expect(response).to_be_ok()

            # Header keys are case-insensitive in HTTP; normalize to lowercase before checking
            headers = {k.lower(): v for k, v in response.headers.items()}
            assert "content-type" in headers
            assert "application/json" in headers["content-type"].lower()

            def test_post_response_schema_and_field_types(api_client: APIRequestContext):
                # Fetch a post resource and verify the request succeeded
                response = api_client.get("/posts/1")
                expect(response).to_be_ok()
                assert response.status == 200

                post = response.json()

                # Confirm the response body is a JSON object (dict) and contains all required keys
                assert isinstance(post, dict)
                expected_keys = {"id", "userId", "title", "body"}
                assert expected_keys.issubset(post.keys())

                # Validate exact field types and basic value constraints
                assert isinstance(post["id"], int) and post["id"] > 0
                assert isinstance(post["userId"], int) and post["userId"] > 0
                assert isinstance(post["title"], str) and len(post["title"].strip()) > 0
                assert isinstance(post["body"], str) and len(post["body"].strip()) > 0

    import pytest
    from playwright.sync_api import APIRequestContext, expect

    @pytest.mark.parametrize(
        "post_id, expected_user_id",
        [
            (1, 1),
            (11, 2),
            (21, 3),
        ],
    )
    def test_get_post_by_multiple_ids(
            api_client: APIRequestContext,
            post_id: int,
            expected_user_id: int,
    ):
        # Request a specific post resource by parameterized ID
        response = api_client.get(f"/posts/{post_id}")

        # Verify HTTP 200 OK response status
        expect(response).to_be_ok()
        assert response.status == 200

        # Parse JSON body and confirm both the post ID and owner userId match expected values
        post = response.json()
        assert post["id"] == post_id
        assert post["userId"] == expected_user_id
        assert isinstance(post["title"], str) and len(post["title"].strip()) > 0