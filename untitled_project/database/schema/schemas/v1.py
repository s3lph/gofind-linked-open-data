from typing import List

from untitled_project.database.schema import BaseSchema


class SchemaV1(BaseSchema):

    @staticmethod
    def version() -> int:
        return 1

    @staticmethod
    def migrations() -> List[str]:
        return [
            """
            CREATE TABLE places (
                p_id INTEGER(8) PRIMARY KEY AUTO_INCREMENT,
                p_lat FLOAT DEFAULT NULL,
                p_lon FLOAT DEFAULT NULL,
                p_name VARCHAR(300) UNIQUE NOT NULL,
                p_wikidata VARCHAR(64) DEFAULT NULL
            ) CHARACTER SET utf8mb4;
            """, """
            CREATE INDEX places_geolocation ON places(p_lat, p_lon);
            """, """
            CREATE TABLE documents (
                d_id INTEGER(8) PRIMARY KEY AUTO_INCREMENT,
                d_title VARCHAR(300) DEFAULT NULL,
                d_text TEXT NOT NULL,
                d_author VARCHAR(300) DEFAULT NULL,
                d_year INTEGER DEFAULT NULL,
                d_source VARCHAR(512) UNIQUE NOT NULL 
            ) CHARACTER SET utf8mb4;
            """, """
            CREATE TABLE documents_places (
                d_id INTEGER(8) NOT NULL,
                p_id INTEGER(8) NOT NULL,
                dp_position_in_text INTEGER(8) NOT NULL,
                PRIMARY KEY (d_id, p_id, dp_position_in_text),
                FOREIGN KEY (d_id) REFERENCES documents(d_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (p_id) REFERENCES places(p_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            ) CHARACTER SET utf8mb4;
            """, """
            CREATE TABLE images (
                i_id INTEGER(8) PRIMARY KEY AUTO_INCREMENT,
                p_id INTEGER(8) DEFAULT NULL,
                i_filepath VARCHAR(512) NOT NULL,
                i_author VARCHAR(300) DEFAULT NULL,
                i_year INTEGER DEFAULT NULL,
                i_source VARCHAR(512) DEFAULT NULL,
                FOREIGN KEY (p_id) REFERENCES places(p_id)
                    ON UPDATE CASCADE ON DELETE SET NULL 
            );
            """
        ]
