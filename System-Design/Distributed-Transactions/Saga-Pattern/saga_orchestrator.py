from abc import ABC, abstractmethod
class SagaStep(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def compensate(self) -> None:
        pass

# --- MICROSERVICE SIMULATIONS ---
class CreateOrderStep(SagaStep):
    @property
    def name(self): return "Order Service"
    
    def execute(self):
        print("[Execute]   -> Creating pending order in database...")
        return True
        
    def compensate(self):
        print("[Compensate]<- Changing order status to 'CANCELED'.")

class ProcessPaymentStep(SagaStep):
    @property
    def name(self): return "Payment Service"
    
    def execute(self):
        print("[Execute]   -> Charging credit card via Stripe...")
        return True
        
    def compensate(self):
        print("[Compensate]<- Issuing Idempotent Refund to credit card.")

class ReserveInventoryStep(SagaStep):
    def __init__(self, fail_intentionally: bool):
        self.fail_intentionally = fail_intentionally

    @property
    def name(self): return "Inventory Service"
    
    def execute(self):
        print("[Execute]   -> Attempting to reserve item in warehouse...")
        if self.fail_intentionally:
            print("             ❌ ERROR: Item is out of stock!")
            return False
        return True
        
    def compensate(self):
        print("[Compensate]<- Restocking item to warehouse shelves.")
class SagaOrchestrator:
    def run_saga(self, steps: list[SagaStep]) -> bool:
        executed_steps = []
        
        for step in steps:
            print(f"\n⚙️  Running: {step.name}")
            try:
                success = step.execute()
                if success:
                    executed_steps.append(step)
                else:
                    raise Exception(f"Step {step.name} failed gracefully.")
            except Exception as e:
                print(f"\n🚨 SAGA FAILED. INITIATING ROLLBACK SEQUENCE...")
                self._rollback(executed_steps)
                return False
                
        print("\n✅ SAGA COMPLETED SUCCESSFULLY. ALL TRANSACTIONS COMMITTED.")
        return True

    def _rollback(self, executed_steps: list[SagaStep]):
        for step in reversed(executed_steps):
            print(f"⏪ Rolling back: {step.name}")
            step.compensate()
        print("🛡️ System successfully restored to initial state.")

if __name__ == '__main__':
    orchestrator = SagaOrchestrator()
    
    print("=== SCENARIO 1: SUCCESSFUL CHECKOUT ===")
    steps_success = [
        CreateOrderStep(),
        ProcessPaymentStep(),
        ReserveInventoryStep(fail_intentionally=False)
    ]
    assert orchestrator.run_saga(steps_success) == True
    
    print("\n\n=== SCENARIO 2: OUT OF STOCK INVENTORY (TRIGGERING SAGA ROLLBACK) ===")
    steps_fail = [
        CreateOrderStep(),
        ProcessPaymentStep(),
        ReserveInventoryStep(fail_intentionally=True)
    ]
    assert orchestrator.run_saga(steps_fail) == False
    
    print("\nPython Saga Pattern Test Passed!")