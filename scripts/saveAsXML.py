import mujoco
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.join(script_dir, '..')

urdf_path = os.path.join(repo_root, 'tracer.urdf')
xml_path = os.path.join(repo_root, 'tracer.xml')

m = mujoco.MjModel.from_xml_path(urdf_path)
mujoco.mj_saveLastXML(xml_path, m)
print(f"Saved MJCF to {xml_path}")