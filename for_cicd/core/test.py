
from .src.utils import S3Handler, MySQLHandler

if __name__ == "__main__":

    db_handler = MySQLHandler()
    s3_handler = S3Handler()


    paperDOI = "10.18653/v1/2020.acl-demos.1"
    prefix_path = "https://documento-s3.s3.ap-northeast-2.amazonaws.com/papers/"
    db_handler.connect()
                
    insert_query = "SELECT s3_path FROM DOCUMENTO.paper WHERE paper_doi = %s"
    request_result = db_handler.fetch_one(insert_query, (paperDOI, ))

    if request_result['s3_path']:
        public_path = prefix_path + request_result["s3_path"]
        s3_handler.generate_presigned_url()


    else:
        print("error")
    
