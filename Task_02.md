# Camouflage System Implementation Guide
## 🎯 GOAL
- Input: 3-color B&W camouflage PNG (Black, Gray, White)
- Tool: Maya/Blender tool to allow recoloring these 3 values
- Output:
  + 6 ScriptableObjects (with color sets)
  + Shader/material in Unity that uses the texture and color map
  + C# script that applies ScriptableObject colors to the shader

## 🧰 Part 1: DCC Tool Implementation
### Maya Export Tool
The Camo Texture Editor is a Maya tool that allows users to preview and customize camouflage texture colors. It provides a simple interface to load a grayscale texture and assign specific colors to different luminance ranges (white, grey, and black areas). The tool also supports exporting color settings to Unity.
- Load and preview grayscale textures
- Real-time color customization
- Live preview of color changes
- Export color settings to Unity-compatible format
```python
import os
import json
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance


def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)

class TexturePreviewWidget(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(TexturePreviewWidget, self).__init__(parent)
        self.setMinimumSize(200, 200)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("No texture loaded")
        self.setStyleSheet("border: 1px solid gray")
        self.original_pixmap = None
        self.colors = {
            "white": QtGui.QColor(255, 255, 255),
            "grey": QtGui.QColor(128, 128, 128),
            "black": QtGui.QColor(0, 0, 0)
        }

    def load_texture(self, file_path):
        if not file_path or not os.path.exists(file_path):
            self.setText("No texture loaded")
            self.original_pixmap = None
            return

        self.original_pixmap = QtGui.QPixmap(file_path)
        self.update_preview()

    def update_preview(self):
        if not self.original_pixmap:
            return
            
        # Create working copy
        image = self.original_pixmap.toImage()
        
        # Process each pixel
        for x in range(image.width()):
            for y in range(image.height()):
                pixel = image.pixel(x, y)
                gray = QtGui.qGray(pixel)
                
                if gray > 178:  # White areas (70%)
                    image.setPixel(x, y, self.colors["white"].rgb())
                elif gray > 76:  # Grey areas (30-70%)
                    image.setPixel(x, y, self.colors["grey"].rgb())
                else:  # Black areas
                    image.setPixel(x, y, self.colors["black"].rgb())
        
        # Convert back to pixmap and scale
        pixmap = QtGui.QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(
            200, 200,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

    def update_color(self, area, color):
        self.colors[area] = color
        self.update_preview()

class CamoTextureEditor(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(CamoTextureEditor, self).__init__(parent)
        
        self.setWindowTitle("Camo Texture Editor")
        self.setMinimumWidth(400)
        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_widgets(self):
        # File input
        self.file_path_le = QtWidgets.QLineEdit()
        self.browse_btn = QtWidgets.QPushButton("Browse")
        
        # Color pickers
        self.white_color_btn = QtWidgets.QPushButton("White Areas")
        self.grey_color_btn = QtWidgets.QPushButton("Grey Areas")
        self.black_color_btn = QtWidgets.QPushButton("Black Areas")
        
        # Add texture preview widget
        self.texture_preview = TexturePreviewWidget()
        
        # Add export button
        self.export_btn = QtWidgets.QPushButton("Export Colors for Unity")
    
    def create_layout(self):
        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(QtWidgets.QLabel("Texture:"))
        file_layout.addWidget(self.file_path_le)
        file_layout.addWidget(self.browse_btn)
        
        color_layout = QtWidgets.QVBoxLayout()
        color_layout.addWidget(self.white_color_btn)
        color_layout.addWidget(self.grey_color_btn)
        color_layout.addWidget(self.black_color_btn)
        
        # Add preview to layout
        preview_layout = QtWidgets.QVBoxLayout()
        preview_layout.addWidget(QtWidgets.QLabel("Texture Preview:"))
        preview_layout.addWidget(self.texture_preview)
        
        # Modify main layout to include preview
        main_layout = QtWidgets.QHBoxLayout()
        
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addLayout(file_layout)
        left_layout.addLayout(color_layout)
        left_layout.addWidget(self.export_btn)
        left_layout.addStretch()
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(preview_layout)
        
        # Set the main layout
        self.setLayout(main_layout)
        
    def create_connections(self):
        self.browse_btn.clicked.connect(self.browse_file)
        self.white_color_btn.clicked.connect(lambda: self.pick_color("white"))
        self.grey_color_btn.clicked.connect(lambda: self.pick_color("grey"))
        self.black_color_btn.clicked.connect(lambda: self.pick_color("black"))
        self.export_btn.clicked.connect(self.export_colors)
    
    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Camo Texture",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.file_path_le.setText(file_path)
            self.texture_preview.load_texture(file_path)

    def pick_color(self, area):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            button = getattr(self, f"{area}_color_btn")
            button.setStyleSheet(f"background-color: {color.name()}")
            self.texture_preview.update_color(area, color)

    def export_colors(self):
        colors_data = {
            "name": "CamoColors",
            "whiteColor": self._color_to_unity_format(self.white_color_btn),
            "greyColor": self._color_to_unity_format(self.grey_color_btn),
            "blackColor": self._color_to_unity_format(self.black_color_btn)
        }
        
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export Colors",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            with open(file_path, 'w') as f:
                json.dump(colors_data, f, indent=4)
                
            QtWidgets.QMessageBox.information(
                self,
                "Export Successful",
                f"Colors exported to:\n{file_path}"
            )
    
    def _color_to_unity_format(self, button):
        color = button.palette().button().color()
        return {
            "r": color.redF(),
            "g": color.greenF(),
            "b": color.blueF(),
            "a": 1.0
        }

def show_dialog():
    dialog = CamoTextureEditor()
    dialog.show()

if __name__ == "__main__":
    show_dialog()
```
![image](https://github.com/user-attachments/assets/02b24823-6e71-454d-8328-5a2ce3e95372)


## 🧾 Part 2: Unity Implementation
### CamoColorSet ScriptableObject
```csharp
using UnityEngine;
using UnityEditor;
using System.IO;

[CreateAssetMenu(fileName = "CamoColors", menuName = "Camo/Color Settings")]
public class CamoColors : ScriptableObject
{
    public Color whiteColor = Color.white;
    public Color greyColor = Color.gray;
    public Color blackColor = Color.black;

    [ContextMenu("Import Colors From JSON")]
    public void ImportFromJson()
    {
        string path = EditorUtility.OpenFilePanel("Select JSON File", "", "json");
        if (string.IsNullOrEmpty(path)) return;

        string jsonContent = File.ReadAllText(path);
        JsonUtility.FromJsonOverwrite(jsonContent, this);
        EditorUtility.SetDirty(this);
        AssetDatabase.SaveAssets();
    }
}
```
### Importing Colors in Unity
1. Create a new Color Settings asset (Right-click > Create > Camo > Color Settings)
2. Select the created asset
3. Right-click on the inspector header
4. Choose "Import Colors From JSON"
5. Select your exported JSON file

## 🎨 Part 3: Shader Implementation
### HLSL Version
```hlsl
fixed4 frag(v2f i) : SV_Target {
    float sample = tex2D(_MainTex, i.uv).r;

    if (sample < 0.33) return _ColorBlack;
    else if (sample < 0.66) return _ColorGray;
    else return _ColorWhite;
}
```

### Shader Properties

| Property | Type | Description |
|---|---|---|
| _MainTex | Texture2D | Grayscale camo pattern |
| _ColorBlack | Color | Color for dark regions (0-0.33) |
| _ColorGray | Color | Color for mid regions (0.33-0.66) |
| _ColorWhite | Color | Color for light regions (0.66-1.0) |
| _Threshold1 | Float | Lower threshold (default 0.33) |
| _Threshold2 | Float | Upper threshold (default 0.66) |

## ⚙️ Part 4: Runtime Controller
### CamoMaterialApplier Component
```csharp
using UnityEngine;

public class CamoMaterialApplier : MonoBehaviour
{
    public Material targetMaterial;
    public CamoColorSet camoSet;

    public void ApplyColors()
    {
        if (targetMaterial == null || camoSet == null) return;

        targetMaterial.SetColor("_ColorBlack", camoSet.colorForBlack);
        targetMaterial.SetColor("_ColorGray", camoSet.colorForGray);
        targetMaterial.SetColor("_ColorWhite", camoSet.colorForWhite);
    }
}
```

### Deliverables Checklist

| Component | Status | Description | Dependencies |
|---|---|---|---|
| Base Texture | Required | B&W camo pattern PNG | DCC tool |
| DCC Export Tool | Required | Color config generator | Python, Maya/Blender |
| ScriptableObjects | Required | 6 color variant sets | Unity |
| Shader | Required | Color mapping implementation | Unity URP/HLSL |
| Runtime Controller | Required | Dynamic color application | Unity C# |
| Documentation | Optional | Setup and usage guide | Markdown |
