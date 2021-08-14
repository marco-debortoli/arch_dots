import requests
import json

from bs4 import BeautifulSoup


# TODO
# - Create classes for each "Job Board" object
# - Save jobs to file to get list of new jobs


class Job( object ):

    def __init__( self, title, location = None, url = None ):
        self.title = title
        self.location = location
        self.url = url


    def __str__( self ):
        """
        Return a string representation of the job object
        """

        title_str = f"Job Title: { self.title }"
        location_str = f"Location: { self.location if self.location else 'Unknown' }"
        url_str = f"URL: { self.url if self.url else 'Undefined' }"

        return f"{ title_str }\n{ location_str }\n{ url_str }"



def get_soup( url ):
    """
    Given a URL, return the BeautifulSoup object for that url
    """

    page = requests.get( url )
    
    if page.status_code == 200:
        return BeautifulSoup( page.content, "html.parser" )

    return None


def carbon_engineering():
    soup = get_soup( "https://carbonengineering.applytojob.com/apply/" )

    # Now we can parse and get the jobs
    job_elements = soup.find( "div", class_ = "jobs-list" ).find_all( "li", class_ = "list-group-item" )

    job_objs = list()

    for j in job_elements:
        title_html = j.find( "a" )
        location_html = j.find( "ul", class_ = "list-inline" ).find( "li" )
        job_objs.append( 
            Job( 
                title_html.text.strip(),
                location = location_html.text.strip(),
                url = title_html[ "href" ].strip()
            )
        )

    print( "\n-- Carbon Engineering --\n")

    for j in job_objs:
        print( f"{ j }\n" )

    

def carbon_cure():
    soup = get_soup( "https://carboncure.bamboohr.com/jobs/?source=carboncure" )

    # I only care about the engineering jobs

    job_elements = soup.find( "script", id = "positionData" )
    job_elements = json.loads( job_elements.string.strip() )

    job_objs = list()

    for job_json in job_elements:
        if job_json.get( "departmentLabel", None ) == "Engineering":
            title = job_json[ "jobOpeningName" ]
            location = job_json[ "location" ][ "name" ]
            url = f"https://carboncure.bamboohr.com/jobs/view.php?id={ job_json[ 'id' ] }&source=carboncure"

            job_objs.append(
                Job(
                    title,
                    location = location,
                    url = url
                )
            )

    print( "\n-- CarbonCure --\n")

    for j in job_objs:
        print( f"{ j }\n" )    



def kepler_communications():
    soup = get_soup( "https://www.keplercommunications.com/kepler/company-jobs" )

    job_elements = soup.find( "div", class_ = "career-job-list" )

    in_engineering = False

    job_objs = list()

    for div in job_elements.find_all( "div" ):
        if "job-direction" in div[ "class" ][ 0 ]:
            in_engineering = "Engineering" in div.text.strip()

        else:
            if in_engineering:
                if "jobs-table__item" in div[ "class" ][ 0 ]:
                    rows = div.find_all( "div", class_ = "jobs-table__row" )

                    for r in rows:
                        name_tag = r.find( "a" )
                        location = r.find( "div", class_ = "jobs-table__job-address" ).text.strip()
                        
                        job_objs.append(
                            Job(
                                name_tag.text.strip(),
                                location = location,
                                url = name_tag[ "href" ].strip()
                            )
                        )

    print( "\n-- Kepler Communications --\n")

    for j in job_objs:
        print( f"{ j }\n" )    


if __name__ == "__main__":
    carbon_engineering()
    carbon_cure()
    kepler_communications()
