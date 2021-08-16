from boards.board import JobBoard, Job


class CarbonEngineering( JobBoard ):

    def __init__( self ):
        super().__init__()

        self.name = "Carbon Engineering"
        self.url = "https://carbonengineering.applytojob.com/apply/"


    def process( self ):

        soup = self._get_soup()

        # Now we can parse and get the jobs
        job_elements = soup.find( "div", class_ = "jobs-list" ).find_all( "li", class_ = "list-group-item" )

        for j in job_elements:
            title_html = j.find( "a" )
            location_html = j.find( "ul", class_ = "list-inline" ).find( "li" )
            self.jobs.append( 
                Job( 
                    title_html.text.strip(),
                    location = location_html.text.strip(),
                    url = title_html[ "href" ].strip()
                )
            )

