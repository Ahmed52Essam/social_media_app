import logging
from json import JSONDecodeError

import httpx
from databases import Database

from social_media_app.config import config
from social_media_app.database import post_table

logger = logging.getLogger(__name__)


class APIResponseError(Exception):
    pass


async def send_simple_email(to: str, subject: str, body: str):
    logger.debug(f"Sending email to '{to[:3]}' , with subject '{subject[:20]}' ")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://api.mailgun.net/v3/{config.MAILGUN_DOMAIN}/messages",
                auth=("api", config.MAILGUN_API_KEY),
                data={
                    "from": f"Social Media App <postmaster@{config.MAILGUN_DOMAIN}>",
                    "to": f"{to} <{to}>",
                    "subject": subject,
                    "text": body,
                },
            )
            response.raise_for_status()

            logger.debug(response.content)

            return response

        except httpx.HTTPStatusError as err:
            raise APIResponseError(
                f"API request failed with status code of {err.response.status_code}"
            ) from err


async def send_user_registeration_email(email: str, confirmation_url: str):
    return await send_simple_email(
        email,
        "Successfully signed up",
        (
            f"Hi {email}! You have successfully signed up to Social Media REST API."
            " Please confirm your email by clicking on the"
            f" following link: {confirmation_url}"
        ),
    )


async def _generate_cute_creature_image_api(prompt: str):
    logger.debug(f"Generating image for prompt '{prompt[:20]}'")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.deepai.org/api/text2img",
                data={
                    "text": f"{prompt}",
                },
                headers={"api-key": config.DEEPAI_API_KEY},
            )
            logger.debug(response)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as err:
            raise APIResponseError(
                f"DeepAI API request failed with status code of {err.response.status_code}"
            ) from err
        except (JSONDecodeError, TypeError) as err:
            raise APIResponseError(
                f"API response parsing failed with error {err}"
            ) from err


async def generate_and_add_to_post(
    email: str,
    post_id: int,
    post_url: str,
    database: Database,
    prompt: str = "A blue cat is sitting on couch",
):
    try:
        response = await _generate_cute_creature_image_api(prompt)
    except APIResponseError:
        return await send_simple_email(
            email,
            "Failed to generate image",
            (
                f"Hi {email}! You have failed to generate image for post {post_url}."
                " Please try again later."
            ),
        )
    logger.debug("Connecting to database to update post")
    query = (
        post_table.update()
        .where(post_table.c.id == post_id)
        .values({"image_url": response["output_url"]})
    )
    logger.debug(query)
    await database.execute(query)
    logger.debug("Database connection in background task closed")
    return await send_simple_email(
        email,
        "Image generated successfully",
        (
            f"Hi {email}! You have successfully generated image for post {post_url}."
            " Please check your email for the image."
        ),
    )
    return response
