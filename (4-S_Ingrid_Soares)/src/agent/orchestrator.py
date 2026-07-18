import logging
import time
from src.agent.tools import PurpleTeamTools
from src.agent.prompts import TTP_LIST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PurpleOrchestrator")

class PurpleOrchestrator:
    def __init__(self):
        self.tools = PurpleTeamTools()
        self.results = {}
        self.reasoning_log = []

    def log_reasoning(self, message: str):
        """Records the agent's thought process."""
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        logger.info(entry)
        self.reasoning_log.append(entry)

    def run_validation_cycle(self, auto_fix: bool = False):
        """
        Runs the full cycle for all configured TTPs. 
        If auto_fix is True, it will apply rules and re-test.
        """
        self.reasoning_log = [] # Reset log for new run
        self.log_reasoning("Starting Purple Team Validation Cycle...")
        
        for ttp in TTP_LIST:
            self.log_reasoning(f"Analyzing TTP {ttp}...")
            
            # 1. Simulate
            self.log_reasoning(f"Action: Simulating attack {ttp} via Atomic Red Team.")
            self.tools.simulate_attack(ttp)
            
            # 2. Check Detection
            self.log_reasoning(f"Action: Querying Wazuh API for alerts related to {ttp}.")
            det_res = self.tools.check_detection(ttp)
            
            if det_res["detected"]:
                self.log_reasoning(f"Conclusion: TTP {ttp} was detected. Security control is effective.")
                self.results[ttp] = "DETECTED"
            else:
                self.log_reasoning(f"Conclusion: TTP {ttp} was NOT detected. Blind spot identified.")
                self.results[ttp] = "MISSED"
                
                if auto_fix:
                    self.log_reasoning(f"Initiating Auto-Remediation for {ttp}...")
                    # 3. Propose and Apply
                    rule = self.tools.propose_detection_rule(ttp, "Simulated Sysmon logs")
                    self.log_reasoning(f"Proposed Rule: {rule}")
                    
                    apply_res = self.tools.apply_detection_rule(rule)
                    self.log_reasoning(f"Rule Deployment: {apply_res}")
                    
                    # 4. Re-test
                    self.log_reasoning(f"Re-testing TTP {ttp} after remediation...")
                    self.tools.simulate_attack(ttp)
                    re_det = self.tools.check_detection(ttp)
                    
                    if re_det["detected"]:
                        self.log_reasoning(f"Conclusion: TTP {ttp} is now DETECTED. Remediation successful.")
                        self.results[ttp] = "DETECTED"
                    else:
                        self.log_reasoning(f"Conclusion: TTP {ttp} still NOT detected. Manual intervention required.")
                        self.results[ttp] = "MISSED"
        
        self.log_reasoning("Validation Cycle Complete.")
        return self.results

    def validate_noise(self):
        """
        Tests the system for False Positives by simulating legitimate actions.
        """
        self.log_reasoning("Starting False Positive (Noise) Analysis...")
        noise_results = {}
        actions = ["update_service", "check_logs", "user_management"]
        
        for action in actions:
            self.log_reasoning(f"Simulating legitimate action: {action}")
            self.tools.simulate_legitimate_action(action)
            
            # In a real scenario, we'd check Wazuh for alerts triggered by these actions
            # Simulating: 'update_service' might trigger a false positive
            is_alerted = (action == "update_service") 
            
            if is_alerted:
                self.log_reasoning(f"Result: [ NOISE ] Action {action} triggered a false positive alert.")
                noise_results[action] = "FALSE POSITIVE"
            else:
                self.log_reasoning(f"Result: [ CLEAN ] Action {action} was correctly ignored.")
                noise_results[action] = "CLEAN"
                
        self.log_reasoning("Noise Analysis Complete.")
        return noise_results

if __name__ == "__main__":
    orchestrator = PurpleOrchestrator()
    final_results = orchestrator.run_validation_cycle()
    print("\nFinal Security Coverage Map:")
    for ttp, status in final_results.items():
        print(f"{ttp}: {status}")
