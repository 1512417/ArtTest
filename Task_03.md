# Character Customization System Documentation
## 1. Character Model Design (Base Mesh + Modular Parts)
### Strategy
- Use a base mesh with predefined attachment points and consistent topology.
### Base Character
- One base mesh (male, female, or unisex depending on scope)
- Same rig (skeleton) across all customizable parts
- Design the mesh with vertex masking for hiding unseen body parts
### Modular Parts
- Each customization piece (Hair, Eyewear, etc.) is a separate mesh
- Skinned to the same skeleton as the base character
Key Tip : Use bone-based animation, not blend shapes, to ensure compatibility and performance on mobile.

## 2. File & Asset Organization
### Folder Structure
```plaintext
Assets/
├── Characters/
│   ├── BaseMesh/
│   ├── Hair/
│   ├── Eyewear/
│   ├── Tops/
│   ├── Bottoms/
│   ├── Shoes/
│   └── Faces/
 ```
### Define CustomizationCategory  (ScriptableObject)
```csharp
public enum CustomizationCategory
{
     Hair,
     Eyewear,
     Tops,
     Bottoms,
     Shoes,
     Face
}
```
### Customization Item Definition (ScriptableObject)
```csharp
[CreateAssetMenu(menuName = "Customization/Item")]
public class CustomizationItem : ScriptableObject
{
    public string itemName;
    public GameObject prefab;
    public CustomizationCategory category;
}
```

## 3. Runtime Customization System
### Strategy
- Dynamically attach/detach modular parts at runtime
### Key Components
- Attachment Points: Empty GameObjects parented to the skeleton
- CharacterCustomizer Script Example:
```csharp
public void EquipItem(CustomizationItem item)
{
    Transform attachPoint = GetAttachPoint(item.category);
    
    // Clear existing
    foreach (Transform child in attachPoint) Destroy(child.gameObject);

    // Instantiate new
    Instantiate(item.prefab, attachPoint);
}
```

## 4. Optimization Techniques
### A. GPU Skinning / GPU Instancing
- Use shared skeleton for efficient GPU skinning
- Utilize SkinnedMeshRenderers with shared bones
### B. Texture Optimization
- Combine textures into atlases
- Use Texture Arrays for different materials
### C. LOD System
- Implement Level of Detail for distant characters
- Simplified meshes for performance
### D. Object Pooling
- Reuse instantiated customization objects
- Avoid runtime GC spikes

## 5. Content Creation Guidelines (Artist)
### Artist Requirements
- Match bone weights and hierarchy
- Follow naming conventions
- Use consistent scale and orientation
- Export in FBX format by category
### Skin Weight Consistency
- Modular parts must match the skin weights of the corresponding areas on the base mesh.
- Avoid assigning a vertex to bones outside its expected influence zone (e.g., don't let a glove mesh get weights from the pelvis).
- Use a copy-skin-weights or transfer-weights tool (like Maya’s Copy Skin Weights) when binding parts.
- Limit to 4 bone influences per vertex (or 2 on very low-end targets) to maintain GPU skinning performance.
- Keep weights clean—no stray influences or unnormalized values.

## 6. Testing & Profiling (TechArt)
### Performance Monitoring
- Use Unity Profiler (Memory Profiler, Frame Debugger, or RenderDoc if deep analysis is needed)
- Monitor CPU/GPU usage
- Track draw calls and memory
- Test on low-end devices

## 7. Editor Tools (TechArt)
### Customization Editor
- Preview combinations
- Validate parts
- Test without runtime
- The Artist has a place to showcase their works for review.
- The Level Design and Game Design have a place to find the objects they need.
### Skin Weight Debugging
- Use Unity’s SkinnedMeshRenderer > Debug > Weights Visualization (via third-party or custom editor tools).
- Validate:
  + Bone influence limits
  + Weight normalization
  + No missing bones during runtime binding

  
# Summary Checklist 
| Area | Solution |
|------|----------|
| Base Mesh | One rig, modular parts |
| Runtime Switching | SkinnedMeshRenderer swapping |
| Texture Optimization | Atlases or arrays |
| Mobile Performance | GPU skinning, LODs, pooling |
| Customization Data | ScriptableObjects |
| Editor Workflow | Clean folders, prefab references |
| Load Management | Use Addressables for scalability |
