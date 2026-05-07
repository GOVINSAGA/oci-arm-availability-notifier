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
    

def check_arm_capacity():
    try:
        compute_client = oci.core.ComputeClient(OCI_CONFIG)

        launch_details = oci.core.models.LaunchInstanceDetails(
            compartment_id=OCI_CONFIG["compartment_id"],
            availability_domain=OCI_CONFIG["availability_domain"],
            shape="VM.Standard.A1.Flex",
            display_name="capacity-check-test",
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=1,
                memory_in_gbs=6
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=OCI_CONFIG["subnet_id"],
                assign_public_ip=False
            ),
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=OCI_CONFIG["image_id"]
            )
        )

        # Intentionally trigger validation
        compute_client.launch_instance(launch_details)

        return {
            "available": True
        }

    except Exception as e:
        error_text = str(e)

        if "Out of host capacity" in error_text:
            return {
                "available": False,
                "reason": "Out of capacity"
            }

        return {
            "available": False,
            "reason": error_text
        }