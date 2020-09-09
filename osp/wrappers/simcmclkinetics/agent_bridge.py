import requests
import json
import urllib.parse
import time

class AgentBridge:
    """Class to handle communicating with the KineticsAgent servlet via a
    series of HTTP requests.
    """

    # Polling interval when waiting or jobs to finish (seconds)
    POLL_INTERVAL = 30

    # Maximum number of requests when waiting for jobs to finish
    MAX_ATTEMPTS = 20

    # Base URL for HTTP requests
    BASE_URL = "http://localhost:8088/KineticsAgent/job/"

    # Additional URL part for job submission
    SUBMISSION_URL_PART = "request?query="

    # Additional URL part for requesting job outputs
    OUTPUT_URL_PART = "output/request?query="

    # ID of generated job
    jobID = None
  

    def runJob(self, jsonString: str):
        """Runs a complete Kinetics simulation on a remote machine via use of HTTP requests.
        Note that this method will block until the remote job is completed and has returned
        a result or error message.

        Arguments:
            jsonString (str) -- JSON input data string

        Returns:
            Resulting JSON data objects (or None if error occurs)
        """
        submitted = self.submitJob(jsonString)

        if(submitted == False):
            print("Job was not submitted successfully, returning None")
            return None

        # Wait a little time
        time.sleep(self.POLL_INTERVAL)

        # Request outputs
        outputs = self.requestOutputs()

        if(outputs == None):
            print("Could not get job outputs (failed job?), returning None")
            return None

        print("Job completed, returning JSON representation of output data")
        return outputs


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
        if(response.status_code != 200):
            print("HTTP request returns unexpected status code %s" % (response.status_code))
            print("Reason: %s" % (response.reason))
            return False

        # Get the returned RAW text
        returnedRaw = response.text

        # Parse into JSON
        returnedJSON = json.loads(returnedRaw)

        # Get the generated job ID from the JSON
        self.jobID = returnedJSON["jobId"]
        print("Job submitted successfully, resulting job ID is %s" % (self.jobID))
        return True


    def requestOutputs(self):
        """Sends a HTTP request asking for the results of the submitted job.
        If the job fails, None is returned. Note that this function will block
        until the job has executed on the remote machine.

        Returns:
            JSON object detailing job outputs (None in case of failure)
        """

        # Build the URL
        url = self.buildOutputURL()

        # Submit the request
        result = self.__getJobResults(url, 1)
        if(result == None):
            print("Job was not completed on the remote HPC!")
            return None

        # Detect if the job has actually finished successfully
        if("message" in result):
            message = result["message"]

            if(message.find("error") >= 0):
                print("Job finished with errors, no outputs received.")
                return None

        print("Job finished successfully, output data received.")
        return result
     

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


    def __getJobResults(self, url: str, attempt: int):
        """Make a HTTP request to get the final results of the submitted job.
        Recurses until the request reports that the job is finished (or a maximum
        number of attempts is reached)

        Arguments:
            url (str)     -- Output request URL
            attempt (int) -- Current attempt index

        Returns:
            JSON object parsed from response (or None if failure occurs)
        """

        # Fail at is more than max attempts
        if(attempt >= self.MAX_ATTEMPTS):
            print("Maximum number of attempts reached, considering job a failure.")
            return None

        # Submit the request
        response = requests.get(url)

        # Check the HTTP return code
        if(response.status_code != 200):
            print("HTTP request returns unexpected status code %s" % (response.status_code))
            print("Reason: %s" % (response.reason))
            return None

        # Get the returned RAW text
        returnedRaw = response.text

        # Parse into JSON
        returnedJSON = json.loads(returnedRaw)   

        # Detect if the job has actually finished successfully
        if("message" in returnedJSON):
            message = returnedJSON["message"]

            if((message.find("executing") >= 0) or (message.find("executed") >= 0)):
                print("Job still running (attempt %s of %s)..." % (attempt, self.MAX_ATTEMPTS))

                # Wait 
                time.sleep(self.POLL_INTERVAL)
                return self.__getJobResults(url, attempt + 1)
            
        else:
            print("Job has finished.")
            return returnedJSON
