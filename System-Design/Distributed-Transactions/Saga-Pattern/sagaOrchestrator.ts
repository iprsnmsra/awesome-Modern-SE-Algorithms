interface SagaStep {
    name: string;
    execute(): boolean;
    compensate(): void;
}

class CreateOrderStep implements SagaStep {
    name = "Order Service";
    execute(): boolean {
        console.log("[Execute]   -> Creating pending order in database...");
        return true;
    }
    compensate(): void {
        console.log("[Compensate]<- Changing order status to 'CANCELED'.");
    }
}

class ProcessPaymentStep implements SagaStep {
    name = "Payment Service";
    execute(): boolean {
        console.log("[Execute]   -> Charging credit card via Stripe...");
        return true;
    }
    compensate(): void {
        console.log("[Compensate]<- Issuing Idempotent Refund to credit card.");
    }
}

class ReserveInventoryStep implements SagaStep {
    name = "Inventory Service";
    constructor(private failIntentionally: boolean) {}

    execute(): boolean {
        console.log("[Execute]   -> Attempting to reserve item in warehouse...");
        if (this.failIntentionally) {
            console.log("             ❌ ERROR: Item is out of stock!");
            return false;
        }
        return true;
    }
    compensate(): void {
        console.log("[Compensate]<- Restocking item to warehouse shelves.");
    }
}

class SagaOrchestrator {
    public runSaga(steps: SagaStep[]): boolean {
        const executedSteps: SagaStep[] = [];

        for (const step of steps) {
            console.log(`\n⚙️  Running: ${step.name}`);
            try {
                if (step.execute()) {
                    executedSteps.push(step);
                } else {
                    throw new Error(`Step ${step.name} failed gracefully.`);
                }
            } catch (error) {
                console.log("\n🚨 SAGA FAILED. INITIATING ROLLBACK SEQUENCE...");
                this.rollback(executedSteps);
                return false;
            }
        }
        console.log("\n✅ SAGA COMPLETED SUCCESSFULLY. ALL TRANSACTIONS COMMITTED.");
        return true;
    }

    private rollback(executedSteps: SagaStep[]): void {
        for (let i = executedSteps.length - 1; i >= 0; i--) {
            const step = executedSteps[i];
            console.log(`⏪ Rolling back: ${step.name}`);
            step.compensate();
        }
        console.log("🛡️ System successfully restored to initial state.");
    }
}

const orchestrator = new SagaOrchestrator();

console.log("=== SCENARIO 1: SUCCESSFUL CHECKOUT ===");
const stepsSuccess = [
    new CreateOrderStep(),
    new ProcessPaymentStep(),
    new ReserveInventoryStep(false)
];
const p1 = orchestrator.runSaga(stepsSuccess) === true;

console.log("\n\n=== SCENARIO 2: OUT OF STOCK INVENTORY (TRIGGERING SAGA ROLLBACK) ===");
const stepsFail = [
    new CreateOrderStep(),
    new ProcessPaymentStep(),
    new ReserveInventoryStep(true)
];
const p2 = orchestrator.runSaga(stepsFail) === false;

if (p1 && p2) {
    console.log("\nTypeScript Saga Pattern Test Passed!");
} else {
    process.exit(1);
}