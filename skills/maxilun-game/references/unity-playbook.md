# Unity 6 LTS Architecture & Playbook

Unity 6 LTS engineering standards: C# 9+, data-oriented DOTS/ECS architecture, Universal Render Pipeline (URP), Addressables, Netcode for GameObjects (NGO), and NUnit testing.

---

## 1. Modern C# Standards & Zero Memory Allocation

In Unity 6 LTS, the C# runtime supports C# 9+ features. Use pure *value types* to minimize Garbage Collection (GC) load:

```csharp
public readonly record struct CombatDamageEvent(
    int AttackerEntityId,
    int TargetEntityId,
    float DamageAmount,
    float KnockbackImpulse
);

public class UnitStatsConfig : ScriptableObject
{
    [field: SerializeField] public float BaseHealth { get; init; } = 100f;
    [field: SerializeField] public float MovementSpeed { get; init; } = 6.5f;
    [field: SerializeField] public float ArmorRating { get; init; } = 25f;
}
```

### Memory Allocation Invariants:
- Avoid `new` allocations inside `Update()` or `FixedUpdate()`.
- Avoid string formatting calls such as `$"Player Health: {hp}"` every frame in the game loop; update UI text only when a value-change event fires.
- Use `ArrayPool<T>.Shared` or `NativeArray<T>` with a deterministic allocator (`Allocator.TempJob`, `Allocator.Persistent`).

---

## 2. Data-Oriented Architecture (DOTS / ECS)

Use an unmanaged `ISystem` that is fully compatible with the Burst compiler for large-scale, high-performance simulation:

```csharp
using Unity.Burst;
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

public struct UnitMovementSpeed : IComponentData
{
    public float Value;
}

public struct MovementTarget : IComponentData
{
    public float3 Position;
}

[BurstCompile]
public partial struct MovementSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;

        foreach (var (transform, speed, target) in
                 SystemAPI.Query<RefRW<LocalTransform>, RefRO<UnitMovementSpeed>, RefRO<MovementTarget>>())
        {
            float3 dir = math.normalizesafe(target.ValueRO.Position - transform.ValueRO.Position);
            transform.ValueRW.Position += dir * speed.ValueRO.Value * deltaTime;
        }
    }
}
```

---

## 3. Asynchronous Asset Management with Addressables

Use the Addressables package to load assets into memory and unload them without blocking a frame:

```csharp
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AssetLoaderService
{
    private AsyncOperationHandle<GameObject> _prefabHandle;

    public async Task<GameObject> InstantiateEnemyAsync(AssetReferenceGameObject enemyRef, Vector3 spawnPosition)
    {
        _prefabHandle = enemyRef.InstantiateAsync(spawnPosition, Quaternion.identity);
        GameObject spawned = await _prefabHandle.Task;
        return spawned;
    }

    public void ReleaseAsset()
    {
        if (_prefabHandle.IsValid())
        {
            Addressables.Release(_prefabHandle);
        }
    }
}
```

---

## 4. Multiplayer with Netcode for GameObjects (NGO)

The server has full authority over player state and inventory calculations. The client predicts local movement and reconciles its position:

```csharp
using Unity.Netcode;
using UnityEngine;

public class NetworkHealthSystem : NetworkBehaviour
{
    public NetworkVariable<float> NetworkHealth = new(
        100f,
        NetworkVariableReadPermission.Everyone,
        NetworkVariableWritePermission.Server
    );

    [ServerRpc]
    public void ApplyDamageServerRpc(float damageAmount, ServerRpcParams rpcParams = default)
    {
        if (!IsServer) return;

        NetworkHealth.Value = Mathf.Max(0f, NetworkHealth.Value - damageAmount);
        if (NetworkHealth.Value <= 0f)
        {
            HandleDeathClientRpc();
        }
    }

    [ClientRpc]
    private void HandleDeathClientRpc()
    {
        // Play particle effects and ragdoll on the client
    }
}
```

---

## 5. NUnit Testing (PlayMode & EditMode)

Run gameplay logic tests in isolation, with no dependency on editor rendering:

```csharp
using NUnit.Framework;
using UnityEngine;

[TestFixture]
public class CombatCalculatorTests
{
    [Test]
    public void CalculateDamage_ArmorMitigation_FollowsDiminishingReturns()
    {
        float rawDamage = 100f;
        float armor = 100f; // Constant K = 100
        float expectedTaken = 50f;

        float calculated = CombatMath.CalculateMitigatedDamage(rawDamage, armor);

        Assert.AreEqual(expectedTaken, calculated, 0.001f);
    }
}
```

Headless CLI run:
```pwsh
Unity.exe -batchmode -runTests -projectPath . -testPlatform EditMode -testResults results.xml
```
