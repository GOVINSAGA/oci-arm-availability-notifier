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


def check_arm_shapes():
    try:
        compute_client = oci.core.ComputeClient(OCI_CONFIG)

        shapes = compute_client.list_shapes(
            compartment_id=OCI_CONFIG["compartment_id"]
        )

        arm_shapes = []

        for shape in shapes.data:
            if "A1.Flex" in shape.shape:
                arm_shapes.append({
                    "shape": shape.shape,
                    "ocpus": shape.ocpus,
                    "memory": shape.memory_in_gbs
                })

        return {
            "success": True,
            "arm_shapes_found": len(arm_shapes),
            "shapes": arm_shapes
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }