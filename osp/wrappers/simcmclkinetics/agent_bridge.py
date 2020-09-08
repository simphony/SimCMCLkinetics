import requests
import json
import urllib.parse


class AgentBridge:
    """Class to handle communicating with the KineticsAgent servlet via a
    series of HTTP requests.
    """

    # Base URL for HTTP requests
    BASE_URL = "http://localhost:8088/KineticsAgent/job/"

    # Additional URL part for job submission
    SUBMISSION_URL_PART = "request?query="

    # Additional URL part for requesting job outputs
    OUTPUT_URL_PART = "output/request?query="

    # ID of generated job
    jobID = None
  

    def submitJob(self, jsonString: str) -> bool:
        """Submits a job using a HTTP request with the input JSON string, stores
        resulting job ID returned by KineticsAgent.

        Arguments:
            jsonString (str) -- Input parameter data in raw JSON form

        Returns:
            True if a job was succesfully submitted
        """

        # Check that we have JSON data
        if not jsonString:
            print("Supplied JSON string is empty!")
            return False

        # Build the job submission URL
        url = self.buildSubmissionURL(jsonString)

        # Submit the request and get the response
        response = requests.get(url)

        # Check the HTTP return code
        if(response.status_code >= 200):
            print("HTTP request returns status code 200 (OK).")
        else:
            print("HTTP request returns unexpected status code %s" % (response.status_code))
            print("Reason: %s" % (response.reason))
            return False

        # Get the returned RAW text
        returnedRaw = response.text

        # Parse into JSON
        returnedJSON = json.loads(returnedRaw)

        # Get the generated job ID from the JSON
        self.jobID = returnedJSON["jobId"]
        print("Received job ID: " + self.jobID)

        print("Job submitted successfully, resulting job ID is %s" % (self.jobID))
        return True


    def buildSubmissionURL(self, jsonString: str) -> str:
        """Builds the submission URL for the input JSON string.

        Arguments:
            jsonString (str) -- Input parameter data in JSON form

        Returns:
            Full job submission URL
        """
        url = self.BASE_URL + self.SUBMISSION_URL_PART
        url += self.encodeURL(jsonString)
        return url   


    def buildOutputURL(self) -> str:
        """Builds the request outputs URL for the current job ID.

        Arguments:
            jsonString (str) -- Input parameter data in JSON form

        Returns:
            Full output request URL
        """
        url = self.BASE_URL + self.OUTPUT_URL_PART

        # Build JSON from job ID
        jsonString = "{\"jobId\":\"" + self.jobID + "\"}"

        url += self.encodeURL(jsonString)
        return url


    def encodeURL(self, string: str) -> str:
        """Encodes the input string into a valid URL

        Arguments:
            string (str) --- string to encode

        Returns:
            Valid URL
        """
        return urllib.parse.quote(string)
