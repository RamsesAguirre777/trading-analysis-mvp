#!/usr/bin/env python3
"""
Test Script for N8N Trading Analysis Pipeline
Tests the complete automation workflow end-to-end
"""

import requests
import json
import time
import os
from datetime import datetime


class N8NPipelineTest:
    def __init__(self, n8n_url="http://localhost:5678", webhook_path="/webhook/trading"):
        self.n8n_url = n8n_url
        self.webhook_url = f"{n8n_url}{webhook_path}"
        self.test_results = []
        
    def log_test(self, test_name, success, message, duration=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        duration_str = f" ({duration:.2f}s)" if duration else ""
        print(f"{status}: {test_name} - {message}{duration_str}")
        
    def test_n8n_health(self):
        """Test if N8N is running and healthy"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.n8n_url}/healthz", timeout=5)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("N8N Health Check", True, "N8N is running", duration)
                return True
            else:
                self.log_test("N8N Health Check", False, f"HTTP {response.status_code}", duration)
                return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("N8N Health Check", False, f"Connection failed: {str(e)}", duration)
            return False
    
    def test_webhook_trigger(self):
        """Test webhook trigger with sample data"""
        start_time = time.time()
        
        test_payload = {
            "symbol": "NVDA",
            "test_mode": True,
            "manual_break_points": {
                "break_point": 171.67,
                "max_pos_exp": 174.04,
                "int_pos_exp": 172.85,
                "int_neg_exp": 170.48,
                "max_neg_exp": 169.29
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=test_payload,
                timeout=60,  # Allow up to 60 seconds for complete analysis
                headers={"Content-Type": "application/json"}
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    result_data = response.json()
                    if "trading_signals" in result_data:
                        self.log_test(
                            "Webhook Trigger", 
                            True, 
                            f"Analysis completed for {result_data.get('symbol', 'UNKNOWN')}", 
                            duration
                        )
                        return True, result_data
                    else:
                        self.log_test(
                            "Webhook Trigger", 
                            False, 
                            "Response missing trading_signals", 
                            duration
                        )
                        return False, None
                except json.JSONDecodeError:
                    self.log_test(
                        "Webhook Trigger", 
                        False, 
                        "Response is not valid JSON", 
                        duration
                    )
                    return False, None
            else:
                self.log_test(
                    "Webhook Trigger", 
                    False, 
                    f"HTTP {response.status_code}: {response.text[:100]}", 
                    duration
                )
                return False, None
                
        except requests.exceptions.Timeout:
            duration = time.time() - start_time
            self.log_test("Webhook Trigger", False, "Request timeout (>60s)", duration)
            return False, None
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Webhook Trigger", False, f"Request failed: {str(e)}", duration)
            return False, None
    
    def test_dashboard_update(self):
        """Test if dashboard data was updated"""
        dashboard_file = "dashboard/data/latest_analysis.json"
        
        if not os.path.exists(dashboard_file):
            self.log_test("Dashboard Update", False, f"File not found: {dashboard_file}")
            return False
            
        try:
            with open(dashboard_file, 'r') as f:
                data = json.load(f)
            
            # Check if timestamp is recent (within last 5 minutes)
            if "analysis_timestamp" in data:
                timestamp = datetime.fromisoformat(data["analysis_timestamp"].replace('Z', '+00:00'))
                age_seconds = (datetime.now().astimezone() - timestamp).total_seconds()
                
                if age_seconds < 300:  # 5 minutes
                    self.log_test(
                        "Dashboard Update", 
                        True, 
                        f"Data updated {age_seconds:.0f}s ago"
                    )
                    return True
                else:
                    self.log_test(
                        "Dashboard Update", 
                        False, 
                        f"Data is stale ({age_seconds:.0f}s old)"
                    )
                    return False
            else:
                self.log_test("Dashboard Update", False, "Missing timestamp in data")
                return False
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.log_test("Dashboard Update", False, f"File read error: {str(e)}")
            return False
    
    def test_calculator_direct(self):
        """Test trading calculator directly"""
        start_time = time.time()
        
        try:
            import subprocess
            result = subprocess.run(
                ["python", "src/trading_calculator.py", "--input", "data/nvda_test_data.json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            duration = time.time() - start_time
            
            if result.returncode == 0:
                try:
                    output_data = json.loads(result.stdout)
                    if "trading_signals" in output_data:
                        self.log_test(
                            "Calculator Direct", 
                            True, 
                            "Calculator executed successfully", 
                            duration
                        )
                        return True
                    else:
                        self.log_test(
                            "Calculator Direct", 
                            False, 
                            "Output missing trading_signals", 
                            duration
                        )
                        return False
                except json.JSONDecodeError:
                    self.log_test(
                        "Calculator Direct", 
                        False, 
                        "Calculator output is not valid JSON", 
                        duration
                    )
                    return False
            else:
                self.log_test(
                    "Calculator Direct", 
                    False, 
                    f"Exit code {result.returncode}: {result.stderr}", 
                    duration
                )
                return False
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            self.log_test("Calculator Direct", False, "Calculator timeout", duration)
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Calculator Direct", False, f"Execution error: {str(e)}", duration)
            return False
    
    def validate_analysis_format(self, analysis_data):
        """Validate the analysis data format"""
        required_fields = [
            "analysis_timestamp",
            "symbol", 
            "gap_analysis",
            "trading_signals"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in analysis_data:
                missing_fields.append(field)
        
        if missing_fields:
            self.log_test(
                "Analysis Format", 
                False, 
                f"Missing fields: {', '.join(missing_fields)}"
            )
            return False
        
        # Validate trading signals structure
        trading_signals = analysis_data.get("trading_signals", {})
        signal_fields = ["primary_direction", "confidence", "entry_levels"]
        
        for field in signal_fields:
            if field not in trading_signals:
                missing_fields.append(f"trading_signals.{field}")
        
        if missing_fields:
            self.log_test(
                "Analysis Format", 
                False, 
                f"Missing signal fields: {', '.join(missing_fields)}"
            )
            return False
        
        self.log_test("Analysis Format", True, "All required fields present")
        return True
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 Starting N8N Trading Analysis Pipeline Tests\n")
        
        # Test 1: N8N Health
        if not self.test_n8n_health():
            print("\n❌ N8N is not running. Please start N8N and try again.")
            return False
        
        # Test 2: Calculator Direct (baseline)
        self.test_calculator_direct()
        
        # Test 3: Full Pipeline via Webhook
        webhook_success, analysis_data = self.test_webhook_trigger()
        
        if webhook_success and analysis_data:
            # Test 4: Validate Analysis Format
            self.validate_analysis_format(analysis_data)
        
        # Test 5: Dashboard Update
        time.sleep(2)  # Give file system a moment
        self.test_dashboard_update()
        
        # Summary
        self.print_summary()
        
        # Return overall success
        return all(result["success"] for result in self.test_results)
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        passed = sum(1 for r in self.test_results if r["success"])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Pipeline is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the issues above.")
            
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            duration = f" ({result['duration_seconds']:.2f}s)" if result.get('duration_seconds') else ""
            print(f"  {status} {result['test']}: {result['message']}{duration}")


def main():
    """Main test execution"""
    # Change to project directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    tester = N8NPipelineTest()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    main()