from flask import (
    Flask,
    render_template,
    request,
    send_file,
    flash,
    redirect,
    url_for,
    jsonify,
)
from src import app
import subprocess
import imagekitio
import logging
import os
import subprocess
import uuid
import psutil
from src.utils import pybullet_simulation, recreate


# Create an ImageKit object
imagekit = imagekitio.ImageKit(
    private_key=app.config["PRIVATE_KEY"],
    public_key=app.config["PUBLIC_KEY"],
    url_endpoint=app.config["URL"],
)

def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Print child PIDs before terminating
        logging.error("Child PIDs:")
        for child in children:
            logging.error(child.pid)
            os.kill(child.pid,15)
            
        # for child in children:
        #     child.terminate()  # Terminate child processes

        psutil.wait_procs(children, timeout=5)  # Wait for child processes to terminate

        parent.terminate()  # Terminate the parent process
        parent.wait(5)  # Wait for the parent process to terminate
    except psutil.NoSuchProcess:
        pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/examples", methods = ["GET"])
def render_examples():
    return render_template("examples.html")

@app.route("/textbox", methods = ["GET"])
def render_box():
    return render_template("textobox.html")



@app.route("/generate_video", methods=["POST", "GET"])
def generate_video():
    
    
    # Start the tdw port 
    
    # Set the command to run
    command = "DISPLAY=:0 ./TDW.x86_64 -port=1071 -force-glcore42"
    # Set the working directory
    working_directory = os.path.expanduser("~/tdw_build/TDW")
    # Run the command in the background
    process = subprocess.Popen(command, shell=True, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Get the PID of the process
    pid = process.pid
    # Print the PID
    logging.error(f"TDW Process PID: {pid}")
    
    

    video_url = None
    # unique id for request
    uuid_string = str(uuid.uuid4())
    json_data = request.get_json()
    logging.error(f"JSON= {json_data}")

    output_filename = pybullet_simulation.simulate(json_data, uuid_string)

    recreate.render(output_filename, uuid_string)
    video_path = f"src/static/output_{uuid_string}.mp4"

    try:
        # Upload the video to ImageKit.io
        with open(video_path, "rb") as video_file:
            response = imagekit.upload_file(file=video_file, file_name="output.mp4")
            video_url = response.url
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        flash(f"Error: {str(e)}")

    os.remove(output_filename)
    os.remove(video_path)
    
    # Destroy the existing port! 
    kill_process_tree(pid)
        
    return jsonify({"video_url": video_url})


if __name__ == "__main__":
    app.run(debug=True)
