# Unreal Engine 5.x Architecture & Playbook

Unreal Engine 5.x engineering standards: modern C++20, Gameplay Ability System (GAS), Enhanced Input, Nanite & Lumen, Chaos Physics, authoritative network replication, and Automation Testing.

---

## 1. Modern C++20 Standards in UE5

### 1.1 `TObjectPtr<T>` & Garbage Collection Hygiene

Use `TObjectPtr<T>` instead of a raw `T*` pointer for UObject member properties of a class:

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

Use structured bindings to destructure a tuple or a calculation result:

```cpp
if (auto [bSuccess, ImpactPoint, HitActor] = TraceProjectilePath(); bSuccess)
{
    ApplyDirectDamage(HitActor, ImpactPoint);
}
```

---

## 2. Gameplay Ability System (GAS)

Build the gameplay ability architecture on the four pillars of GAS:

1. **Gameplay Tags**: Use hierarchical tags (for example `State.Debuff.Stun`, `Ability.Attack.Melee`) to permit and block abilities.
2. **Gameplay Attributes**: Measured numeric values (Health, MaxHealth, Mana, Armor) defined in a `UAttributeSet`.
3. **Gameplay Effects (GE)**: Attribute modifications that are instant, timed, or periodic, with external mitigation calculation.
4. **Gameplay Abilities (GA)**: Asynchronous skill activation logic that uses Ability Tasks to handle montage animations or visual target traces.

```cpp
// Add a state tag to the Ability System Component
FGameplayTag StunTag = FGameplayTag::RequestGameplayTag(FName("State.Debuff.Stun"));
AbilitySystemComponent->AddLooseGameplayTag(StunTag);
```

---

## 3. Enhanced Input System

Separate raw input capture from game action logic with Input Mapping Contexts (IMC) and Input Actions (IA):

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

## 4. Network Replication & Authoritative Netcode

The server validates every critical game action. The client runs local prediction for character movement and reconciles state when the server sends a correction (*desync*):

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
    // Validate maximum range and sanitize the raycast
    return FVector::DistSquared(GetActorLocation(), AimTarget) <= FMath::Square(5000.0f);
}

void Server_RequestFireWeapon_Implementation(const FVector_NetQuantize& AimTarget)
{
    ExecuteWeaponFireAuthoritative(AimTarget);
}
```

---

## 5. Test Automation with Unreal Automation Tool

Write functional unit tests with the standard Unreal Engine test macros:

```cpp
#include "Misc/AutomationTest.h"
#include "Combat/CombatCalculation.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCombatDamageMitigationTest, "MyGame.Combat.MitigationFormula",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FCombatDamageMitigationTest::RunTest(const FString& Parameters)
{
    const float RawDamage = 100.0f;
    const float Armor = 100.0f; // K = 100 mitigation constant
    const float ExpectedDamage = 50.0f;

    const float ActualDamage = UCombatCalculation::CalculateDamage(RawDamage, Armor);

    TestEqual(TEXT("Damage after armor mitigation must match the 50% curve"), ActualDamage, ExpectedDamage);
    return true;
}
```

Headless CLI run through AutomationTool:
```cmd
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:\MyGame\MyGame.uproject" -ExecCmds="Automation RunTests MyGame.; Quit" -unattended -nullrhi -stdout -FullStdOutLogOutput
```
Exit code 0 means the whole test suite passed.
