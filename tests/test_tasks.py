from databases import Database
from social_media_app.database import database, post_table
import httpx
import pytest

from social_media_app.tasks import APIResponseError, send_simple_email , _generate_cute_creature_image_api , generate_and_add_to_post


@pytest.mark.anyio
async def test_mocked_async_client(mock_httpx_client):
    await send_simple_email("test@example.com", "Test Subject", "Test Body")
    mock_httpx_client.post.assert_called()


@pytest.mark.anyio
async def test_send_simple_email_api_error(mock_httpx_client):
    mock_httpx_client.post.return_value = httpx.Response(
        status_code=500, content="", request=httpx.Request("POST", "//")
    )
    with pytest.raises(APIResponseError):
        await send_simple_email("test@example.com", "Test Subject", "Test Body")


@pytest.mark.anyio
async def test_generate_cute_creature_image_api_success(mock_httpx_client):
    mock_httpx_client.post.return_value = httpx.Response(
        status_code=200,
        json={"output_url": "https://example.com/image.jpg"},
        request=httpx.Request("POST", "//"),
    )
    result = await _generate_cute_creature_image_api("A blue cat")
    assert result == {"output_url": "https://example.com/image.jpg"}


@pytest.mark.anyio
async def test_generate_cute_creature_image_api_server_error(mock_httpx_client):
    mock_httpx_client.post.return_value = httpx.Response(
        status_code=500, content="", request=httpx.Request("POST", "//")
    )
    with pytest.raises(APIResponseError):
        await _generate_cute_creature_image_api("A blue cat")


@pytest.mark.anyio
async def test_generate_cute_creature_image_api_json_error(mock_httpx_client):
    mock_httpx_client.post.return_value = httpx.Response(
        status_code=200, content="Not a JSON", request=httpx.Request("POST", "//")
    )
    with pytest.raises(APIResponseError):
        await _generate_cute_creature_image_api("A blue cat")

@pytest.mark.anyio
async def test_generate_and_add_to_post_success(
    mock_httpx_client, created_post: dict, confirmed_user: dict ,db : Database
):

    json_data={"output_url": "https://example.com/image.jpg"}
    mock_httpx_client.post.return_value=httpx.Response(
        status_code=200,
        json=json_data,
        request=httpx.Request("POST", "//"),
    )
    await generate_and_add_to_post(confirmed_user["email"],created_post["id"],"/post/1/",db,"A cat")
    query = post_table.select().where(post_table.c.id == created_post["id"])

    updated_post = await db.fetch_one(query)
    assert updated_post.image_url == json_data["output_url"]