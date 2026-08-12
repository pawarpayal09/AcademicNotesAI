import os
import requests
import streamlit as st
from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# YOUTUBE API CONFIGURATION
# ==========================================================

YOUTUBE_API_URL = (
    "https://www.googleapis.com/youtube/v3/search"
)


# ==========================================================
# GET YOUTUBE API KEY
# ==========================================================

def get_youtube_api_key():

    # ------------------------------------------------------
    # Streamlit Cloud / deployed application
    # ------------------------------------------------------

    try:

        api_key = st.secrets.get(
            "YOUTUBE_DATA_API_KEY"
        )

    except Exception:

        api_key = None


    # ------------------------------------------------------
    # Local .env
    # ------------------------------------------------------

    if not api_key:

        api_key = os.getenv(
            "YOUTUBE_DATA_API_KEY"
        )


    # ------------------------------------------------------
    # Clean whitespace
    # ------------------------------------------------------

    if api_key:

        api_key = api_key.strip()


    return api_key


# ==========================================================
# SEARCH YOUTUBE VIDEOS
# ==========================================================

@st.cache_data(
    ttl=900,
    show_spinner=False
)
def search_youtube_videos(
    query,
    max_results=6
):

    """
    Search public YouTube videos.

    Results are cached for 15 minutes so repeated searches
    do not unnecessarily consume YouTube API quota.
    """

    api_key = get_youtube_api_key()


    # ------------------------------------------------------
    # Validate API key
    # ------------------------------------------------------

    if not api_key:

        return {
            "success": False,
            "error": (
                "YOUTUBE_DATA_API_KEY is not configured."
            ),
            "videos": []
        }


    # ------------------------------------------------------
    # Validate query
    # ------------------------------------------------------

    query = query.strip()

    if not query:

        return {
            "success": False,
            "error": "Please enter a topic to search.",
            "videos": []
        }


    # ------------------------------------------------------
    # Keep result count safe
    # ------------------------------------------------------

    max_results = max(
        1,
        min(
            int(max_results),
            10
        )
    )


    # ------------------------------------------------------
    # API parameters
    # ------------------------------------------------------

    params = {

        "part": "snippet",

        "q": query,

        "type": "video",

        "maxResults": max_results,

        "order": "relevance",

        "regionCode": "IN",

        "relevanceLanguage": "en",

        "safeSearch": "strict",

        "key": api_key
    }


    try:

        # --------------------------------------------------
        # API request
        # --------------------------------------------------

        response = requests.get(
            YOUTUBE_API_URL,
            params=params,
            timeout=15
        )


        # --------------------------------------------------
        # Parse response
        # --------------------------------------------------

        try:

            data = response.json()

        except ValueError:

            return {
                "success": False,
                "error": (
                    "YouTube returned an invalid response."
                ),
                "videos": []
            }


        # --------------------------------------------------
        # Handle API errors
        # --------------------------------------------------

        if response.status_code != 200:

            error_data = data.get(
                "error",
                {}
            )

            error_message = (
                error_data
                .get("message")
                or
                "YouTube API request failed."
            )

            return {
                "success": False,
                "error": (
                    f"YouTube API error "
                    f"({response.status_code}): "
                    f"{error_message}"
                ),
                "videos": []
            }


        # --------------------------------------------------
        # Extract videos
        # --------------------------------------------------

        videos = []


        for item in data.get(
            "items",
            []
        ):

            video_id = (
                item
                .get("id", {})
                .get("videoId")
            )


            snippet = item.get(
                "snippet",
                {}
            )


            if not video_id:
                continue


            # ------------------------------------------------
            # Thumbnail selection
            # ------------------------------------------------

            thumbnails = snippet.get(
                "thumbnails",
                {}
            )


            thumbnail = ""

            if thumbnails.get("high"):

                thumbnail = (
                    thumbnails["high"]
                    .get("url", "")
                )

            elif thumbnails.get("medium"):

                thumbnail = (
                    thumbnails["medium"]
                    .get("url", "")
                )

            elif thumbnails.get("default"):

                thumbnail = (
                    thumbnails["default"]
                    .get("url", "")
                )


            # ------------------------------------------------
            # Description
            # ------------------------------------------------

            description = snippet.get(
                "description",
                ""
            )


            if len(description) > 180:

                description = (
                    description[:180]
                    + "..."
                )


            # ------------------------------------------------
            # Build video object
            # ------------------------------------------------

            videos.append(
                {
                    "video_id": video_id,

                    "title": snippet.get(
                        "title",
                        "Untitled Video"
                    ),

                    "description": description,

                    "channel": snippet.get(
                        "channelTitle",
                        "Unknown Channel"
                    ),

                    "published_at": snippet.get(
                        "publishedAt",
                        ""
                    ),

                    "thumbnail": thumbnail,

                    "url": (
                        "https://www.youtube.com/watch?v="
                        + video_id
                    )
                }
            )


        # --------------------------------------------------
        # Successful response
        # --------------------------------------------------

        return {
            "success": True,
            "error": None,
            "videos": videos
        }


    except requests.Timeout:

        return {
            "success": False,
            "error": (
                "YouTube request timed out. "
                "Please try again."
            ),
            "videos": []
        }


    except requests.RequestException as e:

        return {
            "success": False,
            "error": (
                "Unable to connect to YouTube.\n\n"
                f"{str(e)}"
            ),
            "videos": []
        }


    except Exception as e:

        return {
            "success": False,
            "error": (
                "Unexpected YouTube error.\n\n"
                f"{str(e)}"
            ),
            "videos": []
        }