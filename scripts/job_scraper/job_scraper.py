import argparse
import os
import json

from boards.carbon_cure import CarbonCure
from boards.carbon_engineering import CarbonEngineering
from boards.kepler import KeplerCommunications
from boards.board import Job


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = 'Scrape some job boards for jobs I find interesting and return relevant postings'
    )

    parser.add_argument( 
        '--print-all', 
        action = "store_true",
        help = 'If provided will print all jobs, not just new ones'
    )

    args = parser.parse_args()

    boards = [
        CarbonCure,
        CarbonEngineering,
        KeplerCommunications
    ]

    path = os.path.abspath( __file__ )
    path = "/".join( path.split( "/" )[ :-1 ] )

    if os.path.exists( f"{ path }/archive.json" ):
        with open( "archive.json", "r" ) as f:
            archive = json.load( f )

    else:
        archive = dict()


    new_archive = dict()

    for b in boards:
        # Instantiate the object
        b_obj = b()

        # Fetch new jobs
        b_obj.process()


        if args.print_all:
            b_obj.print_all_jobs()
        else:
            archived_jobs = archive.get( b_obj.name, [] )

            new_job_keys = [ j.get_unique_key() for j in b_obj.jobs ]

            # Print New
            new = [
                j for j in b_obj.jobs if j.get_unique_key() not in archived_jobs
            ]

            # Print Removed
            removed = [
                Job.from_unique_key( k ) for k in archived_jobs if k not in new_job_keys
            ]

            print( f"\n -- { b_obj.name } -- \n" )

            if len( new ) > 0:
                print( "New jobs\n" )

                for j in new:
                    print( f"{ j }\n" )

            else:
                print( "No new jobs\n" )


            if len( removed ) > 0:
                print( "Removed jobs\n" )

                for j in removed:
                    print( f"{ j }\n" )

            else:
                print( "No removed jobs\n" )

        
        new_archive.update( b_obj.export_to_json() )


    # Archive
    with open( "archive.json", "w+" ) as f:
        json.dump( new_archive, f, sort_keys = True, indent = 2 )