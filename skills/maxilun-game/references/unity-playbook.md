# Unity 6 LTS Architecture & Playbook

Standar rekayasa Unity 6 LTS: C# 9+, arsitektur berorientasi data DOTS/ECS, Universal Render Pipeline (URP), Addressables, Netcode for GameObjects (NGO), dan pengujian NUnit.

---

## 1. Standar C# Modern & Alokasi Memori Nol

Di Unity 6 LTS, runtime C# mendukung fitur C# 9+. Manfaatkan tipe data bernilai murni (*value types*) untuk meminimalkan beban Garbage Collection (GC):

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

### Invarian Alokasi Memori:
- Hindari alokasi `new` di dalam `Update()` atau `FixedUpdate()`.
- Hindari pemanggilan string formatting seperti `$"Player Health: {hp}"` setiap frame di game loop; perbarui teks UI hanya saat event perubahan nilai dipicu.
- Gunakan `ArrayPool<T>.Shared` atau `NativeArray<T>` dengan allocator deterministik (`Allocator.TempJob`, `Allocator.Persistent`).

---

## 2. Arsitektur Data-Oriented (DOTS / ECS)

Gunakan `ISystem` unmanaged yang kompatibel penuh dengan kompilator Burst untuk simulasi masif performa tinggi:

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

## 3. Manajemen Aset Asinkron dengan Addressables

Gunakan paket Addressables untuk memuat dan membongkar aset dari memori tanpa blocking frame:

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

## 4. Multiplayer dengan Netcode for GameObjects (NGO)

Server berwenang penuh atas kalkulasi status dan inventaris pemain. Klien memprediksi pergerakan lokal dan merekonsiliasi posisi:

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
        // Jalankan efek partikel dan ragdoll di klien
    }
}
```

---

## 5. Pengujian NUnit (PlayMode & EditMode)

Pengujian logika gameplay dijalankan secara terisolasi tanpa bergantung pada rendering editor:

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
        float armor = 100f; // Konstanta K = 100
        float expectedTaken = 50f;

        float calculated = CombatMath.CalculateMitigatedDamage(rawDamage, armor);

        Assert.AreEqual(expectedTaken, calculated, 0.001f);
    }
}
```

Eksekusi CLI headless:
```pwsh
Unity.exe -batchmode -runTests -projectPath . -testPlatform EditMode -testResults results.xml
```
