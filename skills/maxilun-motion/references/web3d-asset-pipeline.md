# Web3D Asset Pipeline & Texture Optimization

Production standard for modelling, converting, compressing, and packaging 3D assets (Blender & Substance 3D) for low-latency interactive web delivery.

---

## 1. ORM Texture Packing (Occlusion - Roughness - Metallic)

In a standard PBR workflow, the browser often loads 3 separate monochrome texture files:
1. Ambient Occlusion map (grayscale)
2. Roughness map (grayscale)
3. Metallic map (grayscale)

Loading these 3 textures separately wastes mobile bandwidth and consumes 3x the GPU texture sampler slots.

### ORM Channel Packing Standard:
Merge the three channels into **one 8-bit RGB texture file**:
- **R channel (Red)**: Ambient Occlusion (AO)
- **G channel (Green)**: Roughness
- **B channel (Blue)**: Metallic
- *(Optional) A channel (Alpha)*: Opacity / Masking

```
File: asset_name_orm.png (or .webp / .ktx2)
├── R: Ambient Occlusion
├── G: Roughness
└── B: Metallic
```

### Three.js / R3F Material Configuration for ORM Textures:
```javascript
const textureLoader = new THREE.TextureLoader();
const ormMap = textureLoader.load('/textures/product_orm.webp');

const material = new THREE.MeshStandardMaterial({
  map: colorMap,
  aoMap: ormMap,             // Read from the Red channel
  aoMapIntensity: 1.0,
  roughnessMap: ormMap,      // Read from the Green channel
  roughness: 1.0,
  metalnessMap: ormMap,      // Read from the Blue channel
  metalness: 1.0
});
```
*Performance result: saves 66% of GPU VRAM texture memory and cuts HTTP requests from 3 to 1.*

---

## 2. Blender-to-Web Export Flow (GLTF / GLB)

Before exporting a model from Blender for the web, apply these 4 mandatory cleanup steps:

### Step 1: Normalize Transforms (Apply Transforms)
Select every mesh and press `Ctrl + A` -> `All Transforms` (Location, Rotation, Scale = 1.0). This prevents matrix distortion on import into Three.js.

### Step 2: Audit Polygon Count & Decimate
- Delete hidden geometry the camera never sees (for example: the inside of a product casing).
- Apply the `Decimate` modifier to reduce vertices until the model is under budget ($\le 50\text{k}$ triangles for mobile).

### Step 3: Armature / Bone Rigging Limits (Mobile WebGL Limit)
- Limit *bones per mesh* to a maximum of **64 bones** for compatibility with mobile vertex shaders.
- Keep bone weights to at most 4 influences per vertex.

### Step 4: GLTF 2.0 Export Settings in Blender
When exporting through `File > Export > glTF 2.0 (.glb/.gltf)`:
- **Format**: `glTF Binary (.glb)` (packs geometry, animation, and textures into 1 compressed binary file).
- **Include**: Selected Objects, Custom Properties.
- **Transform**: `+Y Up` (the WebGL coordinate standard).
- **Geometry**:
  - `Apply Modifiers`: On.
  - `UVs`: On.
  - `Normals`: On.
  - `Tangents`: On (when using normal maps).
- **Compression**: Enable **Draco Mesh Compression** (Level 7 for non-animated geometry) or use the `meshopt` pipeline.

---

## 3. Post-Export Optimization (glTF-Transform CLI)

Use the `gltf-transform` CLI to optimize the `.glb` file before adding it to production web assets:

```bash
# 1. Remove duplicate vertices and clean the node structure
npx @gltf-transform/cli dedup input.glb step1.glb

# 2. Compress textures to a modern GPU format (WebP / KTX2)
npx @gltf-transform/cli webp step1.glb step2.glb --quality 80

# 3. Apply Meshopt compression for instant decompression in the browser
npx @gltf-transform/cli meshopt step2.glb output-optimized.glb

# 4. Validate the size and draw call report
npx @gltf-transform/cli inspect output-optimized.glb
```

---

## 4. Web3D Asset Quality Checklist

- Texture resolution is *Power-of-Two* (`512x512`, `1024x1024`, or at most `2048x2048`).
- Total size of the deliverable `.glb` file is $\le 3.5\text{MB}$ for desktop and $\le 1.5\text{MB}$ for a mobile landing page.
- The main rotation axis faces forward (`Z+` or `Y+`, matching the initial camera orientation).
- The model pivot/origin sits at the center of the bounding box or at the object's floor base.
- Base color (*albedo/diffuse*) textures use the sRGB color space; ORM and Normal textures use the Linear color space.
