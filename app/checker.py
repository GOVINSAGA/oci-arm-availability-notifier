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
                memory_in_gbs=1
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

        compute_client.launch_instance(launch_details)

        return {
            "available": True
        }

    except Exception as e:
        error_text = str(e)

        if "Out of host capacity" in error_text:
            return {
                "available": False,
                "reason": "OUT_OF_CAPACITY"
            }

        if "TooManyRequests" in error_text:
            return {
                "available": False,
                "reason": "RATE_LIMITED"
            }

        if "NameResolutionError" in error_text:
            return {
                "available": False,
                "reason": "NETWORK_ERROR"
            }

        return {
            "available": False,
            "reason": "UNKNOWN_ERROR",
            "error": error_text
        }


def load_ssh_public_key():
    with open(OCI_CONFIG["ssh_public_key_path"], "r") as f:
        return f.read()


def auto_create_arm_instance():
    try:
        compute_client = oci.core.ComputeClient(OCI_CONFIG)

        ssh_key = load_ssh_public_key()

        launch_details = oci.core.models.LaunchInstanceDetails(
            compartment_id=OCI_CONFIG["compartment_id"],
            availability_domain=OCI_CONFIG["availability_domain"],
            shape="VM.Standard.A1.Flex",
            display_name=OCI_CONFIG["instance_name"],
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=1,
                memory_in_gbs=1
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=OCI_CONFIG["subnet_id"],
                assign_public_ip=True
            ),
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=OCI_CONFIG["image_id"]
            ),
            metadata={
                "ssh_authorized_keys": ssh_key
            }
        )

        response = compute_client.launch_instance(launch_details)

        return {
            "created": True,
            "instance_id": response.data.id,
            "display_name": response.data.display_name,
            "state": response.data.lifecycle_state
        }

    except Exception as e:
        error_text = str(e)

        if "Out of host capacity" in error_text:
            return {
                "created": False,
                "reason": "OUT_OF_CAPACITY"
            }

        if "TooManyRequests" in error_text:
            return {
                "created": False,
                "reason": "RATE_LIMITED"
            }

        if "NameResolutionError" in error_text:
            return {
                "created": False,
                "reason": "NETWORK_ERROR"
            }

        return {
            "created": False,
            "reason": "UNKNOWN_ERROR",
            "error": error_text
        }