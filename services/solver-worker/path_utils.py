import os


def get_static_images_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "static", "images")


def build_asset_path(*parts):
    normalized_parts = [str(part).strip("/\\") for part in parts if str(part) != ""]
    relative_path = "/".join(normalized_parts)
    public_base_url = os.getenv("PUBLIC_ASSET_BASE_URL", "").strip()
    if public_base_url:
        return f"{public_base_url.rstrip('/')}/{relative_path}"
    return f"/{relative_path}"
