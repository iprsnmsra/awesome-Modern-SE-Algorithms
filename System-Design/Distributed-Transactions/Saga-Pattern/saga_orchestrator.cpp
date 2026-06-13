#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <algorithm>

using namespace std;

class SagaStep {
public:
    virtual ~SagaStep() = default;
    virtual string getName() const = 0;
    virtual bool execute() = 0;
    virtual void compensate() = 0;
};

class CreateOrderStep : public SagaStep {
public:
    string getName() const override { return "Order Service"; }
    bool execute() override {
        cout << "[Execute]   -> Creating pending order in database...\n";
        return true;
    }
    void compensate() override {
        cout << "[Compensate]<- Changing order status to 'CANCELED'.\n";
    }
};

class ProcessPaymentStep : public SagaStep {
public:
    string getName() const override { return "Payment Service"; }
    bool execute() override {
        cout << "[Execute]   -> Charging credit card via Stripe...\n";
        return true;
    }
    void compensate() override {
        cout << "[Compensate]<- Issuing Idempotent Refund to credit card.\n";
    }
};

class ReserveInventoryStep : public SagaStep {
private:
    bool failIntentionally;
public:
    ReserveInventoryStep(bool fail) : failIntentionally(fail) {}
    string getName() const override { return "Inventory Service"; }
    bool execute() override {
        cout << "[Execute]   -> Attempting to reserve item in warehouse...\n";
        if (failIntentionally) {
            cout << "             ❌ ERROR: Item is out of stock!\n";
            return false;
        }
        return true;
    }
    void compensate() override {
        cout << "[Compensate]<- Restocking item to warehouse shelves.\n";
    }
};

class SagaOrchestrator {
private:
    void rollback(const vector<SagaStep*>& executedSteps) {
        for (auto it = executedSteps.rbegin(); it != executedSteps.rend(); ++it) {
            cout << "⏪ Rolling back: " << (*it)->getName() << "\n";
            (*it)->compensate();
        }
        cout << "🛡️ System successfully restored to initial state.\n";
    }

public:
    bool runSaga(const vector<shared_ptr<SagaStep>>& steps) {
        vector<SagaStep*> executedSteps;

        for (const auto& step : steps) {
            cout << "\n⚙️  Running: " << step->getName() << "\n";
            try {
                if (step->execute()) {
                    executedSteps.push_back(step.get());
                } else {
                    throw runtime_error("Step failed gracefully.");
                }
            } catch (...) {
                cout << "\n🚨 SAGA FAILED. INITIATING ROLLBACK SEQUENCE...\n";
                rollback(executedSteps);
                return false;
            }
        }
        cout << "\n✅ SAGA COMPLETED SUCCESSFULLY. ALL TRANSACTIONS COMMITTED.\n";
        return true;
    }
};
int main() {
    SagaOrchestrator orchestrator;

    cout << "=== SCENARIO 1: SUCCESSFUL CHECKOUT ===\n";
    vector<shared_ptr<SagaStep>> stepsSuccess;
    stepsSuccess.push_back(make_shared<CreateOrderStep>());
    stepsSuccess.push_back(make_shared<ProcessPaymentStep>());
    stepsSuccess.push_back(make_shared<ReserveInventoryStep>(false));
    
    bool p1 = orchestrator.runSaga(stepsSuccess);

    cout << "\n\n=== SCENARIO 2: OUT OF STOCK INVENTORY (TRIGGERING SAGA ROLLBACK) ===\n";
    vector<shared_ptr<SagaStep>> stepsFail;
    stepsFail.push_back(make_shared<CreateOrderStep>());
    stepsFail.push_back(make_shared<ProcessPaymentStep>());
    stepsFail.push_back(make_shared<ReserveInventoryStep>(true));
    
    bool p2 = !orchestrator.runSaga(stepsFail);

    if (p1 && p2) {
        cout << "\nC++ Saga Pattern Test Passed!\n";
        return 0;
    }
    return 1;
}