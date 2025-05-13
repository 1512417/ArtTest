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