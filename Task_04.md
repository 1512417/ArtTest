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
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)

class NormalFixTool(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(NormalFixTool, self).__init__(parent)
        
        self.setWindowTitle("Normal Fix Tool")
        self.setMinimumWidth(300)
        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_widgets(self):
        self.check_btn = QtWidgets.QPushButton("Check Selected Objects")
        self.select_flipped_btn = QtWidgets.QPushButton("Select Flipped Objects")
        self.fix_btn = QtWidgets.QPushButton("Fix Selected Objects")
        self.fix_all_btn = QtWidgets.QPushButton("Fix All Objects")
        self.result_label = QtWidgets.QLabel("Select objects to check normals")
        
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.check_btn)
        main_layout.addWidget(self.select_flipped_btn)
        main_layout.addWidget(self.fix_btn)
        main_layout.addWidget(self.fix_all_btn)
        main_layout.addWidget(self.result_label)
        self.setLayout(main_layout)
        
    def create_connections(self):
        self.check_btn.clicked.connect(self.check_normals)
        self.select_flipped_btn.clicked.connect(self.select_flipped_objects)
        self.fix_btn.clicked.connect(lambda: self.fix_normals(selected_only=True))
        self.fix_all_btn.clicked.connect(lambda: self.fix_normals(selected_only=False))

    def select_flipped_objects(self):
        all_meshes = cmds.ls(type='mesh', dag=True, long=True)
        flipped_objects = []
        
        for mesh in all_meshes:
            face_normals = cmds.polyInfo(mesh, faceNormals=True)
            if face_normals:
                for normal in face_normals:
                    nx, ny, nz = map(float, normal.split()[2:5])
                    if nx < 0 or ny < 0 or nz < 0:
                        # Get transform node instead of shape node
                        transform = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
                        flipped_objects.append(transform)
                        break
        
        if flipped_objects:
            cmds.select(flipped_objects, replace=True)
            self.result_label.setText(f"Selected {len(flipped_objects)} objects with flipped normals")
        else:
            cmds.select(clear=True)
            self.result_label.setText("No flipped normals found in scene")
    
    def check_normals(self):
        selection = cmds.ls(selection=True, type='mesh', dag=True, long=True)
        if not selection:
            self.result_label.setText("No objects selected")
            return
            
        flipped_count = 0
        for mesh in selection:
            # Get face normals
            face_normals = cmds.polyInfo(mesh, faceNormals=True)
            if face_normals:
                # Check for negative normals
                for normal in face_normals:
                    nx, ny, nz = map(float, normal.split()[2:5])
                    if nx < 0 or ny < 0 or nz < 0:
                        flipped_count += 1
                        break
        
        if flipped_count > 0:
            self.result_label.setText(f"Found {flipped_count} objects with flipped normals")
        else:
            self.result_label.setText("No flipped normals found")
    
    def fix_normals(self, selected_only=True):
        if selected_only:
            meshes = cmds.ls(selection=True, type='mesh', dag=True, long=True)
            if not meshes:
                self.result_label.setText("No objects selected")
                return
        else:
            meshes = cmds.ls(type='mesh', dag=True, long=True)
            if not meshes:
                self.result_label.setText("No mesh objects in scene")
                return
        
        fixed_count = 0
        for mesh in meshes:
            # Unify normals
            cmds.polyNormal(mesh, normalMode=2, userNormalMode=0, ch=1)
            # Orient normals outward
            cmds.polySetToFaceNormal(mesh)
            fixed_count += 1
        
        self.result_label.setText(f"Fixed normals on {fixed_count} objects")

def show_dialog():
    dialog = NormalFixTool()
    dialog.show()

if __name__ == "__main__":
    show_dialog()
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
