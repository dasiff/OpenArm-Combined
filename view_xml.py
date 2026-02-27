import mujoco
import mujoco.viewer
import time
import sys

xml_path = sys.argv[1] if len(sys.argv) > 1 else "Tracer.xml"
model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)