from typing import Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from models.base import Base

Table = TypeVar("Table", bound=Base)


class AbstractDB:
    table: Type[Table]

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection
        self.all_columns = [m.key for m in self.table.__table__.columns]

    async def insert(self, entity: Table) -> Table:
        """
        Insert SQLalchemy table into SQL table

        Parameters
        ----------
        entity : Table
            SQLalchemy table

        Returns
        -------
        list[Table]
            List with one inserted sqlalchemy object
        """
        entity_dict = self._get_values_dict(entity)

        statement = insert(self.table).values(**entity_dict).returning(self.table)

        return await self._process_crud_statement(statement)

    async def get(self, entity_id: UUID) -> list[Table]:
        """
        Get a SQLalchemy table by its id from SQL table

        Parameters
        ----------
        entity_id : UUID
            UUID of the row

        Returns
        -------
        list[Table]
            List of SQLalchemy tables according to the selected condition
        """
        statement = select(self.table).where(self.table.id == entity_id)
        return await self._process_crud_statement(statement)

    async def get_all(self) -> list[Table]:
        """
        Get all rows from the SQL table

        Returns
        -------
        list[Table]
            List of SQLalchemy tables according to the selected condition
        """
        statement = select(self.table)
        return await self._process_crud_statement(statement)

    async def find(
        self,
        search_fields: dict,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        descending: Optional[bool] = None,
    ) -> list[Table]:
        """
        Find the rows from SQL table according to the condition with
        equality

        Parameters
        ----------
        search_fields : dict
            A dictionary with keys corresponding to column names and values
            corresponding to searched values

        offset : Optional[int] = None
            Offset value of the find statement

        limit : Optional[int] = None
            Limit value of the find statement

        order_by : Optional[int] = None
            Order by value of the find statement

        descending : Optional[int] = None
            Direction of the order of the find statement, if None then no order is applied

        Returns
        -------
        list[Table]
            List of SQLalchemy tables according to the selected condition
        """
        where_clause = and_(
            getattr(self.table, key) == value for key, value in search_fields.items()
        )

        # Determine order by
        if descending is not None:
            if descending:
                order_by = order_by.desc()
            else:
                order_by = order_by.asc()

        statement = (
            select(self.table)
            .where(where_clause)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )
        return await self._process_crud_statement(statement)

    async def update(self, entity_id: UUID, new_entity: Table) -> Table:
        """
        Update the row of the table with new values.

        Parameters
        ----------
        entity_id : UUID
            ID of the row to update
        new_entity : Table
            New SQLalchemy model which will update the row

        Returns
        -------
        Table
             List with one updated sqlalchemy object
        """
        new_entity_dict = self._get_values_dict(new_entity)

        statement = (
            update(self.table)
            .where(self.table.id == entity_id)
            .values(**new_entity_dict)
            .returning(self.table)
        )
        return await self._process_crud_statement(statement)

    async def delete(self, entity_id: UUID) -> list[Table]:
        """
        Delete a row from SQL table by its id

        Parameters
        ----------
        entity_id : UUID
            ID of the row to delete

        Returns
        -------
        list[Table]
            List with one deleted sqlalchemy object
        """
        statement = (
            delete(self.table).where(self.table.id == entity_id).returning(self.table)
        )
        return await self._process_crud_statement(statement)

    def _get_values_dict(self, entity: Table) -> dict:
        return {
            key: value
            for key, value in entity.__dict__.items()
            if key in self.all_columns
        }

    async def _process_crud_statement(self, statement) -> Table:
        async with self.connection.connect() as conn:
            result = await conn.execute(statement)
            await conn.commit()

        return [self.table(**val._asdict()) for val in result]
