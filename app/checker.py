import oci

from app.config import OCI_CONFIG


def test_oci_connection():
    try:
        identity_client = oci.identity.IdentityClient(OCI_CONFIG)

        regions = identity_client.list_regions()

        return {
            "success": True,
            "region_count": len(regions.data)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }