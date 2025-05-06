# Electric Weapon Skin Creation Guidelines
## 🎨 Artistic Guidelines
### 1. Shape Language
- Favor medium-to-large flat or gently curved surfaces for electric VFX travel
- Avoid excessive small-scale geometry that can:
  - Interrupt shader flow
  - Cause UV issues
### 2. Surface Readability
- Design skin for visible electric texture
- Avoid overcrowding with:
  - Decals
  - Greebles
  - Dark color details
- Highlight electricity flow areas:
  - Barrel
  - Edges
  - Defined channels
### 3. Emissive Detail Zones
- Mark/model areas for:
  - Emissive electricity pulses
  - Sparks
- Consider integrating:
  - Tech grooves
  - Glowing seams
  - Capacitors
    
## 🧰 Technical Guidelines
### 1. Shared Generic Weapon Mesh
- Match base generic weapon mesh:
  - Scale
  - Pivot
  - Proportions
- Avoid geometry alterations affecting:
  - UV layout
  - Shader-driven effects
### 2. UV Mapping Requirements
- Clean and proportional UV unwrapping
- No overlapping UV shells (unless intentional)
- Uniform texel density for Voronoi shader
    
## ⚡ VFX Shader Compatibility
### 1. Voronoi Shader Design
- Test models with electric Voronoi shader
- Preview in VFX team's test scenes
### 2. Material Setup

![image](https://github.com/user-attachments/assets/680d7c0c-764a-4617-a72d-33885011ddb1)


### 3. Animation Guidelines
- No custom skinned/animated parts
- Use standardized animation system
- Match base weapon bone hierarchy
  
## ✅ Deliverables Checklist 

| Asset | Requirement |
|-------|-------------|
| Mesh | Matches base weapon mesh in scale and proportions |
| UVs | Clean, non-overlapping, uniform density |
| Textures | BaseColor, Normal, Emissive, optional Mask (RGBA) |
| Shader Testing | Previewed with Voronoi shader for flow quality |
| Poly Budget | Mobile-friendly, ≤ X tris (define exact budget) |
| Naming | Use naming conventions like Weapon_ElectricSkin01.fbx |

## 📦 Artist Tools
### Gym Scene Contents for review
- Base weapon prefab contains:
  + Weapon mesh
  + VFX

### Automation screenshot tool
- Take screenshot with transparent background so we can use that for the icon of weapon in game.
