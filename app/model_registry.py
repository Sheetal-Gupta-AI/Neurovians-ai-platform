from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.models import RegisteredLLM


class ModelRegistry:
    def __init__(
            self,
            connection_pool: ConnectionPool,
            organization_id: str,
    ) -> None:
        self.connection_pool = connection_pool
        self.organization_id = organization_id

    def list_models(self) -> list[RegisteredLLM]:
        query = """
            SELECT model_id, name, provider, status, endpoint_or_path
            FROM llm_models
            WHERE organization_id = %s
            ORDER BY created_at
        """

        with self.connection_pool.connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (self.organization_id,))
                return [
                    RegisteredLLM.model_validate(row)
                    for row in cursor.fetchall()
                ]

    def get_model(self, model_id: str) -> RegisteredLLM | None:
        query = """
            SELECT model_id, name, provider, status, endpoint_or_path
            FROM llm_models
            WHERE organization_id = %s AND model_id = %s
        """

        with self.connection_pool.connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (self.organization_id, model_id))
                row = cursor.fetchone()

        return RegisteredLLM.model_validate(row) if row else None

    def create_model(self, model: RegisteredLLM) -> RegisteredLLM:
        query = """
            INSERT INTO llm_models (
                organization_id,
                model_id,
                name,
                provider,
                status,
                endpoint_or_path
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (organization_id, model_id) DO NOTHING
            RETURNING model_id, name, provider, status, endpoint_or_path
        """

        values = (
            self.organization_id,
            model.model_id,
            model.name,
            model.provider,
            model.status.value,
            model.endpoint_or_path,
        )

        with self.connection_pool.connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, values)
                row = cursor.fetchone()

        if row is None:
            raise ValueError("Model ID already exists.")

        return RegisteredLLM.model_validate(row)

    def update_model(
            self,
            model_id: str,
            model: RegisteredLLM,
    ) -> RegisteredLLM | None:
        query = """
            UPDATE llm_models
            SET
                name = %s,
                provider = %s,
                status = %s,
                endpoint_or_path = %s,
                updated_at = NOW()
            WHERE organization_id = %s AND model_id = %s
            RETURNING model_id, name, provider, status, endpoint_or_path
        """

        values = (
            model.name,
            model.provider,
            model.status.value,
            model.endpoint_or_path,
            self.organization_id,
            model_id,
        )

        with self.connection_pool.connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, values)
                row = cursor.fetchone()

        return RegisteredLLM.model_validate(row) if row else None

    def delete_model(self, model_id: str) -> bool:
        query = """
            DELETE FROM llm_models
            WHERE organization_id = %s AND model_id = %s
            RETURNING model_id
        """

        with self.connection_pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (self.organization_id, model_id))
                return cursor.fetchone() is not None