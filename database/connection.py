"""Supabase client connection."""

import streamlit as st
from supabase import Client, create_client


class DatabaseError(Exception):
    """Raised when a database operation fails."""


@st.cache_resource
def get_supabase_client() -> Client:
    """Create and cache the Supabase client."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError) as exc:
        raise DatabaseError(
            "Database not configured. Add SUPABASE_URL and SUPABASE_KEY to "
            ".streamlit/secrets.toml or Streamlit Cloud secrets."
        ) from exc

    return create_client(url, key)
