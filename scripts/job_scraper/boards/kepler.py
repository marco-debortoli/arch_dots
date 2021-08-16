from boards.board import JobBoard, Job


class KeplerCommunications( JobBoard ):

    def __init__( self ):
        super().__init__()

        self.name = "Kepler Communications"
        self.url = "https://www.keplercommunications.com/kepler/company-jobs"


    def process( self ):

        soup = self._get_soup()

        job_elements = soup.find( "div", class_ = "career-job-list" )

        in_engineering = False

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
                            
                            self.jobs.append(
                                Job(
                                    name_tag.text.strip(),
                                    location = location,
                                    url = name_tag[ "href" ].strip()
                                )
                            )
