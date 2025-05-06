# Mobile Dynamic Bones Implementation Guide

Implementing dynamic bones (for cloth, hair, accessories, etc.) in a mobile shooter with a humanoid rig is a great way to increase visual fidelity on higher-tier outfits, but it must be done carefully to balance performance and quality.
Here’s a breakdown of how to approach this from both the tech and art/animation perspectives, including pipeline adjustments and performance constraints tailored for mobile.

## 🎨 Art / Animation Pipeline Changes
### 1. Design for Physics-Enabled Parts
- Separate dynamic parts from main character mesh
  - Hair strands
  - Scarves
  - Coat tails
- Rig with dedicated simulation bones
- No manual animation for these parts
### 2. Bone Hierarchy Guidelines
- Dynamic bones as children of existing skeleton joints
- Example: Scarf_Bone_01 → spine/neck joint
- Keep bone chains minimal and shallow
### 3. Weight Painting Rules
- Weight only to dynamic bone chain
- Avoid main rig weighting
- Ensure smooth, natural weighting
### 4. Export & Prefab Standards
## 🔧 Technical Implementation
### Option A: Unity Built-In Solution
- Simple implementation
- High mobile CPU cost
- Per-frame physics calculations
### Option B: Mobile-Optimized Solutions
Recommended approaches:

- DOTS Bone Physics
- Simple Spring Bone systems
- GPU vertex animation
- Bone-driven curves
## ⚙️ Performance Guidelines
### 1. Bone Count Limits
- Mobile: 5-10 bones max per character
- 1-2 bone chains per asset
- Example pairs:
  - Pigtails
  - Scarf ends
### 2. Culling & LOD Strategy
Disable dynamics when:

- Off-screen
- Distance > threshold
- High-load scenarios
### 3. Simulation Optimization
- Reduced update frequency
- Example: Every 2nd frame
- Configurable via quality settings
### 4. Physics Constraints
- Minimal collision usage
- Simple collider shapes only
  - Capsules
  - Spheres

## 📋 Technical Constraints

| Constraint | Mobile Target |
|------------|---------------|
| Max Dynamic Bone Chains | 2 per outfit |
| Max Bones per Chain | 3-5 |
| Update Frequency | Every 2 frames |
| Colliders | Max 2 per character |
| Fallback Behavior | Replace with static pose |
| LOD Switching | Off when beyond 10m |

## ✅ Pipeline Checklist for High-Tier Dynamic Outfits

| Step | Responsibility | Details |
|------|---------------|----------|
| Add dynamic bones to rig | Artist | Follow bone naming conventions |
| Weight paint dynamic parts | Artist | Only to dynamic chains |
| Tag dynamic parts in FBX | Artist | For prefab automation |
| Create prefab with toggles | Tech Artist | Enable/disable dynamics via script |
| Add fallback/static alternative | Animator | Prebaked idle bone pose |
