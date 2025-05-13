from behave import given, when, then
import httpx
import anyio

BASE_URL = "http://localhost:8000/users"

@given("the API is running")
def step_impl(context):
    pass  # Assume app is running

@when('I request users with page {page} and page size {size}')
def step_impl(context, page, size):
    async def async_call():
        async with httpx.AsyncClient() as client:
            return await client.get(f"{BASE_URL}/?page={page}&page_size={size}")

    context.response = anyio.run(async_call)

@then('the response status code should be {code:d}')
def step_impl(context, code):
    assert context.response.status_code == code

@then("the response should contain pagination keys")
def step_impl(context):
    data = context.response.json()
    assert all(k in data for k in ["users", "total", "page", "page_size"])

@then('the response should mention "{field}"')
def step_impl(context, field):
    data = context.response.json()
    assert "detail" in data
    assert any(field in str(e.get("loc", [])) for e in data["detail"])
