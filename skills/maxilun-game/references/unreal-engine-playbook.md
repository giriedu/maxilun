# Unreal Engine 5.x Architecture & Playbook

Standar rekayasa Unreal Engine 5.x: C++20 modern, Gameplay Ability System (GAS), Enhanced Input, Nanite & Lumen, Chaos Physics, replikasi jaringan berotoritas, dan Automation Testing.

---

## 1. Standar C++20 Modern di UE5

### 1.1 `TObjectPtr<T>` & Garbage Collection Hygiene

Gunakan `TObjectPtr<T>` sebagai pengganti raw pointer `T*` untuk properti UObject anggota kelas:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "AbilitySystemInterface.h"
#include "HeroCharacter.generated.h"

class UAbilitySystemComponent;
class UAttributeSet;
class UInputMappingContext;
class UInputAction;

UCLASS(Abstract)
class MYGAME_API AHeroCharacter : public ACharacter, public IAbilitySystemInterface
{
    GENERATED_BODY()

public:
    AHeroCharacter();

    virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|Abilities")
    TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

    UPROPERTY(Transient)
    TObjectPtr<UAttributeSet> AttributeSet;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Input")
    TObjectPtr<UInputMappingContext> DefaultMappingContext;
};
```

### 1.2 Structured Bindings & Type Safety

Gunakan structured bindings untuk dekonstruksi tuple atau hasil perhitungan:

```cpp
if (auto [bSuccess, ImpactPoint, HitActor] = TraceProjectilePath(); bSuccess)
{
    ApplyDirectDamage(HitActor, ImpactPoint);
}
```

---

## 2. Gameplay Ability System (GAS)

Arsitektur kemampuan gameplay dibangun di atas empat pilar GAS:

1. **Gameplay Tags**: Gunakan tag hierarkis (misal `State.Debuff.Stun`, `Ability.Attack.Melee`) untuk perizinan dan blokir kemampuan.
2. **Gameplay Attributes**: Nilai numerik terukur (Health, MaxHealth, Mana, Armor) yang didefinisikan dalam `UAttributeSet`.
3. **Gameplay Effects (GE)**: Modifikasi atribut secara instan, berdurasi, atau periodik dengan kalkulasi mitigasi eksternal.
4. **Gameplay Abilities (GA)**: Logika aktivasi skill asinkron menggunakan Ability Tasks untuk penanganan animasi montase atau target visual trace.

```cpp
// Menambahkan tag state ke Ability System Component
FGameplayTag StunTag = FGameplayTag::RequestGameplayTag(FName("State.Debuff.Stun"));
AbilitySystemComponent->AddLooseGameplayTag(StunTag);
```

---

## 3. Enhanced Input System

Pisahkan penangkapan input mentah dari logika aksi permainan menggunakan Input Mapping Contexts (IMC) dan Input Actions (IA):

```cpp
void AHeroCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    if (UEnhancedInputComponent* EnhancedInputComp = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        EnhancedInputComp->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AHeroCharacter::Move);
        EnhancedInputComp->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
        EnhancedInputComp->BindAction(JumpAction, ETriggerEvent::Completed, this, &ACharacter::StopJumping);
    }
}
```

---

## 4. Replikasi Jaringan & Netcode Otoritatif

Server memvalidasi seluruh aksi kritis permainan. Klien menjalankan prediksi lokal pada pergerakan karakter dan merekonsiliasi state saat terjadi koreksi server (*desync*):

```cpp
#include "Net/UnrealNetwork.h"

void AHeroCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME_CONDITION(AHeroCharacter, CurrentHealth, COND_OwnerOnly);
    DOREPLIFETIME(AHeroCharacter, bIsSprinting);
}

UFUNCTION(Server, Reliable, WithValidation)
void Server_RequestFireWeapon(const FVector_NetQuantize& AimTarget);

bool Server_RequestFireWeapon_Validate(const FVector_NetQuantize& AimTarget)
{
    // Validasi jangkauan maksimum dan raycast sanitization
    return FVector::DistSquared(GetActorLocation(), AimTarget) <= FMath::Square(5000.0f);
}

void Server_RequestFireWeapon_Implementation(const FVector_NetQuantize& AimTarget)
{
    ExecuteWeaponFireAuthoritative(AimTarget);
}
```

---

## 5. Otomasi Pengujian dengan Unreal Automation Tool

Tulis pengujian fungsional unit menggunakan makro pengujian standar Unreal Engine:

```cpp
#include "Misc/AutomationTest.h"
#include "Combat/CombatCalculation.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCombatDamageMitigationTest, "MyGame.Combat.MitigationFormula",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FCombatDamageMitigationTest::RunTest(const FString& Parameters)
{
    const float RawDamage = 100.0f;
    const float Armor = 100.0f; // K = 100 konstanta mitigasi
    const float ExpectedDamage = 50.0f;

    const float ActualDamage = UCombatCalculation::CalculateDamage(RawDamage, Armor);

    TestEqual(TEXT("Kerusakan setelah mitigasi armor harus sesuai kurva 50%"), ActualDamage, ExpectedDamage);
    return true;
}
```

Eksekusi CLI headless via AutomationTool:
```cmd
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:\MyGame\MyGame.uproject" -ExecCmds="Automation RunTests MyGame.; Quit" -unattended -nullrhi -stdout -FullStdOutLogOutput
```
Exit code 0 menandakan seluruh suite pengujian lulus.
