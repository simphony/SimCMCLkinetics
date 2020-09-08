from osp.wrappers.simcmclkinetics import AgentBridge
import unittest
import os
import sys

class AgentBridgeTest(unittest.TestCase):
    """Test class for the AgentBridge class.
    """

    # AgentBridge instance for testing
    agentBridge = AgentBridge()


    def test_encodeURL(self):
        """Tests encoding of simple JSON string
        """
        print("\nRunning test_encodeURL()...")

        sampleJSON = "{ \"name\":\"John\", \"age\":30, \"car\":null }"
        url = self.agentBridge.encodeURL(sampleJSON)

        # Check against expected result
        expectedURL = "%7B%20%22name%22%3A%22John%22%2C%20%22age%22%3A30%2C%20%22car%22%3Anull%20%7D"

        print("Result:   " + url)
        print("Expected: " + expectedURL)
        self.assertEqual(url, expectedURL)


    def test_buildSubmissionURL(self):
        """Tests that a job submission URL can be built
        """
        print("\nRunning test_buildSubmissionURL()...")

        sampleJSON = "{ \"name\":\"John\", \"age\":30, \"car\":null }"
        url = self.agentBridge.buildSubmissionURL(sampleJSON)

        # Check against expected result
        expectedURL = self.agentBridge.BASE_URL + "request?query=%7B%20%22name%22%3A%22John%22%2C%20%22age%22%3A30%2C%20%22car%22%3Anull%20%7D"

        print("Result:   " + url)
        print("Expected: " + expectedURL)
        self.assertEqual(url, expectedURL)

        
    def test_buildOutputURL(self):
        """Tests that an outputs request URL can be built
        """
        print("\nRunning test_buildOutputURL()...")

        self.agentBridge.jobID = "login.hpc.co.uk_0123456789"
        url = self.agentBridge.buildOutputURL()

        # Check against expected result
        expectedURL = self.agentBridge.BASE_URL + "output/request?query=%7B%22jobId%22%3A%22login.hpc.co.uk_0123456789%22%7D"

        print("Result:   " + url)
        print("Expected: " + expectedURL)
        self.assertEqual(url, expectedURL)
        

    def test_submitJob(self):
        """Tests if a job can be submitted via HTTP requests using the
        submitJob() function of the AgentBridge class. Note that this test
        WILL fail if the AgentBridge has an incorrect BASE_URL variable, or the
        HTTP server at that URL is not operational.
        """
        print("\nRunning test_submitJob()...")

        # Load the input JSON string for testing
        with open(os.path.join(sys.path[0], "test_input.json"), "r") as file:
            jsonString = file.read().replace("\n", "")

        # Try to submit a job using the AgentBridge
        result = self.agentBridge.submitJob(jsonString)
        self.assertTrue(result)
        self.assertFalse(self.agentBridge.jobID == None)


if __name__ == '__main__':
    unittest.main()        
