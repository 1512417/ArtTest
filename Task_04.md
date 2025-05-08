# Maya Normal Fixing Tool Documentation
Flipped normals during the Blender → Maya pipeline are a common issue due to differences in coordinate systems, FBX export/import settings, or mesh construction. Automating the detection and fixing of flipped normals inside Maya can drastically reduce back-and-forth between tools.

## ✅ Goals of the Tool
- Automatically detect and fix flipped normals in imported 3D models
- Provide a user-friendly interface for mesh normal correction
- Give clear logs about the fixing process

## 🧠 Technical Strategy
### Mesh Processing:
   - Works with selected mesh objects
   - Handles both direct mesh selections and transform node selections
   - Uses Maya's OpenMaya API for efficient geometry access
### Normal Detection Algorithm:  
   - For each face in the mesh:
     + Calculates the face's geometric center
     + Gets the face normal direction
     + Determines if the normal is pointing inward by comparing the dot product of the normal and center vector
     + Identifies faces with inverted normals (pointing inward)
### Normal Correction: 
   - Uses Maya's polyNormal command to flip identified faces
   - Preserves mesh topology and UV mapping
   - Processes multiple objects in a single operation
### User Interface: 
   - Simple, single-window design
   - Clear action button
   - Real-time feedback through a log window
   - Persistent display of operation results
### Error Handling: 
   - Validates mesh selection
   - Checks for valid geometry types
   - Provides clear warning messages
   - Gracefully handles non-mesh objects in selection

## 🧰 Tool Implementation
```python
import maya.cmds as cmds
import maya.OpenMaya as om

def fix_flipped_normals():
    # Clear previous log
    cmds.scrollField('normalFixerLog', edit=True, clear=True)
    
    # Get selected objects
    selection = cmds.ls(selection=True)
    
    if not selection:
        log_message("Please select a mesh object")
        return
    
    for obj in selection:
        # Ensure we're working with a mesh
        if cmds.objectType(obj, isType="transform"):
            shapes = cmds.listRelatives(obj, shapes=True)
            if shapes:
                mesh = shapes[0]
        else:
            mesh = obj
            
        if not cmds.objectType(mesh, isType="mesh"):
            continue
            
        # Get the mesh's MFnMesh
        selection_list = om.MSelectionList()
        selection_list.add(mesh)
        dag_path = om.MDagPath()
        selection_list.getDagPath(0, dag_path)
        mesh_fn = om.MFnMesh(dag_path)
        
        # Get face normals
        normal_count = mesh_fn.numNormals()
        face_count = mesh_fn.numPolygons()
        
        flipped_faces = []
        
        # Check each face's normal direction
        for face_id in range(face_count):
            normal = om.MVector()
            mesh_fn.getPolygonNormal(face_id, normal)
            
            # Get face center position
            center = om.MVector()  # Changed from MPoint to MVector
            vertices = om.MPointArray()
            mesh_fn.getPoints(vertices)
            
            vertex_list = om.MIntArray()
            mesh_fn.getPolygonVertices(face_id, vertex_list)
            
            # Calculate geometric center using MVector
            for i in range(vertex_list.length()):
                vertex_point = vertices[vertex_list[i]]
                center += om.MVector(vertex_point.x, vertex_point.y, vertex_point.z)
            center = center / vertex_list.length()
            
            # Check if normal is pointing inward
            if normal.length() > 0:
                normalized_normal = normal.normal()
                if normalized_normal * center < 0:  # Simplified since center is already MVector
                    flipped_faces.append(face_id)
        
        # Fix flipped faces
        if flipped_faces:
            face_names = [f"{mesh}.f[{face}]" for face in flipped_faces]
            cmds.polyNormal(face_names, normalMode=0, userNormalMode=0, ch=1)
            log_message(f"Fixed {len(flipped_faces)} flipped normals in {obj}")
        else:
            log_message(f"No flipped normals found in {obj}")

def log_message(message):
    # Add message to log field and print to console
    cmds.scrollField('normalFixerLog', edit=True, insertText=message + '\n')
    print(message)

def create_normal_fix_ui():
    window_name = "normalFixerUI"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(window_name, title="Normal Fixer", width=300)
    
    cmds.columnLayout(adjustableColumn=True, columnOffset=['both', 10])
    cmds.text(label="Select mesh objects and click the button to fix flipped normals")
    cmds.separator(height=10)
    cmds.button(label="Fix Flipped Normals", command=lambda x: fix_flipped_normals())
    cmds.separator(height=10)
    
    # Add scrollable log field
    cmds.text(label="Log:")
    cmds.scrollField('normalFixerLog', width=280, height=150, wordWrap=True, 
                    editable=False, text="Ready to process...\n")
    
    cmds.showWindow(window)

# Show the UI
create_normal_fix_ui()
```
![image](https://github.com/user-attachments/assets/7d11b29d-60d1-4442-809f-eed33ed069e7)
![image](https://github.com/user-attachments/assets/8a6be089-a088-4b4c-8dab-b63dcc34cf9c)


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
![image](https://github.com/user-attachments/assets/bfe65552-0d7e-4491-80b1-00bca2ba59a7)

