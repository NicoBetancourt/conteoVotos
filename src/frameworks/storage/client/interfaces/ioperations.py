
import json


class psql_operations:
    def insertOne(self, id: str) -> json:
        """Load in the file for extracting text."""
        pass

    def insertAll(self) -> json:
        """Load in the file for extracting text."""
        pass

    def updateOne(self, id: str) -> dict:
        """Extract text from the currently loaded file."""
        pass

    # insertOne(item: T, collection: Collection): Promise<T>;
    # updateOne(id: string, item: T, collection: Collection): Promise<T | null>;
    # deleteOne(id: string, collection: Collection): Promise<boolean>;
    # //Reading
    # findAll(filter: FDal,collection: Collection): Promise<T[]>;
    # findOne(id: string, collection: Collection): Promise<T | null>;
