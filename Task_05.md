# Mobile Dynamic Bones Implementation Guide

Implementing dynamic bones (for cloth, hair, accessories, etc.) in a mobile shooter with a humanoid rig is a great way to increase visual fidelity on higher-tier outfits, but it must be done carefully to balance performance and quality.
Here’s a breakdown of how to approach this from both the tech and art/animation perspectives, including pipeline adjustments and performance constraints tailored for mobile.

## 🎨 Art / Animation Pipeline Changes
### 1. Design for Physics-Enabled Parts
- Artists must clearly separate dynamic parts (e.g., hair strands, scarves, coat tails) from the main character mesh.
- These parts should be rigged with extra bones specifically for simulation (not animated manually).
### 2. Bone Hierarchy Guidelines
- Add dynamic bones as children of existing skeleton joints, maintaining clean hierarchy.
  + e.g., attach "Scarf_Bone_01" to the spine or neck joint.
- Avoid deep or excessive chains — keep bone chains short and minimal for performance.
### 3. Weight Painting Rules
- Ensure dynamic parts are only weighted to the dynamic bone chain, not the main rig.
- Weighting should be smooth and natural to avoid erratic simulation.
### 4. Export & Prefab Standards
- Dynamic bone rigs should:
  + Use a consistent naming convention (e.g., _Dyn_ prefix).
  + Be tagged or separated in FBX for easy identification during prefab setup.
- Export as separate skinned mesh renderers, or embedded but referenced via script.

## 🔧 Technical Implementation
### Option A: Unity Built-In Solution (e.g., Legacy Dynamic Bone asset)
- Simple implementation
- Performance-heavy on mobile — each dynamic bone requires CPU physics calculation per frame.
### Option B: Mobile-Optimized Solutions (Recommended for Mobile)
- Use custom dynamic bone system or optimized assets like:
- Unity DOTS Bone Physics (if compatible with your project architecture).
- Simple Spring Bone systems (minimal math, fewer allocations).
- GPU-based vertex animation or bone-driven animation curves (for pre-authored motion).
  
Runtime Setup:
```csharp
if (deviceIsHighTier)
    EnableDynamicBones();
else
    UseStaticBones();
 ```
Allow toggling dynamic bones based on device capability or graphics settings.

## ⚙️ Performance Guidelines
### 1. Bone Count Limits
- Define a maximum number of dynamic bones per character.
  + 📱 Mobile: 5–10 bones max per character (even less for low-end devices).
  + 🧍 Prefer 1–2 bone chains per asset (e.g., pigtails, scarf ends).
### 2. Culling & LOD Strategy
- Disable or freeze dynamics bones when:
  + Off-screen
  + Distance > threshold
  + High-load scenarios
- Use LODGroup or custom LOD switching script.
### 3. Simulation Optimization
- Update dynamic bones at reduced framerate:
  + e.g., simulate every 2 frames instead of 1.
- This can be exposed via quality settings.
### 4. Collision & Physics Constraints
- Avoid physics-based collisions unless critical.
- If used, simplify colliders (capsules/spheres only).

## 📋 Technical Constraints

| Device Tier | Max Chains | Bones/Chain | Update Rate | Collision |
|-------------|------------|-------------|-------------|-----------|
| High-End    | 3         | 5           | 30Hz (half rate of 60FPS gameplay) | Simple    |
| Mid-Tier    | 2         | 3           | 20Hz        | None      |
| Low-End     | 0         | Static Only  | N/A         | N/A       |

## ✅ Pipeline Checklist for High-Tier Dynamic Outfits

| Step | Responsibility | Details |
|------|---------------|----------|
| Add dynamic bones to rig | Artist | Follow bone naming conventions |
| Weight paint dynamic parts | Artist | Only to dynamic chains |
| Tag dynamic parts in FBX | Artist | For prefab automation |
| Create prefab with toggles | Tech Artist | Enable/disable dynamics via script |
| Add fallback/static alternative | Animator | Prebaked idle bone pose |
