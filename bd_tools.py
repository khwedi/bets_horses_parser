import aiomysql
import asyncio
import variables

local_variables = variables.Variables()


class BD_Tools:
    def __init__(self):
        self.connection = None
        self.login = 'Diana'
        self.password = 'Dianasuper247'
        self.host = '78.29.40.225'
        self.port = 3306
        self.output_object_massive = []

    async def open_connect(self):
        if self.connection is None:
            try:
                self.connection = await aiomysql.create_pool(
                    host=self.host,
                    port=self.port,
                    user=self.login,
                    password=self.password,
                    charset='utf8mb4',
                    db='mysql',
                    cursorclass=aiomysql.cursors.DictCursor
                )
                print("Connection to the server is established")
            except aiomysql.Error as error:
                print(f"Error connecting to database: {error}")
                raise

    async def close(self):
        if self.connection:
            self.connection.close()
            await self.connection.wait_closed()
            print("Disconnected from the server")

    async def execute_script(self, connection, script, params=None, fetch=True):
        try:
            async with connection.cursor() as cursor:
                await cursor.execute(script, params)
                if fetch:
                    return await cursor.fetchall()

        except aiomysql.Error as error:
            print(f"Error executing data: {error}")
            return None

    async def upload_data(self, script):
        try:
            async with self.connection.acquire() as connection:
                return await self.execute_script(connection, script, fetch=True)

        except aiomysql.Error as error:
            print(f"Error uploading data: {error}")
            return None

    async def update_data(self, script, status, bk1_winloss, id):
        try:
            async with self.connection.acquire() as connection:
                params = (status, bk1_winloss, id)
                await self.execute_script(connection, script, params=params, fetch=False)
                await connection.commit()

        except aiomysql.Error as error:
            print(f"Error updating data: {error}")



