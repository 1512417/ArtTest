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
```python
import maya.cmds as cmds
import json
import os

def export_camouflage_set(name, black_color, gray_color, white_color, export_path):
    data = {
        "setName": name,
        "black": black_color,
        "gray": gray_color,
        "white": white_color
    }
    
    filepath = os.path.join(export_path, name + ".json")
    with open(filepath, 'w') as f:
        json.dump(data, f)
    
    print("Camouflage set exported to:", filepath)
```

### Usage Example
```python
export_camouflage_set(
    "UrbanCamo",
    black_color=[0.1, 0.1, 0.1],
    gray_color=[0.5, 0.5, 0.5],
    white_color=[1.0, 1.0, 1.0],
    export_path="C:/Temp/CamoSets"
)
 ```

## 🧾 Part 2: Unity Implementation
### CamoColorSet ScriptableObject
```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewCamoColorSet", menuName = "Customization/CamoColorSet")]
public class CamoColorSet : ScriptableObject
{
    public Color colorForBlack;
    public Color colorForGray;
    public Color colorForWhite;
}
```

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
