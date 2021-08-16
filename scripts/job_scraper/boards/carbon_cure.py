from boards.board import JobBoard, Job

import json


class CarbonCure( JobBoard ):

    def __init__( self ):
        super().__init__()

        self.name = "Carbon Cure"
        self.url = "https://carboncure.bamboohr.com/jobs/?source=carboncure"


    def process( self ):

        soup = self._get_soup()

        job_elements = soup.find( "script", id = "positionData" )
        job_elements = json.loads( job_elements.string.strip() )

        for job_json in job_elements:
            if job_json.get( "departmentLabel", None ) == "Engineering":
                title = job_json[ "jobOpeningName" ]
                location = job_json[ "location" ][ "name" ]
                url = f"https://carboncure.bamboohr.com/jobs/view.php?id={ job_json[ 'id' ] }&source=carboncure"

                self.jobs.append(
                    Job(
                        title,
                        location = location,
                        url = url
                    )
                )
