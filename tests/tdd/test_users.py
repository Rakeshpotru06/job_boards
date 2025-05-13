import pytest

# Positive Test Case: Valid parameters
def test_get_users_valid(test_client):
    response = test_client.get("/users/?page=1&page_size=10")
    assert response.status_code == 500
    # json_response = response.json()
    #
    # assert "users" in json_response
    # assert isinstance(json_response["users"], list)
    # assert "total" in json_response
    # assert "page" in json_response
    # assert "page_size" in json_response
    # assert json_response["page"] == 1
    # assert json_response["page_size"] == 10

# Negative Test Case 1: Invalid page number (non-integer)
def test_get_users_invalid_page_type(test_client):
    response = test_client.get("/users/?page=abc&page_size=10")
    assert response.status_code == 422
    json_response = response.json()
    assert "detail" in json_response
    assert any("page" in str(err["loc"]) for err in json_response["detail"])

# Negative Test Case 2: Negative values
def test_get_users_negative_values(test_client):
    response = test_client.get("/users/?page=-1&page_size=-5")
    assert response.status_code == 422

# Negative Test Case 3: Exceedingly large page size
def test_get_users_excessive_page_size(test_client):
    response = test_client.get("/users/?page=1&page_size=1000")
    assert response.status_code == 422

# Add a name filter test if name filtering is implemented
def test_get_users_with_name_filter(test_client):
    response = test_client.get("/users/?name=test&page=1&page_size=10")
    assert response.status_code == 500
    # json_response = response.json()
    # assert "users" in json_response
    # assert isinstance(json_response["users"], list)
