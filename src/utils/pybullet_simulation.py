import pybullet as p
import pybullet_data
import random
import json

# Define RGB values for red, blue, and green
red_rgb = (1, 0, 0)
blue_rgb = (0, 0, 1)
green_rgb = (0, 1, 0)


def simulate(objects, uuid_string):
    # Initialize PyBullet in direct mode (headless)
    p.connect(p.DIRECT)

    # Set up the PyBullet simulation
    p.setGravity(0, -9.81, 0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # # Create a list of objects in JSON format with type, shape, color, acceleration, and material
    # objects = [
    #     {
    #         "type": "static",
    #         "shape": "sphere",
    #         "color": "purple",
    #         "acceleration": 0,
    #         "material": "cardboard_paper",
    #     },
    #     {
    #         "type": "static",
    #         "shape": "sphere",
    #         "color": "purple",
    #         "acceleration": 0,
    #         "material": "aluminium_clean",
    #     },
    #     {
    #         "type": "static",
    #         "shape": "cube",
    #         "color": "purple",
    #         "acceleration": 0,
    #         "material": "cardboard_paper",
    #     },
    #     {
    #         "type": "static",
    #         "shape": "cube",
    #         "color": "teal",
    #         "acceleration": 0,
    #         "material": "cardboard_paper",
    #     },
    #     {
    #         "type": "static",
    #         "shape": "cube",
    #         "color": "purple",
    #         "acceleration": 0,
    #         "material": "aluminium_clean",
    #     },
    #     {
    #         "type": "static",
    #         "shape": "cube",
    #         "color": "teal",
    #         "acceleration": 0,
    #         "material": "aluminium_clean",
    #     },
    #     {
    #         "type": "dynamic",
    #         "shape": "cube",
    #         "color": "yellow",
    #         "acceleration": 14,
    #         "material": "cardboard_paper",
    #     },
    #     {
    #         "type": "dynamic",
    #         "shape": "sphere",
    #         "color": "yellow",
    #         "acceleration": 14,
    #         "material": "aluminium_clean",
    #     },
    # ]

    # Initialize the JSON output structure
    output_json = {
        "total_objects": len(objects),
        "total_initial_moving_objects": sum(
            obj["type"] == "dynamic" for obj in objects
        ),
        "initial_static_objects": [],
        "initial_dynamic_objects": [],
        "frames": [],
    }

    # Create objects in the simulation and populate JSON data
    object_ids = []
    for idx, obj in enumerate(objects):
        # Random mass between 1 and 20 for all objects
        mass = random.uniform(1, 20)

        # Random location on the x,z plane (y=0)
        x = random.uniform(-5, 5)
        z = random.uniform(-5, 5)
        loc = {"x": x, "y": 0.0, "z": z}  # Make y a floating-point value

        # Random color (r, g, b values)
        r, g, b = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)

        # Create objects in PyBullet
        if obj["shape"] == "sphere":
            obj_id = p.createCollisionShape(p.GEOM_SPHERE, radius=1)
        elif obj["shape"] == "cube":
            obj_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1, 1, 1])
        elif obj["shape"] == "cylinder":
            obj_id = p.createCollisionShape(p.GEOM_CYLINDER, radius=1, height=2)

        if obj["color"] == "red":
            r, g, b = red_rgb
        elif obj["color"] == "blue":
            r, g, b = blue_rgb
        elif obj["color"] == "green":
            r, g, b = green_rgb

        obj_body = p.createMultiBody(mass, obj_id, -1, basePosition=loc)
        p.changeVisualShape(obj_body, -1, rgbaColor=[r, g, b, 1])

        object_ids.append(obj_body)

        # Populate JSON data for the object
        object_data = {
            "id": idx,
            "name": obj["shape"],
            "color": {"r": r, "g": g, "b": b, "a": 1},
            "material": obj["material"],
            "scale": "1",
            "loc": loc,
            "mass": mass,
        }

        if obj["type"] == "dynamic":
            # if idx == 6:  # Index 6 corresponds to the dynamic object to start after 1 second
            #     # Delay the application of force by simulating 125 frames (assuming 125 Hz)
            #     for _ in range(125):
            #         p.stepSimulation()

            # Assign a random force between -200 and 200 in the x and z directions
            force_x = random.uniform(-200, 200)
            force_z = random.uniform(-200, 200)
            p.applyExternalForce(
                obj_body, -1, [force_x, 0, force_z], [0, 0, 0], p.LINK_FRAME
            )

            # Populate JSON data for dynamic objects
            object_data["target_object_id"] = idx  # Assuming the same ID for now
            object_data["directional_force"] = {"x": force_x, "y": 0, "z": force_z}
            object_data["initial_acc"] = obj["acceleration"]

            # Record the initial dynamic object data
            output_json["initial_dynamic_objects"].append(object_data)
        else:
            # Record the initial static object data
            output_json["initial_static_objects"].append(object_data)

    # Simulate and record object states for each frame
    num_frames = 10  # Number of frames to simulate (you can adjust this)
    for frame in range(num_frames):
        frame_data = {}

        # Update the simulation for each frame
        p.stepSimulation()

        for idx, obj_id in enumerate(object_ids):
            pos, _ = p.getBasePositionAndOrientation(obj_id)
            vel, _ = p.getBaseVelocity(obj_id)
            frame_data[idx] = {"location": pos, "velocity": vel}

        output_json["frames"].append({"frame": frame, **frame_data})

    # Define the filename for saving the JSON data
    output_filename = f"src/static/simulation_data_{uuid_string}.json"

    # Save the JSON data to a file
    with open(output_filename, "w") as json_file:
        json.dump(output_json, json_file, indent=4)

    # Print a message to confirm that the data has been saved
    print(f"JSON data saved to {output_filename}")

    # Disconnect from the PyBullet simulation
    p.disconnect()

    return output_filename
