# OpenArm Combined

### Tracer.urdf
- The original `tracer.urdf` file only had a <visual> tag. 
- Added `<inertial>` and `<collision>` tags that include data for every link in tracer.urdf so Mujoco has valid masses/inertias and can simulate contacts.

#### `<inertial>`
- origin: places the inertial frame.
- mass: link's mass.
- inertia: 3x3 inertia tensor about the link's inertial frame.

#### `<collision>`
- Geometry used for contact and collision detection.

#### NOTE:
- All the calculations for the inertial is estimated.
- To get the best results, we need to calculate the from the real tracer.
- We need to determine:
    - Mass of each component (base, battery, each wheel, each caster, lidar)
    - Dimensions of each component (length/width/height for boxes, radius/length for cylinders).
    - Center of mass offsets if the part isn’t symmetric. If the COM is not centered, update the inertial `<origin>` accordingly.
- Another thing to note is that our urdf model only has two main components: links and joints.
    - Joints define what can move. 
    - Actuators define how we can command that motion.
        - To actually controll things like wheels of our tracer, we need to convert the mujoco to mjcf and add actuators. 

### Tracer.xml (MJCF)
- Converted from `tracer.urdf` using MuJoCo's compiler (`scripts/saveAsXML.py`), then manually restructured.
- MJCF is MuJoCo's native format. Key differences from URDF:
    - All `fixed` joints get flattened — casters, battery, lidar become plain `<geom>` shapes on the parent body.
    - `size` for boxes is **half-extents** (URDF uses full size). e.g. URDF `0.702` becomes MJCF `0.351`.
    - `size` for cylinders is `radius, half-length`. e.g. URDF `radius=0.025, length=0.03` becomes `0.025, 0.015`.
    - Only the two drive wheels (`right_wheel`, `left_wheel`) have `<body>` tags because they have non-fixed joints.

#### Half-extents
- MJCF half-extents do NOT change actual dimensions. It's just a different notation (0.351 * 2 = 0.702). The geometry is identical.
- When editing the URDF, use full sizes. When editing the MJCF directly, use half sizes.

#### `<freejoint>`
- The entire robot is wrapped in a `<body>` with a `<freejoint>` so it can move freely in 3D space.
- Without this, geoms placed directly in `<worldbody>` are static — welded to the world and can never move.

#### `<actuator>`
- Added motor actuators for the two drive wheels (`left_motor`, `right_motor`).
- `gear="10"` — torque multiplier. `ctrl=1` applies 10 N·m.
- `ctrllimited="true"` + `ctrlrange="-1 1"` — clamps control input to prevent unrealistic forces.
- Controlled in Python via `data.ctrl[0]` (left) and `data.ctrl[1]` (right). Both positive = forward, opposite signs = turn (differential drive).

#### `<contact>` 
- The wheels visually overlap into the chassis (by design from the URDF).
- Without `<exclude>`, MuJoCo detects collisions between the wheel geoms and chassis geom — wheels fight the chassis instead of gripping the ground.
- Added `<exclude body1="base_link" body2="right_wheel"/>` and same for left_wheel to fix this.

#### Other physics settings
- `timestep="0.002"` — smaller timestep for stable contact solving.
- `friction="1.5"` on drive wheels for grip, `friction="0.1"` on casters so they slide like real casters.
- `damping="0.1"` on wheel joints — prevents wheels from spinning forever.