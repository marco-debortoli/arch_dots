
import requests
import json

from bs4 import BeautifulSoup


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

    
    def get_unique_key( self ):
        """
        Get the unique representation of this object
        """

        return f"{ self.title }+{ self.location }+{ self.url }"


    @classmethod
    def from_unique_key( cls, unique_key ):
        """
        Restore a Job object from its unique key
        """

        title, location, url = unique_key.split( "+" )

        return cls( title, location = location, url = url )


class JobBoard( object ):

    def __init__( self ):
        self.url = None
        self.name = None
        self.jobs = [] # Will be filled when `process` is called


    def _get_soup( self ):
        """
        Using the URL, return a BeautifulSoup object that represents the job board page
        """

        page = requests.get( self.url )
    
        if page.status_code == 200:
            return BeautifulSoup( page.content, "html.parser" )

        return None       


    def process( self ):
        """
        Process the Job Board and return a list of Job objects
        """

        raise NotImplementedError( "process needs to be implemented for each job board" )


    def export_to_json( self ):
        """
        Export the JobBoard to a JSON dictionary.
        Should be called after `process` which will populate the jobs
        """

        return {
            self.name: [ j.get_unique_key() for j in self.jobs ]
        }


    def print_all_jobs( self ):
        """
        Print all jobs
        """

        print( f"\n -- { self.name } --\n" )

        for j in self.jobs:
            print( f"{ j }\n" )
