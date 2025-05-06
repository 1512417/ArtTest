# Maya Normal Fixing Tool Documentation
Flipped normals during the Blender → Maya pipeline are a common issue due to differences in coordinate systems, FBX export/import settings, or mesh construction. Automating the detection and fixing of flipped normals inside Maya can drastically reduce back-and-forth between tools.

## ✅ Goals of the Tool
- Detect faces with flipped/inverted normals
- Automatically recalculate and unify normals to point outward
- Support single or multiple meshes (start with base skin)
- Provide a UI or simple script to process selected meshes

## 🧠 Technical Strategy
- Check for inconsistent face normals:
  + Use the dot product of each face normal with the average vertex normal direction or bounding box centroid direction.
  + Faces pointing inward are likely flipped.
- Reverse face normals only when necessary.
- Optionally, unify normals across connected faces to prevent lighting seams.

## 🧰 Tool Implementation
```python
import maya.cmds as cmds

def fix_flipped_normals(mesh_name):
    if not cmds.objExists(mesh_name):
        cmds.warning(f"Mesh '{mesh_name}' does not exist.")
        return

    # Select and make the normals consistent
    cmds.select(mesh_name, r=True)
    cmds.polySetToFaceNormal(mesh_name, setUserNormal=True)
    cmds.polyNormal(mesh_name, normalMode=0, userNormalMode=0, ch=0)  # Set to 'Unify'
    
    # Flip faces pointing inward
    cmds.polyNormal(mesh_name, normalMode=0, ch=0)  # normalMode=0 = 'Reverse'
    
    print(f"Normals fixed for: {mesh_name}")

# Example usage
fix_flipped_normals("BaseSkinMesh")
```

## ⚙️ TIPS FOR FBX EXPORT/IMPORT
To prevent issues before they reach Maya:
### Blender Export Settings Setting Value Apply Transform
- ✅ Enable Apply Transform
- ✅ Use +Y Up, Z Forward
- ❗ Uncheck Add Leaf Bones
- 🔁 Check Apply Modifiers if using Mirror or Subsurf

### Maya Import Settings Setting Configuration Normals
- Make sure Normals and Tangents are preserved (not recalculated automatically).
- Check Coordinate Conversion behavior if orientation issues occur.

Check conversion
## 🧪 Quality Verification
### Debug Tools
- Add a debug overlay: colorize flipped faces
- Display face normals:
  ```plaintext
  Display > Polygons > Face Normals
   ```
### Pipeline Integration
A Validator tool should be built that includes all QC tools for artists to validate their files before integrating them into Unity. This tool should check for issues such as clearing all history, freezing transforms, ensuring UVs exist, and identifying lamina faces, among others.
If you don't have one, I can build it for you, like this:
![image](https://github.com/user-attachments/assets/22973233-f46b-4c97-a0cc-62f2494c2c99)
