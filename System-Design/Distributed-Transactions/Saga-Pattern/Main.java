import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    interface SagaStep {
        String getName();
        boolean execute();
        void compensate();
    }

    static class CreateOrderStep implements SagaStep {
        public String getName() { return "Order Service"; }
        public boolean execute() {
            System.out.println("[Execute]   -> Creating pending order in database...");
            return true;
        }
        public void compensate() {
            System.out.println("[Compensate]<- Changing order status to 'CANCELED'.");
        }
    }

    static class ProcessPaymentStep implements SagaStep {
        public String getName() { return "Payment Service"; }
        public boolean execute() {
            System.out.println("[Execute]   -> Charging credit card via Stripe...");
            return true;
        }
        public void compensate() {
            System.out.println("[Compensate]<- Issuing Idempotent Refund to credit card.");
        }
    }

    static class ReserveInventoryStep implements SagaStep {
        private boolean failIntentionally;
        public ReserveInventoryStep(boolean failIntentionally) {
            this.failIntentionally = failIntentionally;
        }
        public String getName() { return "Inventory Service"; }
        public boolean execute() {
            System.out.println("[Execute]   -> Attempting to reserve item in warehouse...");
            if (failIntentionally) {
                System.out.println("             ❌ ERROR: Item is out of stock!");
                return false;
            }
            return true;
        }
        public void compensate() {
            System.out.println("[Compensate]<- Restocking item to warehouse shelves.");
        }
    }

    static class SagaOrchestrator {
        public boolean runSaga(List<SagaStep> steps) {
            List<SagaStep> executedSteps = new ArrayList<>();

            for (SagaStep step : steps) {
                System.out.println("\n⚙️  Running: " + step.getName());
                try {
                    if (step.execute()) {
                        executedSteps.add(step);
                    } else {
                        throw new RuntimeException("Step failed gracefully.");
                    }
                } catch (Exception e) {
                    System.out.println("\n🚨 SAGA FAILED. INITIATING ROLLBACK SEQUENCE...");
                    rollback(executedSteps);
                    return false;
                }
            }
            System.out.println("\n✅ SAGA COMPLETED SUCCESSFULLY. ALL TRANSACTIONS COMMITTED.");
            return true;
        }

        private void rollback(List<SagaStep> executedSteps) {
            List<SagaStep> reverseSteps = new ArrayList<>(executedSteps);
            Collections.reverse(reverseSteps);
            for (SagaStep step : reverseSteps) {
                System.out.println("⏪ Rolling back: " + step.getName());
                step.compensate();
            }
            System.out.println("🛡️ System successfully restored to initial state.");
        }
    }

    public static void main(String[] args) {
        SagaOrchestrator orchestrator = new SagaOrchestrator();

        System.out.println("=== SCENARIO 1: SUCCESSFUL CHECKOUT ===");
        List<SagaStep> stepsSuccess = new ArrayList<>();
        stepsSuccess.add(new CreateOrderStep());
        stepsSuccess.add(new ProcessPaymentStep());
        stepsSuccess.add(new ReserveInventoryStep(false));
        
        boolean p1 = orchestrator.runSaga(stepsSuccess);

        System.out.println("\n\n=== SCENARIO 2: OUT OF STOCK INVENTORY (TRIGGERING SAGA ROLLBACK) ===");
        List<SagaStep> stepsFail = new ArrayList<>();
        stepsFail.add(new CreateOrderStep());
        stepsFail.add(new ProcessPaymentStep());
        stepsFail.add(new ReserveInventoryStep(true));
        
        boolean p2 = !orchestrator.runSaga(stepsFail);

        if (p1 && p2) {
            System.out.println("\nJava Saga Pattern Test Passed!");
        } else {
            System.exit(1);
        }
    }
}