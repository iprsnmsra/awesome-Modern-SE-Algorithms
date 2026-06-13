using System;
using System.Collections.Generic;

public class Program {
    public interface ISagaStep {
        string Name { get; }
        bool Execute();
        void Compensate();
    }

    public class CreateOrderStep : ISagaStep {
        public string Name => "Order Service";
        public bool Execute() {
            Console.WriteLine("[Execute]   -> Creating pending order in database...");
            return true;
        }
        public void Compensate() {
            Console.WriteLine("[Compensate]<- Changing order status to 'CANCELED'.");
        }
    }

    public class ProcessPaymentStep : ISagaStep {
        public string Name => "Payment Service";
        public bool Execute() {
            Console.WriteLine("[Execute]   -> Charging credit card via Stripe...");
            return true;
        }
        public void Compensate() {
            Console.WriteLine("[Compensate]<- Issuing Idempotent Refund to credit card.");
        }
    }

    public class ReserveInventoryStep : ISagaStep {
        private bool failIntentionally;
        public ReserveInventoryStep(bool failIntentionally) {
            this.failIntentionally = failIntentionally;
        }
        public string Name => "Inventory Service";
        public bool Execute() {
            Console.WriteLine("[Execute]   -> Attempting to reserve item in warehouse...");
            if (failIntentionally) {
                Console.WriteLine("             ❌ ERROR: Item is out of stock!");
                return false;
            }
            return true;
        }
        public void Compensate() {
            Console.WriteLine("[Compensate]<- Restocking item to warehouse shelves.");
        }
    }

    public class SagaOrchestrator {
        public bool RunSaga(List<ISagaStep> steps) {
            List<ISagaStep> executedSteps = new List<ISagaStep>();

            foreach (var step in steps) {
                Console.WriteLine($"\n⚙️  Running: {step.Name}");
                try {
                    if (step.Execute()) {
                        executedSteps.Add(step);
                    } else {
                        throw new Exception("Step failed gracefully.");
                    }
                } catch {
                    Console.WriteLine("\n🚨 SAGA FAILED. INITIATING ROLLBACK SEQUENCE...");
                    Rollback(executedSteps);
                    return false;
                }
            }
            Console.WriteLine("\n✅ SAGA COMPLETED SUCCESSFULLY. ALL TRANSACTIONS COMMITTED.");
            return true;
        }

        private void Rollback(List<ISagaStep> executedSteps) {
            for (int i = executedSteps.Count - 1; i >= 0; i--) {
                var step = executedSteps[i];
                Console.WriteLine($"⏪ Rolling back: {step.Name}");
                step.Compensate();
            }
            Console.WriteLine("🛡️ System successfully restored to initial state.");
        }
    }
    public static int Main() {
        var orchestrator = new SagaOrchestrator();

        Console.WriteLine("=== SCENARIO 1: SUCCESSFUL CHECKOUT ===");
        var stepsSuccess = new List<ISagaStep> {
            new CreateOrderStep(),
            new ProcessPaymentStep(),
            new ReserveInventoryStep(false)
        };
        bool p1 = orchestrator.RunSaga(stepsSuccess);

        Console.WriteLine("\n\n=== SCENARIO 2: OUT OF STOCK INVENTORY (TRIGGERING SAGA ROLLBACK) ===");
        var stepsFail = new List<ISagaStep> {
            new CreateOrderStep(),
            new ProcessPaymentStep(),
            new ReserveInventoryStep(true)
        };
        bool p2 = !orchestrator.RunSaga(stepsFail);

        if (p1 && p2) {
            Console.WriteLine("\nC# Saga Pattern Test Passed!");
            return 0;
        }
        return 1;
    }
}